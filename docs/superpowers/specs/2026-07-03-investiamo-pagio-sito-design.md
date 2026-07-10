# Investiamo Pagio: design del sito

**Data:** 2026-07-03 · **Stato:** approvato dall'utente (mockup incluso)

## 1. Obiettivo

Sostituire e ampliare il Notion "Wall Street Hub" con un sito statico pubblico su GitHub Pages: un second brain di gruppo sulla finanza personale che aggrega fonti (video, podcast, libri, paper), le riassume in modo pratico, cataloga ETF e portafogli modello con backtest fatti in casa, e raccoglie strumenti utili. Deve essere modificabile da persone con basi di programmazione quasi nulle tramite la sola interfaccia web di GitHub.

## 2. Decisioni prese (con l'utente)

| Tema | Decisione |
|---|---|
| Nome sito e repo | **Investiamo Pagio** / `investiamo-pagio` |
| Lingua | Italiano (contenuti e interfaccia) |
| Stack | **Astro 5** + **Pagefind** (ricerca) + GitHub Actions → GitHub Pages |
| Contributi | Interfaccia web di GitHub + template + guida con screenshot; collaborator committano direttamente su `main` |
| Fonti e riassunti | **Unificati**: ogni fonte è un solo file markdown (metadati + riassunto) |
| Estetica | **Editoriale/rivista**: serif per i titoli, avorio/quasi-nero, un accento verde bottiglia, dark mode |
| Copyright | Paper e fonti pubbliche → **solo link** all'originale (DOI/SSRN); materiale su Drive → link ad accesso privato; PDF/zip locali in `.gitignore`; contenuto testuale del Notion pubblicabile |
| Dashboard backtest | **Inclusa in v1**, con script Python nel repo |

## 3. Architettura

- **Astro 5** (Node ≥ 20). Contenuti markdown caricati con il Content Layer (`glob` loader) da cartelle italiane a livello radice, con schema **zod** che valida i metadati: errore di build chiaro se un contributor sbaglia un campo.
- **Pagefind** per la ricerca full-text client-side, indicizzato dopo la build.
- **GitHub Actions**: workflow su push a `main` → build → deploy su GitHub Pages. Se la build fallisce, il sito resta all'ultima versione buona.
- URL: `https://<owner>.github.io/investiamo-pagio` → in `astro.config.mjs` vanno impostati `site` e `base: '/investiamo-pagio'`; tutti i link interni usano il base path (gotcha classico di GitHub Pages).
- Nessun backend, database, servizio a pagamento, analytics o cookie.

## 4. Struttura del repo

```
investiamo-pagio/
├── contenuti/
│   ├── fonti/              # una scheda .md per fonte
│   ├── articoli/           # articoli originali del gruppo
│   └── lavagna/            # note libere (to-do, domande aperte)
├── dati/
│   ├── etf.yaml            # catalogo ETF per categoria
│   ├── portafogli/         # un .yaml per lazy portfolio
│   └── backtest/           # output JSON degli script Python (committati)
├── backtest/
│   ├── run_backtest.py     # entrypoint
│   ├── metriche.py         # funzioni pure di calcolo (testate)
│   ├── dati_grezzi/        # CSV scaricati, committati (rigenerazione deterministica)
│   ├── tests/
│   ├── requirements.txt
│   └── README.md           # come rigenerare i dati
├── src/                    # layout, componenti, pagine Astro (solo per i "tecnici")
├── template/
│   ├── template-fonte.md
│   └── template-articolo.md
├── docs/superpowers/       # spec e piani
├── .github/workflows/deploy.yml
├── CONTRIBUIRE.md
├── IDEE.md                 # idee e promemoria del gruppo (già esistente)
├── paper/                  # paper.bib tracciato; paper/files/ in .gitignore
└── drive-locale/           # Excel/simulazioni scaricati da Drive → .gitignore
```

`.gitignore` include: `paper/files/`, `notion_investiamo_pagio.zip`, `drive-locale/`, `node_modules/`, `dist/`, cache Python.

## 5. Modello dei contenuti

### Scheda fonte (`contenuti/fonti/*.md`)

```yaml
---
titolo: "The Bull: podcast settimanale"
tipo: podcast            # video | podcast | libro | paper | corso | sito
autore: "Riccardo Spada" # opzionale
link: "https://open.spotify.com/show/..."
linkAlternativi:         # opzionale
  - etichetta: "YouTube"
    url: "https://youtube.com/..."
stato: riassunto         # solo-link | in-lavorazione | riassunto (default: solo-link)
tag: [etf, principianti] # opzionale
aggiunta: 2026-07-03     # opzionale, per "Ultime aggiunte"
---
Corpo markdown: concetti principali da portarsi a casa, note pratiche.
```

- Il catalogo `/fonti` si genera automaticamente, filtrabile per tipo e tag.
- Fonti `solo-link` → scheda compatta nel catalogo (nessuna pagina propria); `in-lavorazione` e `riassunto` → pagina dedicata.
- I 19 paper accademici vengono generati una tantum da `paper/paper.bib` (titolo, autori, anno, rivista, link DOI/URL), `tipo: paper`, senza PDF.

### Articolo (`contenuti/articoli/*.md`)

```yaml
---
titolo: "ETF obbligazionari vs obbligazioni singole"
autore: "Nome Cognome"
data: 2026-07-03
tag: [obbligazioni]
bozza: false             # true = non pubblicato
---
```

### Catalogo ETF (`dati/etf.yaml`)

Ampliato su richiesta dell'utente (2026-07-04): più ETF per categoria, TER indicativi
(con data di aggiornamento e nota "verifica su JustETF") e **label** per cercare per
caratteristica (value, growth, world, small-cap, attivo, oro, crypto, commodities,
managed-futures, leva, obbligazioni…). La pagina ETF filtra per label e per testo.

```yaml
aggiornato: "2026-07-04"
categorie:
  - id: azionario-mondo
    nome: "Azionario mondo"
    nota: "FTSE All World e MSCI ACWI comprendono gli emergenti, MSCI World no…"
    etf:
      - nome: "Vanguard FTSE All-World UCITS ETF Acc"
        isin: IE00BK5BQT80
        ticker: VWCE
        ter: 0.22           # percento annuo, indicativo
        label: [azionario, world]
        note: "Comprende gli emergenti; domicilio irlandese"
        justetf: "https://www.justetf.com/it/etf-profile.html?isin=IE00BK5BQT80"
```

### Portafoglio (`dati/portafogli/*.yaml`)

```yaml
nome: "Golden Butterfly The Bull"
slug: golden-butterfly-the-bull
descrizione: "Adattamento europeo del Golden Butterfly proposto da The Bull…"
ribilanciamento: annuale
allocazioni:
  - asset: "Azionario globale"
    peso: 0.45
    proxy: "^990100-USD-STRD"    # ticker/serie usata nel backtest
    etf_reale: { nome: "Vanguard FTSE All-World UCITS ETF Acc", isin: IE00BK5BQT80, ticker: VWCE }
```

### Output backtest (`dati/backtest/<slug>.json`)

```json
{
  "portafoglio": "golden-butterfly-the-bull",
  "aggiornato": "2026-06-30",
  "valuta": "EUR",
  "finestra": ["2008-07", "2026-06"],
  "serie": [["2008-07", 10000], ["2008-08", 10034]],
  "metriche": { "cagr": 0.067, "volatilita": 0.079, "max_drawdown": -0.19, "peggior_anno": -0.12 }
}
```

## 6. Mappa del sito e migrazione dal Notion

| Pagina | Contenuto | Origine |
|---|---|---|
| Home | Indice "da rivista" + ultime aggiunte (dalle date `aggiunta`/`data`) | nuovo |
| Inizia qui | Percorso ordinato per principianti con rimandi alle fonti | nuovo |
| Fonti | Catalogo filtrabile + pagine scheda | homepage Notion + `paper.bib` |
| ETF | Tabelle per categoria, ISIN copiabile con un click, link JustETF | pagina "ETF Selezionati" |
| Portafogli | Una pagina per portafoglio + **Dashboard confronto** | "Golden Butterfly The Bull" + sezione lazy portfolio |
| Strumenti | Link commentati: fogli, calcolatori, Curvo, trackingdifferences, IPS, NotebookLM | "HUB utilities" + homepage Notion |
| Articoli | Elenco per data + pagine articolo | nuovo + "Confronto emittenti" come primo articolo |
| Lavagna | Rende `IDEE.md` + `contenuti/lavagna/*.md` | "To do" + "Open Questions" + IDEE.md |
| Come contribuire | Versione web di CONTRIBUIRE.md | nuovo |
| 404 | Pagina di cortesia in tema | nuovo |

**Caso copyright deciso:** la pagina "Confronto emittenti" migra **solo come testo**; gli screenshot delle slide del videocorso a pagamento di Lazzaro restano fuori dal repo (al loro posto un link al Drive privato del gruppo). I 3 PDF del Notion (dispensa Educati e Finanziati, guida Omney, slide) → schede fonte con link al Drive privato, nessun PDF nel repo.

## 7. Design visivo (approvato via mockup)

Riferimento: `docs/superpowers/specs/assets/mockup-investiamo-pagio.html` (mockup approvato dall'utente).

- **Tipografia:** titoli in **Source Serif 4** (self-hosted via `@fontsource-variable/source-serif-4`); corpo in stack di sistema sans (`-apple-system, "Segoe UI", Roboto…`); ISIN/ticker/numeri in stack monospace di sistema.
- **Colori (light):** fondo avorio `#FBF8F1`, testo `#1E1C17`, accento verde bottiglia `#1E5C3F`, righe sottili `#E2DCCC`. **(dark):** fondo `#171511`, testo `#E8E3D6`, accento `#7FBD98`, righe `#322F27`. Toggle manuale + rispetto di `prefers-color-scheme`.
- **Layout:** colonna di lettura ~42rem, pagine dati fino a ~56rem; header essenziale (nome + nav testuale + ricerca + toggle); nessuna ombra/gradienta/hero; homepage a indice numerato; tabelle con testate maiuscoletto e righe sottili.
- **Accessibilità:** contrasto AA, stati di focus visibili, tabelle scorrevoli in orizzontale su mobile dentro contenitori `overflow-x: auto`.

## 8. Dashboard e backtest Python

- **Portafogli al lancio (4):** Golden Butterfly The Bull, All Weather EU, LifeStrategy 60, 100% azionario globale.
- **Dati:** gli ETF UCITS reali hanno storia breve → si usano **indici sottostanti o proxy** con storia lunga (scaricati con `yfinance`; in mancanza, serie pubbliche equivalenti). I CSV grezzi vengono **committati** in `backtest/dati_grezzi/`: la build del sito non scarica nulla e chiunque può rigenerare offline.
- **Calcoli:** serie mensili, ribilanciamento annuale, equity line da 10.000 €, metriche: CAGR, volatilità annualizzata, max drawdown, peggior anno solare. Funzioni pure in `metriche.py`, testate con `pytest` su serie sintetiche dal risultato noto a mano.
- **Flusso di aggiornamento (documentato in `backtest/README.md`):** `pip install -r requirements.txt` → `python run_backtest.py` (scarica/aggiorna CSV, riscrive i JSON in `dati/backtest/` con data) → commit → il sito si aggiorna.
- **Resa grafica:** la pagina Dashboard legge i JSON a build time; l'equity line è un componente Astro che genera **SVG inline** (scala logaritmica, si adatta a light/dark, zero librerie JS runtime) + tabella metriche comparata + **disclaimer visibile** ("backtest su indici proxy, non è un consiglio d'investimento") + data di aggiornamento.
- Gli script falliscono con messaggio chiaro se un YAML portafoglio ha pesi che non sommano a 1 o proxy mancante.

## 9. Contribuzione per non-programmatori

- `CONTRIBUIRE.md` + pagina "Come contribuire": passo-passo con screenshot (account GitHub → invito come collaborator → `Add file` → copia template → compila → `Commit changes` → dopo ~2 minuti online). Include "se la build fallisce: cosa vuol dire, chi pingare".
- Template in `template/` con tutti i campi precompilati e commentati.
- Modello di fiducia: gruppo piccolo, commit diretti su `main`, nessuna PR obbligatoria.

## 10. Testing e qualità

- CI su ogni push/PR: `astro build`; la validazione zod dei frontmatter avviene qui e una build fallita non viene pubblicata.
- `pytest` per `backtest/metriche.py` (stessa CI, job separato che gira solo se cambia `backtest/`).
- Verifica manuale prima del lancio: navigazione completa, ricerca, dark mode, mobile.

## 11. Fuori scope v1 (esplicitamente)

- CMS grafico (Pages CMS/Decap): aggiungibile in seguito sopra lo stesso repo.
- Commenti, newsletter, analytics, multi-lingua.
- Trascrizioni automatiche dei video (i riassunti arriveranno come contenuti, non come feature).
- Backtest con dati ETF reali a livello di NAV o simulazioni fiscali.

## 12. Materiale atteso dall'utente (promemoria, anche in IDEE.md)

- Lista dei video di cui vuole trascrizioni e riassunti con i concetti chiave per autore → diventeranno schede fonte.
- Download locale dei fogli Excel e delle simulazioni Python dal Drive → `drive-locale/` (gitignored), sul sito solo i link privati.
