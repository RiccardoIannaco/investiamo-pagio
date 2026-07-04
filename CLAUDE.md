# CLAUDE.md — Investiamo Pagio

> Punto d'ingresso per LLM e umani. Leggilo per intero prima di toccare qualsiasi cosa.
> **Mantienilo aggiornato**: a ogni milestone aggiorna la sezione "Stato" e, se cambia
> una decisione, il documento che la contiene (non questo file: qui solo puntatori e stato).

## Cos'è questo progetto

Sito statico su GitHub Pages che sostituisce il Notion "Wall Street Hub" di un gruppo di
amici: second brain di **finanza personale in italiano** — fonti (video/podcast/libri/paper)
con riassunti pratici, catalogo ETF curato con TER e label, portafogli modello con backtest
Python fatti in casa, strumenti, articoli. I contributor NON sono programmatori: editano
markdown dalla web UI di GitHub.

Diario di lavorazione pubblico (aggiornalo a ogni avanzamento, stesso URL):
https://claude.ai/code/artifact/cf28bf25-076c-4157-a8d5-e1d4e7571faa
(sorgente nello scratchpad di sessione: `diario-investiamo-pagio.html`)

## Ordine di lettura (obbligatorio prima di implementare)

1. `DESIGN.md` — identità visiva (token colore, tipografia), mappa "dove sta cosa e perché",
   convenzioni git, comando per la verifica visiva con screenshot.
2. `docs/superpowers/specs/2026-07-03-investiamo-pagio-sito-design.md` — la spec approvata.
3. `docs/superpowers/plans/2026-07-04-sito-investiamo-pagio.md` — il piano: 12 task con
   codice completo per ogni step. **L'implementazione segue il piano, non l'improvvisazione.**
4. `.superpowers/sdd/progress.md` — il ledger di avanzamento: i task lì marcati completi
   sono FATTI, non ri-eseguirli (fidati del ledger e di `git log`, non della memoria).

## Stato (aggiornato 2026-07-05, TUTTI i 12 task implementati)

**Fatto:**
- Analisi Notion, decisioni, mockup approvato, spec + piano committati.
- **Sito completo**: 16 pagine buildano (`npm run build`), pytest 6/6, tutte le sezioni
  attive (home, inizia-qui, fonti con 29 schede, ETF con label/TER, dashboard con backtest
  reali 2008-2026, strumenti, articoli, lavagna, cerca, come-contribuire, 404).
  Ledger dettagliato in `.superpowers/sdd/progress.md`.
- Task 1 eseguito da subagente con review pulita; Task 2-12 eseguiti inline (limiti
  subagenti) con build + verifica visiva screenshot per ogni task.
- Catalogo ETF: 14/22 categorie verificate sul web (justETF, lug 2026).

**In corso / da fare:**
- Workflow `etf-catalogo-ricerca` (run `wf_19264f2b-257`): ultime 8 categorie (america,
  fattoriali, lifestrategy, obbligazionari-a-scadenza, crypto, managed-futures,
  quantistici, compensazione-minusvalenze) → fondere i risultati in `dati/etf.yaml`
  E in `docs/superpowers/plans/assets/etf.yaml` (stesso formato delle categorie fatte).
- Review finale whole-branch con subagenti (i task 2-12 non hanno avuto review individuale:
  recuperare con una review complessiva; finding minor noti nel ledger).
- L'utente: crea il repo GitHub `investiamo-pagio`, push, attiva Pages (README §Pubblicazione).
- Contenuti attesi dall'utente (promemoria in `IDEE.md`): lista video per i riassunti;
  Excel e simulazioni dal Drive → `drive-locale/` (gitignored); screenshot per la guida.

## Struttura della codebase

Oggi (pre-implementazione): solo documentazione + asset.

```
CLAUDE.md, DESIGN.md, IDEE.md          ← guida LLM, design, idee del gruppo
docs/superpowers/specs/                ← spec + mockup approvato
docs/superpowers/plans/                ← piano 12 task + assets/ (contenuti pronti da copiare)
paper/paper.bib                        ← bibliografia (i PDF in paper/files/ sono GITIGNORED)
notion_investiamo_pagio.zip            ← export originale (GITIGNORED)
```

Dopo il piano (mappa completa nel piano, sezione "Mappa dei file"):

```
contenuti/{fonti,articoli,lavagna}/    ← markdown dei contributor (nomi italiani, radice)
dati/{etf.yaml,strumenti.yaml,portafogli/,backtest/}
backtest/                              ← script Python + test + CSV grezzi committati
src/                                   ← Astro 5: layouts, pages, components, lib (solo tecnici)
template/                              ← template-fonte.md, template-articolo.md
.github/workflows/deploy.yml           ← pytest + build + deploy Pages
```

## Convenzioni vincolanti (violarle = review respinta)

- **Git**: un branch per feature (`feat/…`, `docs/…`, `fix/…`, `contenuti/…`), micro-commit,
  merge in `main` SOLO con `--no-ff`, branch mai cancellati, `main` deve sempre buildare.
- **Copyright**: MAI PDF o materiale protetto nel repo pubblico. Paper → link DOI/SSRN.
  Materiale del gruppo → link Drive privato. `paper/files/`, lo zip Notion e `drive-locale/`
  restano in `.gitignore`.
- **Design**: solo i token di `DESIGN.md`; tema chiaro E scuro; niente gradienti/ombre/hero;
  il mockup è il riferimento vincolante. Ogni modifica visiva va GUARDATA via screenshot
  headless in entrambi i temi (comando in DESIGN.md), non solo compilata.
- **Base path**: il sito vive sotto `/investiamo-pagio` — link interni SOLO via `href()`
  di `src/lib/percorsi.ts`.
- **Lingua**: tutto in italiano (UI, contenuti, commit, note).
- **Niente consigli d'investimento**: disclaimer visibile sulle pagine dati.

## Come lavorare (tecniche che qui funzionano)

- **Un task alla volta, dal piano**: apri il task N del piano, crea il branch indicato,
  esegui gli step nell'ordine (test prima del codice dove previsto), committa a ogni step,
  merge `--no-ff`, aggiorna ledger e todo. Non anticipare task futuri (YAGNI).
- **Ai subagenti passa file, non prose**: brief del task via `scripts/task-brief`, diff di
  review via `scripts/review-package BASE HEAD` (skill subagent-driven-development);
  registra il commit BASE prima di dispatchare.
- **Verifica = evidenza**: mai dichiarare "fatto" senza l'output del comando (build, pytest,
  screenshot). Se un test fallisce, riportalo com'è.
- **Dati fattuali (ISIN, TER)**: mai dalla memoria del modello — verifica su justETF/web;
  in `dati/etf.yaml` la data `aggiornato` va tenuta vera.
- **Windows**: shell PowerShell 5.1 (niente `&&`; vedi note del tool). I path lunghi
  rompono Expand-Archive: usa `tar -xf` verso path corti.

## Limiti noti della sessione

- I limiti di utilizzo (subagenti) si esauriscono a ondate: i workflow vanno ripresi con
  `resumeFromRunId` (i risultati completati sono in cache nel journal del workflow).
- Il journal dei workflow è in
  `~/.claude/projects/<progetto>/<sessione>/subagents/workflows/<runId>/journal.jsonl`
  (campo `result`, una riga per agente completato).
