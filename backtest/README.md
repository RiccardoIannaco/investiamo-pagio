# Backtest: come rigenerare i dati

Chiunque del gruppo può aggiornare i numeri della dashboard:

1. `pip install -r backtest/requirements.txt` (una volta sola)
2. `python backtest/run_backtest.py` (dalla radice del repo)
3. commit di `backtest/dati_grezzi/` e `dati/backtest/`; al push il sito si aggiorna

`--offline` ricalcola senza scaricare (usa i CSV committati).

## Metodologia (e limiti, onestamente)

- Gli ETF UCITS reali hanno pochi anni di storia: usiamo proxy USA con
  dividendi reinvestiti (Adj Close): VT (azioni globali), TLT (bond lunghi),
  SHY (bond brevi), BND (aggregate), GLD (oro), DBC (commodities).
- Conversione in EUR col cambio EURUSD di Yahoo Finance.
- Serie mensili, ribilanciamento al primo mese dell'anno, niente costi,
  tasse o TER: i numeri servono a CONFRONTARE i portafogli, non a prevedere.
- La finestra parte da giugno 2008 (nascita di VT): include la coda della
  crisi 2008, il 2011, il 2020 e il 2022, ma non l'intero crollo Lehman.
- I test dei calcoli: `python -m pytest backtest/tests -q`
