# DESIGN.md — Identità visiva e mappa del progetto

> **Per LLM e umani che riprendono il lavoro:** questo file è la fonte di verità sul design
> e su *dove sta cosa e perché*. Aggiornalo ogni volta che una decisione di design cambia.
> La spec funzionale completa è in `docs/superpowers/specs/2026-07-03-investiamo-pagio-sito-design.md`.

## Stato del progetto (aggiornato 2026-07-03)

| Fase | Stato |
|---|---|
| Analisi export Notion "Wall Street Hub" | ✅ fatta (zip in radice, estratto in temp) |
| Decisioni con l'utente (stack, struttura, estetica, nome) | ✅ prese, verbale nella spec §2 |
| Mockup visivo | ✅ approvato dall'utente |
| Spec | ✅ scritta e committata |
| Piano di implementazione | ⏳ prossimo passo |
| Implementazione sito | ⛔ non iniziata |

## Dove sta cosa (e perché)

| Percorso | Cosa contiene | Perché sta lì |
|---|---|---|
| `docs/superpowers/specs/2026-07-03-investiamo-pagio-sito-design.md` | Spec completa approvata | Convenzione superpowers; leggila PRIMA di toccare qualsiasi cosa |
| `docs/superpowers/specs/assets/mockup-investiamo-pagio.html` | Mockup HTML approvato (4 viste: home, scheda fonte, tabella ETF, dashboard) | È il riferimento visivo vincolante: l'implementazione deve somigliare a questo |
| `IDEE.md` | Idee del gruppo + promemoria materiali da fornire | L'utente lo aggiorna a mano; la futura pagina "Lavagna" lo renderà |
| `paper/paper.bib` | Bibliografia dei 19 paper accademici | Da qui si generano le schede fonte `tipo: paper` (link DOI/SSRN, MAI i PDF) |
| `paper/files/` | PDF dei paper — **gitignored** | Copyright degli editori: non devono finire nel repo pubblico |
| `notion_investiamo_pagio.zip` | Export Notion originale — **gitignored** | Contiene PDF con copyright; è la materia prima della migrazione |
| `drive-locale/` (futura) | Excel e simulazioni scaricate da Drive — **gitignored** | Materiale privato del gruppo: sul sito solo link Drive |

La struttura futura del repo (cartelle `contenuti/`, `dati/`, `backtest/`, `src/`, `template/`) è definita nella spec §4. Regola chiave: **le cartelle che toccano i non-programmatori hanno nomi italiani e stanno alla radice**; `src/` è solo per chi sviluppa.

## Identità visiva ("editoriale / rivista")

Scelta dall'utente tra tre direzioni proposte. Intento: "qui si legge roba seria ma accessibile" — l'opposto del look AI generico (NIENTE gradienti, ombre, card arrotondate ovunque, hero giganti, emoji a pioggia).

### Token colore

| Token | Light | Dark | Uso |
|---|---|---|---|
| `--bg` | `#FBF8F1` (avorio) | `#171511` | fondo pagina |
| `--bg-raise` | `#F4EFE3` | `#201D17` | pannelli (es. riquadro grafico) |
| `--ink` | `#1E1C17` | `#E8E3D6` | testo |
| `--muted` | `#6E695D` | `#9B9587` | testo secondario, meta |
| `--accent` | `#1E5C3F` (verde bottiglia) | `#7FBD98` | link, tag, elementi attivi — **unica tinta di accento** |
| `--accent-soft` | `#E3EDE6` | `#22322A` | sfondo dei badge tipo-fonte |
| `--hairline` | `#E2DCCC` | `#322F27` | righe sottili di tabelle e divisori |

Serie categorica per i grafici multi-linea (oltre all'accento): ocra `#B0813C`, viola spento `#7A6FA8`, rosso mattone `#A85454`. Il neutro ha bias caldo (verso l'avorio), mai grigio puro.

Dark mode: token ridefiniti sotto `[data-theme="dark"]`; toggle manuale + default da `prefers-color-scheme`. Mai stili hard-coded fuori dai token.

### Tipografia

| Ruolo | Font | Note |
|---|---|---|
| Titoli (h1-h3, brand) | **Source Serif 4** (self-hosted `@fontsource-variable/source-serif-4`); fallback Georgia | serif = voce editoriale; `letter-spacing` leggermente negativo sui titoli grandi |
| Corpo | stack di sistema sans (`-apple-system, "Segoe UI", Roboto…`) | leggibilità e zero font da scaricare |
| Dati (ISIN, ticker, date, numeri, percorsi) | stack monospace di sistema (`Cascadia Code, Consolas…`) | i codici si riconoscono e si copiano a colpo d'occhio; `tabular-nums` sulle colonne numeriche |
| Etichette/nav | sans maiuscolo, `letter-spacing: .04–.14em`, corpo ridotto | gerarchia senza pesi extra |

Base 17px, riga ~1.65. Colonna di lettura ~42rem; pagine dati fino a ~56rem.

### Componenti chiave (come da mockup)

- **Header**: nome in serif + nav testuale maiuscola + ricerca + toggle ◐. Niente logo grafico.
- **Indice di rivista** (home): lista numerata `01/02/…` in monospace, nome sezione serif, descrizione muted. La numerazione è legittima: è un ordine di lettura consigliato.
- **Badge tipo-fonte**: rettangolino `--accent-soft`/`--accent`, maiuscolo piccolo (podcast, video, libro, paper, corso, sito).
- **Tabelle**: testata maiuscoletto muted con bordo inferiore netto (`--ink`), righe con hairline, ISIN monospace + bottone copia ⧉, colonna note in muted. Sempre dentro un contenitore `overflow-x: auto`.
- **Grafico dashboard**: SVG inline generato a build time, scala logaritmica, griglia tratteggiata su hairline, legenda testuale con trattino colorato. Dentro pannello `--bg-raise` con bordo hairline. Disclaimer in corsivo muted sotto.
- **Meta-fonte**: riga orizzontale di coppie `label bold + valore` tra due hairline.

### Anti-pattern vietati

Gradienti viola/blu, ombre portate, `border-radius` generosi, hero full-screen, emoji come marcatori di sezione, card con barra colorata laterale, animazioni decorative, font Inter/Space Grotesk come display, tutto-centrato.

## Verifica visiva (come osservare ciò che fai)

Ogni modifica visiva va verificata con screenshot headless, entrambi i temi:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu `
  --screenshot="out.png" --window-size=1280,3400 --hide-scrollbars "file:///C:/percorso/pagina.html"
```

Per il tema scuro senza toggle: copia temporanea del file forzando `data-theme="dark"` (o emulazione media query). Guardare davvero l'immagine, non fidarsi del codice. Verifica fatta sul mockup il 2026-07-03: entrambi i temi ok.

## Diario di lavorazione pubblico

L'avanzamento è pubblicato come Artifact su claude.ai (URL stabile, si aggiorna ricaricando):
il link è condiviso nella conversazione con l'utente e va riproposto qui quando disponibile.

## Rationale delle scelte principali (sintesi)

- **Astro**: design 100% custom (requisito "minimal non-AI"), collections con validazione dei frontmatter → errori chiari per i contributor, ecosistema open source molto attivo.
- **Fonte = scheda unica**: un file per fonte evita di mantenere sincronizzati catalogo e riassunti.
- **SVG a build time per i grafici**: niente librerie JS runtime, tema-aware, coerente col minimal.
- **CSV grezzi committati**: build deterministica, il sito non dipende da API esterne al momento del deploy.
- **Solo link per i PDF**: evita ridistribuzione di materiale protetto (decisione utente, spec §2).
