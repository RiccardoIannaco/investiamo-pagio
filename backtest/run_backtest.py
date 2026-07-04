"""Rigenera i dati di backtest: scarica i proxy, simula i portafogli, scrive i JSON.

Uso (dalla radice del repo):
    python backtest/run_backtest.py            # scarica/aggiorna i CSV e riscrive i JSON
    python backtest/run_backtest.py --offline  # usa solo i CSV già in backtest/dati_grezzi/
"""
import datetime
import json
import pathlib
import sys

import pandas as pd
import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from metriche import (
    cagr,
    max_drawdown,
    peggior_anno,
    simula_portafoglio,
    volatilita_annualizzata,
)

RADICE = pathlib.Path(__file__).resolve().parent.parent
GREZZI = pathlib.Path(__file__).resolve().parent / "dati_grezzi"
USCITA = RADICE / "dati" / "backtest"
CAMBIO = "EURUSD=X"


def carica_portafogli() -> list[dict]:
    portafogli = []
    for percorso in sorted((RADICE / "dati" / "portafogli").glob("*.yaml")):
        p = yaml.safe_load(percorso.read_text(encoding="utf-8"))
        somma = sum(a["peso"] for a in p["allocazioni"])
        if abs(somma - 1.0) > 1e-6:
            sys.exit(f"ERRORE: i pesi di {p['slug']} sommano a {somma:g}, non a 1")
        for a in p["allocazioni"]:
            if not a.get("proxy"):
                sys.exit(f"ERRORE: allocazione senza proxy in {p['slug']}")
        portafogli.append(p)
    if not portafogli:
        sys.exit("ERRORE: nessun portafoglio in dati/portafogli/")
    return portafogli


def scarica(ticker: str, offline: bool) -> pd.Series:
    csv = GREZZI / f"{ticker.replace('=', '_')}.csv"
    if not offline:
        import yfinance as yf

        dati = yf.download(ticker, period="max", interval="1mo", auto_adjust=True, progress=False)
        if dati is None or dati.empty:
            sys.exit(f"ERRORE: nessun dato scaricato per {ticker} (riprova o usa --offline)")
        GREZZI.mkdir(exist_ok=True)
        chiusure = dati["Close"]
        if isinstance(chiusure, pd.DataFrame):  # yfinance recente: colonne multi-livello
            chiusure = chiusure.iloc[:, 0]
        chiusure.to_csv(csv)
    if not csv.exists():
        sys.exit(f"ERRORE: manca {csv}; esegui senza --offline almeno una volta")
    serie = pd.read_csv(csv, index_col=0, parse_dates=True).iloc[:, 0]
    return serie.dropna()


def main() -> None:
    offline = "--offline" in sys.argv
    portafogli = carica_portafogli()
    ticker_unici = sorted({a["proxy"] for p in portafogli for a in p["allocazioni"]})
    print(f"proxy da scaricare: {', '.join(ticker_unici)} + {CAMBIO}")

    prezzi_usd = pd.DataFrame({t: scarica(t, offline) for t in ticker_unici})
    eurusd = scarica(CAMBIO, offline)
    prezzi = prezzi_usd.div(eurusd, axis=0)
    prezzi = prezzi.resample("ME").last().dropna()
    if len(prezzi) < 36:
        sys.exit(f"ERRORE: finestra comune troppo corta ({len(prezzi)} mesi)")

    USCITA.mkdir(parents=True, exist_ok=True)
    for p in portafogli:
        pesi: dict[str, float] = {}
        for a in p["allocazioni"]:
            pesi[a["proxy"]] = pesi.get(a["proxy"], 0.0) + a["peso"]
        serie = simula_portafoglio(prezzi[list(pesi)], pesi)
        risultato = {
            "portafoglio": p["slug"],
            "aggiornato": datetime.date.today().isoformat(),
            "valuta": "EUR",
            "finestra": [serie.index[0].strftime("%Y-%m"), serie.index[-1].strftime("%Y-%m")],
            "serie": [[d.strftime("%Y-%m"), round(float(v), 2)] for d, v in serie.items()],
            "metriche": {
                "cagr": round(cagr(serie), 4),
                "volatilita": round(volatilita_annualizzata(serie), 4),
                "max_drawdown": round(max_drawdown(serie), 4),
                "peggior_anno": round(peggior_anno(serie), 4),
            },
        }
        (USCITA / f"{p['slug']}.json").write_text(
            json.dumps(risultato, indent=1), encoding="utf-8"
        )
        m = risultato["metriche"]
        print(
            f"{p['slug']}: CAGR {m['cagr']:.2%}, vol {m['volatilita']:.2%}, "
            f"maxDD {m['max_drawdown']:.2%}, finestra {risultato['finestra'][0]} -> {risultato['finestra'][1]}"
        )


if __name__ == "__main__":
    main()
