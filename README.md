# Investiamo Pagio

Second brain di finanza personale del gruppo: fonti riassunte, catalogo
ETF, portafogli modello con backtest, strumenti. Sito statico su GitHub
Pages, contenuti in markdown.

**Vuoi solo aggiungere una fonte o un articolo?** Leggi
[CONTRIBUIRE.md](CONTRIBUIRE.md): si fa dal browser, senza programmare.

## Per chi sviluppa

- `npm install && npm run dev` — sviluppo locale (http://localhost:4321/investiamo-pagio)
- `npm run build` — build completa con indice di ricerca
- `python backtest/run_backtest.py` — rigenera i dati della dashboard
  (vedi [backtest/README.md](backtest/README.md))
- Identità visiva e mappa del progetto: [DESIGN.md](DESIGN.md)
- Guida per LLM: [CLAUDE.md](CLAUDE.md) · Spec e piani: `docs/superpowers/`

## Convenzioni

Micro-commit, un branch per feature (`feat/…`, `docs/…`, `fix/…`,
`contenuti/…`), merge in `main` con `--no-ff`. `main` deve sempre
buildare: è il branch pubblicato.

## Pubblicazione (prima volta)

1. Crea il repo `investiamo-pagio` su GitHub (pubblico).
2. `git remote add origin https://github.com/<utente>/investiamo-pagio.git`
3. `git push -u origin main` (e poi `git push origin --all` per i branch)
4. Su GitHub: **Settings → Pages → Source: GitHub Actions**.
5. Al push successivo il sito esce su `https://<utente>.github.io/investiamo-pagio`.
