"""Funzioni pure di calcolo per i backtest.

Tutte le serie sono mensili: pandas.Series di valori con DatetimeIndex.
I rendimenti sono frazioni decimali (0.067 = 6,7%).
"""
import pandas as pd


def cagr(valori: pd.Series) -> float:
    mesi = len(valori) - 1
    return float((valori.iloc[-1] / valori.iloc[0]) ** (12 / mesi) - 1)


def volatilita_annualizzata(valori: pd.Series) -> float:
    return float(valori.pct_change().dropna().std(ddof=0) * (12**0.5))


def max_drawdown(valori: pd.Series) -> float:
    return float((valori / valori.cummax() - 1).min())


def peggior_anno(valori: pd.Series) -> float:
    annuali = valori.resample("YE").last()
    return float(annuali.pct_change().dropna().min())


def simula_portafoglio(
    prezzi: pd.DataFrame, pesi: dict[str, float], capitale: float = 10_000.0
) -> pd.Series:
    """Equity line con ribilanciamento al primo mese di ogni anno.

    prezzi: colonne = ticker proxy, righe mensili, senza NaN.
    pesi: {ticker: peso}; la somma deve fare 1 (validata a monte).
    """
    quote = {t: capitale * p / prezzi[t].iloc[0] for t, p in pesi.items()}
    anno = prezzi.index[0].year
    valori = []
    for data, riga in prezzi.iterrows():
        valore = sum(quote[t] * riga[t] for t in pesi)
        if data.year != anno:
            anno = data.year
            quote = {t: valore * p / riga[t] for t, p in pesi.items()}
        valori.append(valore)
    return pd.Series(valori, index=prezzi.index)
