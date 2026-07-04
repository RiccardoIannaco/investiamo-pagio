# Sito Investiamo Pagio — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sito statico su GitHub Pages che sostituisce il Notion "Wall Street Hub": second brain di finanza personale con fonti riassunte, catalogo ETF filtrabile, portafogli modello con backtest Python e guida contributi per non-programmatori.

**Architecture:** Astro 5 genera il sito da markdown (cartelle italiane alla radice, schemi zod che validano i metadati) e da YAML/JSON in `dati/`; gli script Python in `backtest/` producono i JSON dei backtest committati nel repo; GitHub Actions builda e pubblica su Pages a ogni push su `main`.

**Tech Stack:** Astro ^5, zod, js-yaml, @fontsource-variable/source-serif-4, Pagefind (ricerca), Python 3.12 (pandas ≥2.2, yfinance, PyYAML, pytest), GitHub Actions + GitHub Pages.

**Spec di riferimento:** `docs/superpowers/specs/2026-07-03-investiamo-pagio-sito-design.md` · **Identità visiva:** `DESIGN.md` (radice) · **Mockup vincolante:** `docs/superpowers/specs/assets/mockup-investiamo-pagio.html` · **Asset di migrazione:** `docs/superpowers/plans/assets/`

## Global Constraints

- Node ≥ 20, Astro ^5 (Content Layer / loader `glob`), Python ≥ 3.12.
- Cartelle toccate dai contributor in italiano e alla radice: `contenuti/`, `dati/`, `template/`. `src/` è solo dei tecnici.
- Convenzioni git (da `DESIGN.md`, richieste dall'utente): **un branch per task** (nome indicato in ogni task), **micro-commit** a ogni step di commit, **merge in `main` con `--no-ff`**, branch mai cancellati. `main` deve sempre buildare.
- Copyright: MAI PDF nel repo pubblico. `paper/files/`, `notion_investiamo_pagio.zip`, `drive-locale/` restano in `.gitignore`. I paper si linkano a DOI/SSRN; il materiale Drive si linka con nota "accesso privato".
- Design: SOLO i token di `DESIGN.md` (avorio `#FBF8F1`/`#171511`, accento `#1E5C3F`/`#7FBD98`, serif Source Serif 4 per i titoli). Vietati: gradienti, ombre, border-radius generosi, hero, emoji come marcatori, Inter/Space Grotesk. Tema chiaro E scuro sempre.
- Base path GitHub Pages: il sito vive sotto `/investiamo-pagio`; ogni link interno passa da `href()` di `src/lib/percorsi.ts` (Task 2). Mai `href="/pagina"` hard-coded.
- Niente librerie JS runtime salvo Pagefind; i grafici sono SVG generati a build time.
- Tutti i testi dell'interfaccia in italiano.
- Verifica visiva: dopo ogni task che tocca l'aspetto, screenshot con Chrome headless in ENTRAMBI i temi (comando in `DESIGN.md`) e osservazione reale dell'immagine.
- I comandi shell nei task sono PowerShell-compatibili (ambiente Windows).

## Mappa dei file (chi crea cosa)

| Percorso | Responsabilità | Task |
|---|---|---|
| `package.json`, `astro.config.mjs`, `tsconfig.json` | scaffold e configurazione build | 1 |
| `src/styles/tokens.css` | design token + stili base | 2 |
| `src/lib/percorsi.ts` | helper `href()` per il base path | 2 |
| `src/layouts/Base.astro` | layout unico: head, header/nav, footer, tema | 2 |
| `src/content.config.ts` | collezioni `fonti`, `articoli`, `lavagna` (zod) | 3 |
| `template/template-fonte.md`, `template/template-articolo.md` | modelli da copiare per i contributor | 3 |
| `contenuti/fonti/*.md` | schede fonte (migrazione + paper generati) | 4 |
| `scripts/bib2fonti.py` | genera le schede paper da `paper/paper.bib` | 4 |
| `src/pages/fonti/index.astro`, `src/pages/fonti/[slug].astro` | catalogo filtrabile + pagina scheda | 4 |
| `dati/etf.yaml` | catalogo ETF (categorie, TER, label) | 5 |
| `src/lib/dati.ts` | loader + zod per YAML/JSON di `dati/` | 5 (esteso in 7, 8) |
| `src/pages/etf.astro` | tabelle ETF con filtro label e copia-ISIN | 5 |
| `backtest/metriche.py`, `backtest/tests/test_metriche.py` | calcoli puri, testati | 6 |
| `backtest/run_backtest.py`, `backtest/requirements.txt`, `backtest/README.md`, `backtest/dati_grezzi/*.csv` | pipeline dati → `dati/backtest/*.json` | 6 |
| `dati/portafogli/*.yaml` | definizione dei 4 portafogli | 6 |
| `src/components/GraficoLinee.astro` | grafico SVG a scala log, tema-aware | 7 |
| `src/pages/portafogli/index.astro` (dashboard), `src/pages/portafogli/[slug].astro` | confronto + pagine singole | 7 |
| `src/lib/formato.ts` | formattazione numeri/percentuali/date it-IT | 7 |
| `src/pages/index.astro`, `inizia-qui.astro`, `strumenti.astro`, `lavagna.astro`, `404.astro` | pagine statiche | 8 |
| `dati/strumenti.yaml` | link commentati della pagina Strumenti | 8 |
| `contenuti/articoli/*.md`, `src/pages/articoli/*` | sezione articoli | 9 |
| `src/pages/cerca.astro` | ricerca Pagefind | 10 |
| `CONTRIBUIRE.md`, `src/pages/come-contribuire.astro` | guida per non-programmatori | 11 |
| `.github/workflows/deploy.yml`, `README.md` | CI/CD e documentazione | 12 |

---

### Task 1: Scaffold Astro

**Branch:** `feat/scaffold-astro`

**Files:**
- Create: `package.json`
- Create: `astro.config.mjs`
- Create: `tsconfig.json`
- Create: `src/pages/index.astro` (segnaposto, sostituito nel Task 8)
- Modify: `.gitignore` (aggiunge artefatti Node/Astro se mancanti — già presenti: verifica soltanto)

**Interfaces:**
- Consumes: niente (primo task).
- Produces: comando `npm run build` che produce `dist/` e lancia Pagefind; `npm run dev`; config con `site`/`base` derivati da `GITHUB_REPOSITORY` (fallback locale `/investiamo-pagio`). Ogni task successivo assume che `npm run build` funzioni da radice repo.

- [ ] **Step 1: Verifica che la build fallisca (niente scaffold)**

Run: `npm run build`
Expected: errore `Could not read package.json` (o simile) — conferma che si parte da zero.

- [ ] **Step 2: Crea il branch e i file di scaffold**

```bash
git checkout main
git checkout -b feat/scaffold-astro
```

`package.json`:

```json
{
  "name": "investiamo-pagio",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "astro dev",
    "build": "astro build && pagefind --site dist",
    "preview": "astro preview"
  },
  "dependencies": {
    "@fontsource-variable/source-serif-4": "^5.2.5",
    "astro": "^5.16.0",
    "js-yaml": "^4.1.0",
    "zod": "^3.24.1"
  },
  "devDependencies": {
    "@types/js-yaml": "^4.0.9",
    "pagefind": "^1.3.0"
  }
}
```

`astro.config.mjs`:

```js
import { defineConfig } from 'astro/config';

// Su GitHub Actions GITHUB_REPOSITORY vale "proprietario/repo": site e base
// si adattano da soli al nome del repo. In locale si usa il fallback.
const [proprietario, repo] = (process.env.GITHUB_REPOSITORY ?? 'locale/investiamo-pagio').split('/');

export default defineConfig({
  site: `https://${proprietario}.github.io`,
  base: `/${repo}`,
});
```

`tsconfig.json`:

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "src/**/*"],
  "exclude": ["dist"]
}
```

`src/pages/index.astro`:

```astro
---
---
<!doctype html>
<html lang="it">
  <head><meta charset="utf-8" /><title>Investiamo Pagio</title></head>
  <body><p>Investiamo Pagio — in costruzione.</p></body>
</html>
```

- [ ] **Step 3: Installa e builda**

Run: `npm install`
Expected: installazione senza errori (lockfile creato).

Run: `npm run build`
Expected: `astro build` completa con `1 page(s) built`; Pagefind indicizza `dist` (`Indexed 1 page` circa). Esiste `dist/index.html`.

- [ ] **Step 4: Micro-commit e merge**

```bash
git add package.json package-lock.json astro.config.mjs tsconfig.json src/pages/index.astro
git commit -m "feat: scaffold Astro 5 con base path GitHub Pages e Pagefind in build"
git checkout main
git merge --no-ff feat/scaffold-astro -m "merge: feat/scaffold-astro"
```

---

### Task 2: Design base — token, layout, header, tema

**Branch:** `feat/design-base`

**Files:**
- Create: `src/styles/tokens.css`
- Create: `src/lib/percorsi.ts`
- Create: `src/layouts/Base.astro`
- Modify: `src/pages/index.astro` (usa il layout)

**Interfaces:**
- Consumes: scaffold del Task 1.
- Produces:
  - `href(percorso: string): string` da `src/lib/percorsi.ts` — antepone il base path; TUTTI i link interni dei task successivi lo usano.
  - `Base.astro` con props `{ titolo: string; descrizione?: string }` e uno `<slot />` dentro `<main class="colonna">`; chi ha bisogno della colonna larga usa `<main>` di default e aggiunge la classe `colonna-larga` a un proprio contenitore.
  - Classi CSS globali usate dai task successivi: `colonna`, `colonna-larga`, `kicker`, `badge`, `scorri`, `num`, `muted`, `hairline-top`, `indice`, `meta-riga`.

- [ ] **Step 1: Crea il branch**

```bash
git checkout -b feat/design-base
```

- [ ] **Step 2: Scrivi i token e gli stili base**

`src/styles/tokens.css`:

```css
:root {
  --bg: #FBF8F1; --bg-raise: #F4EFE3; --ink: #1E1C17; --muted: #6E695D;
  --accent: #1E5C3F; --accent-soft: #E3EDE6; --hairline: #E2DCCC;
  --mono: "Cascadia Code", Consolas, "SF Mono", Menlo, monospace;
  --serif: "Source Serif 4 Variable", Georgia, "Iowan Old Style", "Palatino Linotype", serif;
  --sans: -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
:root[data-theme="dark"] {
  --bg: #171511; --bg-raise: #201D17; --ink: #E8E3D6; --muted: #9B9587;
  --accent: #7FBD98; --accent-soft: #22322A; --hairline: #322F27;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --bg: #171511; --bg-raise: #201D17; --ink: #E8E3D6; --muted: #9B9587;
    --accent: #7FBD98; --accent-soft: #22322A; --hairline: #322F27;
  }
}

* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 17px; }
body {
  background: var(--bg); color: var(--ink);
  font-family: var(--sans); line-height: 1.65; -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
a:focus-visible, button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
h1, h2, h3 { font-family: var(--serif); font-weight: 700; letter-spacing: -0.01em; text-wrap: balance; }
h1 { font-size: 2.1rem; line-height: 1.15; margin-bottom: 1rem; }
h2 { font-size: 1.4rem; margin: 2.4rem 0 0.8rem; }
h3 { font-size: 1.1rem; margin: 1.6rem 0 0.5rem; }
p, ul, ol { margin-bottom: 0.9rem; }
main ul, main ol { padding-left: 1.2rem; }
li::marker { color: var(--accent); }

.colonna { max-width: 42rem; margin: 0 auto; padding: 2.6rem 1.4rem 5rem; }
.colonna-larga { max-width: 56rem; margin-left: auto; margin-right: auto; }
.kicker { font-size: .78rem; letter-spacing: .12em; text-transform: uppercase; color: var(--accent); margin-bottom: .8rem; }
.muted { color: var(--muted); }
.hairline-top { border-top: 1px solid var(--hairline); padding-top: 1rem; }
.badge {
  font-size: .68rem; letter-spacing: .08em; text-transform: uppercase;
  background: var(--accent-soft); color: var(--accent);
  padding: .1rem .5rem; border-radius: 2px; white-space: nowrap;
}
.num { font-family: var(--mono); font-size: .84rem; text-align: right; font-variant-numeric: tabular-nums; }
.scorri { overflow-x: auto; }

table { border-collapse: collapse; width: 100%; font-size: .88rem; margin-bottom: 1rem; }
th {
  font-size: .72rem; letter-spacing: .1em; text-transform: uppercase; color: var(--muted);
  font-weight: 600; text-align: left; padding: .5rem .9rem .5rem 0; border-bottom: 1px solid var(--ink);
}
td { padding: .6rem .9rem .6rem 0; border-bottom: 1px solid var(--hairline); vertical-align: top; }
code { font-family: var(--mono); font-size: .84em; background: var(--accent-soft); padding: .08em .35em; border-radius: 2px; }

.indice { list-style: none; counter-reset: sez; border-top: 1px solid var(--hairline); padding-left: 0 !important; }
.indice li { counter-increment: sez; border-bottom: 1px solid var(--hairline); padding: 1rem 0; display: flex; gap: 1.4rem; align-items: baseline; }
.indice li::before { content: counter(sez, decimal-leading-zero); font-family: var(--mono); font-size: .8rem; color: var(--muted); min-width: 1.6rem; }
.indice .nome { font-family: var(--serif); font-weight: 700; font-size: 1.05rem; min-width: 9.5rem; }
.indice .descr { color: var(--muted); font-size: .92rem; }

.meta-riga {
  display: flex; gap: 1.3rem; flex-wrap: wrap; font-size: .85rem; color: var(--muted);
  border-top: 1px solid var(--hairline); border-bottom: 1px solid var(--hairline);
  padding: .7rem 0; margin: 1.2rem 0 1.8rem; list-style: none; padding-left: 0 !important;
}
.meta-riga b { color: var(--ink); font-weight: 600; }

@media (prefers-reduced-motion: no-preference) {
  html { scroll-behavior: smooth; }
}
```

`src/lib/percorsi.ts`:

```ts
/** Antepone il base path di GitHub Pages: href('/fonti') → '/investiamo-pagio/fonti'. */
export function href(percorso: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return base + percorso;
}
```

- [ ] **Step 3: Scrivi il layout Base**

`src/layouts/Base.astro`:

```astro
---
import '@fontsource-variable/source-serif-4';
import '../styles/tokens.css';
import { href } from '../lib/percorsi';

interface Props { titolo: string; descrizione?: string }
const { titolo, descrizione = 'Second brain di finanza personale del gruppo.' } = Astro.props;

const voci = [
  ['Inizia qui', '/inizia-qui'],
  ['Fonti', '/fonti'],
  ['ETF', '/etf'],
  ['Portafogli', '/portafogli'],
  ['Strumenti', '/strumenti'],
  ['Articoli', '/articoli'],
  ['Lavagna', '/lavagna'],
  ['Cerca', '/cerca'],
] as const;
const percorsoAttuale = Astro.url.pathname;
---
<!doctype html>
<html lang="it">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content={descrizione} />
    <title>{titolo} · Investiamo Pagio</title>
    <script is:inline>
      const salvato = localStorage.getItem('tema');
      document.documentElement.dataset.theme =
        salvato ?? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    </script>
  </head>
  <body>
    <header>
      <a class="brand" href={href('/')}>Investiamo Pagio</a>
      <nav aria-label="principale">
        {voci.map(([nome, percorso]) => (
          <a href={href(percorso)} class:list={{ attiva: percorsoAttuale.startsWith(href(percorso)) }}>{nome}</a>
        ))}
      </nav>
      <button id="cambia-tema" title="Tema chiaro/scuro" aria-label="Cambia tema">◐</button>
    </header>
    <main class="colonna" data-pagefind-body>
      <slot />
    </main>
    <footer class="colonna muted">
      <p class="hairline-top">
        Second brain del gruppo, curato a mano. Niente qui è un consiglio d'investimento.
        · <a href={href('/come-contribuire')}>Come contribuire</a>
      </p>
    </footer>
    <script>
      document.getElementById('cambia-tema')?.addEventListener('click', () => {
        const nuovo = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
        document.documentElement.dataset.theme = nuovo;
        localStorage.setItem('tema', nuovo);
      });
    </script>
    <style>
      header {
        border-bottom: 1px solid var(--hairline);
        padding: 1.1rem 1.4rem;
        display: flex; align-items: baseline; gap: 1.6rem; flex-wrap: wrap;
        max-width: 60rem; margin: 0 auto;
      }
      .brand { font-family: var(--serif); font-weight: 700; font-size: 1.2rem; color: var(--ink); }
      nav { display: flex; gap: 1.1rem; flex-wrap: wrap; font-size: .8rem; letter-spacing: .05em; }
      nav a { color: var(--muted); text-transform: uppercase; }
      nav a.attiva { color: var(--accent); border-bottom: 2px solid var(--accent); padding-bottom: 2px; }
      #cambia-tema {
        margin-left: auto; background: none; border: 1px solid var(--hairline); border-radius: 3px;
        color: var(--muted); cursor: pointer; font-size: .85rem; padding: .1rem .5rem;
      }
      footer p { font-size: .8rem; }
    </style>
  </body>
</html>
```

- [ ] **Step 4: Aggiorna la home segnaposto per usare il layout**

`src/pages/index.astro`:

```astro
---
import Base from '../layouts/Base.astro';
---
<Base titolo="Home">
  <p class="kicker">Second brain di finanza personale</p>
  <h1>Le cose che avremmo voluto sapere prima.</h1>
  <p class="muted">Sito in costruzione: la home vera arriva col Task 8.</p>
</Base>
```

- [ ] **Step 5: Builda e verifica visivamente ENTRAMBI i temi**

Run: `npm run build`
Expected: build ok.

Run (dalla radice del repo):

```powershell
npm run preview -- --port 4321 &  # oppure in un secondo terminale
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu --screenshot="$env:TEMP\ip-light.png" --window-size=1280,900 --hide-scrollbars "http://localhost:4321/investiamo-pagio/"
```

Expected: screenshot con header (brand serif + nav maiuscola), fondo avorio, titolo serif. Poi ripeti lo screenshot dopo aver forzato il tema scuro (aggiungi temporaneamente `data-theme="dark"` sull'`<html>` di `dist/index.html` o usa il toggle in un browser vero): fondo `#171511`, testo avorio. GUARDA le immagini, non fidarti.

- [ ] **Step 6: Micro-commit e merge**

```bash
git add src/styles/tokens.css src/lib/percorsi.ts src/layouts/Base.astro src/pages/index.astro
git commit -m "feat: design token, layout Base con nav e tema chiaro/scuro"
git checkout main
git merge --no-ff feat/design-base -m "merge: feat/design-base"
```

---

### Task 3: Collezioni contenuti e template

**Branch:** `feat/collezioni-contenuti`

**Files:**
- Create: `src/content.config.ts`
- Create: `template/template-fonte.md`
- Create: `template/template-articolo.md`
- Create: `contenuti/fonti/.gitkeep`, `contenuti/articoli/.gitkeep`, `contenuti/lavagna/.gitkeep`

**Interfaces:**
- Consumes: scaffold Task 1.
- Produces: collezioni Astro `fonti`, `articoli`, `lavagna` interrogabili con `getCollection('fonti')` ecc. Campi (usati da Task 4, 8, 9):
  - `fonti`: `titolo: string`, `tipo: 'video'|'podcast'|'libro'|'paper'|'corso'|'sito'`, `autore?: string`, `link: string(url)`, `linkAlternativi: {etichetta: string, url: string}[]` (default `[]`), `stato: 'solo-link'|'in-lavorazione'|'riassunto'` (default `'solo-link'`), `tag: string[]` (default `[]`), `aggiunta?: Date`.
  - `articoli`: `titolo: string`, `autore: string`, `data: Date`, `tag: string[]` (default `[]`), `bozza: boolean` (default `false`).
  - `lavagna`: `titolo: string`.
  - Gli id delle entry sono i nomi file senza estensione (loader `glob`).

- [ ] **Step 1: Crea il branch**

```bash
git checkout -b feat/collezioni-contenuti
```

- [ ] **Step 2: Scrivi la configurazione delle collezioni**

`src/content.config.ts`:

```ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const fonti = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './contenuti/fonti' }),
  schema: z.object({
    titolo: z.string(),
    tipo: z.enum(['video', 'podcast', 'libro', 'paper', 'corso', 'sito']),
    autore: z.string().optional(),
    link: z.string().url(),
    linkAlternativi: z.array(z.object({ etichetta: z.string(), url: z.string().url() })).default([]),
    stato: z.enum(['solo-link', 'in-lavorazione', 'riassunto']).default('solo-link'),
    tag: z.array(z.string()).default([]),
    aggiunta: z.coerce.date().optional(),
  }),
});

const articoli = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './contenuti/articoli' }),
  schema: z.object({
    titolo: z.string(),
    autore: z.string(),
    data: z.coerce.date(),
    tag: z.array(z.string()).default([]),
    bozza: z.boolean().default(false),
  }),
});

const lavagna = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './contenuti/lavagna' }),
  schema: z.object({ titolo: z.string() }),
});

export const collections = { fonti, articoli, lavagna };
```

- [ ] **Step 3: Test negativo — un frontmatter sbagliato DEVE far fallire la build**

Crea `contenuti/fonti/prova-rotta.md`:

```markdown
---
titolo: "Prova"
tipo: gazzetta
link: "non-un-url"
---
```

Run: `npm run build`
Expected: FAIL con errore zod che nomina `tipo` (valore non ammesso) e `link` (url non valido). Questo è il meccanismo di protezione per i contributor: verificato.

- [ ] **Step 4: Rimuovi il file rotto e verifica che la build passi**

```powershell
Remove-Item contenuti/fonti/prova-rotta.md
npm run build
```
Expected: PASS.

- [ ] **Step 5: Scrivi i template per i contributor**

`template/template-fonte.md`:

```markdown
---
# ISTRUZIONI: copia questo file in contenuti/fonti/ con un nome tipo
# nome-della-fonte.md (minuscole e trattini). Compila i campi e cancella
# le righe di commento (quelle che iniziano con #).
titolo: "Titolo della fonte"
# tipo: uno tra video | podcast | libro | paper | corso | sito
tipo: video
autore: "Nome dell'autore (facoltativo, cancella la riga se non serve)"
link: "https://esempio.com"
# stato: solo-link (solo segnalazione) | in-lavorazione | riassunto (completo)
stato: solo-link
tag: [etf]
# aggiunta: data di oggi, per la sezione "Ultime aggiunte" della home
aggiunta: 2026-07-04
---

Qui sotto scrivi il riassunto pratico: i concetti da portarsi a casa,
in elenco puntato. Se per ora è solo un link, due righe sul perché
merita bastano.
```

`template/template-articolo.md`:

```markdown
---
# ISTRUZIONI: copia questo file in contenuti/articoli/ con un nome tipo
# titolo-del-articolo.md (minuscole e trattini). Compila e cancella i commenti.
titolo: "Titolo dell'articolo"
autore: "Il tuo nome"
data: 2026-07-04
tag: [obbligazioni]
# bozza: true = non compare sul sito finché non la togli
bozza: false
---

Scrivi qui l'articolo in markdown: titoli con ##, elenchi con -,
link con [testo](https://...).
```

- [ ] **Step 6: Builda di nuovo (i template NON devono entrare nelle collezioni)**

Run: `npm run build`
Expected: PASS — `template/` non è dentro `contenuti/`, quindi il loader non lo tocca.

- [ ] **Step 7: Micro-commit e merge**

```bash
git add src/content.config.ts template/ contenuti/
git commit -m "feat: collezioni fonti/articoli/lavagna con validazione zod + template contributor"
git checkout main
git merge --no-ff feat/collezioni-contenuti -m "merge: feat/collezioni-contenuti"
```

---

### Task 4: Fonti — migrazione, paper da BibTeX, catalogo e pagine

**Branch:** `feat/fonti`

**Files:**
- Create: `contenuti/fonti/*.md` (10 schede copiate da `docs/superpowers/plans/assets/fonti/`)
- Create: `scripts/bib2fonti.py` (genera 19 schede `paper-*.md` da `paper/paper.bib`)
- Create: `src/pages/fonti/index.astro`
- Create: `src/pages/fonti/[slug].astro`
- Create: `src/components/BadgeTipo.astro`

**Interfaces:**
- Consumes: collezione `fonti` (Task 3), `Base.astro` + `href()` + classi CSS (Task 2).
- Produces: pagine `/fonti` e `/fonti/<id>`; `BadgeTipo.astro` con props `{ tipo: string }` (riusato dal Task 8 nella home).

- [ ] **Step 1: Crea il branch e copia le schede migrate**

```powershell
git checkout -b feat/fonti
Copy-Item docs/superpowers/plans/assets/fonti/*.md contenuti/fonti/
npm run build   # le 10 schede devono passare la validazione
```
Expected: PASS.

```bash
git add contenuti/fonti
git commit -m "contenuti: 10 schede fonte migrate dal Notion"
```

- [ ] **Step 2: Scrivi il generatore di schede paper**

`scripts/bib2fonti.py`:

```python
"""Genera le schede fonte tipo=paper da paper/paper.bib (una tantum).

Uso: python scripts/bib2fonti.py   (dalla radice del repo)
"""
import pathlib
import re

BIB = pathlib.Path("paper/paper.bib").read_text(encoding="utf-8")
DEST = pathlib.Path("contenuti/fonti")


def pulisci(testo: str) -> str:
    testo = re.sub(r"[{}]", "", testo)
    return testo.replace("\\%", "%").replace('"', "'").strip()


voci = re.findall(r"@\w+\{(?P<chiave>[^,]+),(?P<corpo>.*?)\n\}", BIB, re.S)
if not voci:
    raise SystemExit("ERRORE: nessuna voce trovata in paper/paper.bib")

for chiave, corpo in voci:
    campi = dict(re.findall(r"(\w+)\s*=\s*\{(.*?)\}\s*,?\n", corpo, re.S))
    titolo = pulisci(campi.get("title", chiave))
    autori = pulisci(campi.get("author", "")).replace(" and ", "; ")
    anno = pulisci(campi.get("year", ""))
    url = pulisci(campi.get("url", ""))
    rivista = pulisci(campi.get("journal", campi.get("publisher", "")))
    slug = chiave.strip().replace("_", "-").lower()
    dove = f" — *{rivista}*" if rivista else ""
    scheda = "\n".join(
        [
            "---",
            f'titolo: "{titolo} ({anno})"',
            "tipo: paper",
            f'autore: "{autori}"',
            f'link: "{url}"',
            "stato: solo-link",
            "tag: [paper]",
            "---",
            f"Paper accademico{dove}. Riferimento completo in `paper/paper.bib`; "
            "il PDF non è nel repo per copyright: usare il link ufficiale.",
            "",
        ]
    )
    (DEST / f"paper-{slug}.md").write_text(scheda, encoding="utf-8")

print(f"{len(voci)} schede paper generate in {DEST}/")
```

- [ ] **Step 3: Esegui il generatore e verifica**

Run: `python scripts/bib2fonti.py`
Expected: `19 schede paper generate in contenuti/fonti/`

Run: `npm run build`
Expected: PASS (19 nuove schede valide).

```bash
git add scripts/bib2fonti.py contenuti/fonti
git commit -m "feat: generatore schede paper da BibTeX + 19 paper migrati"
```

- [ ] **Step 4: Componente badge tipo**

`src/components/BadgeTipo.astro`:

```astro
---
const { tipo } = Astro.props as { tipo: string };
---
<span class="badge">{tipo}</span>
```

- [ ] **Step 5: Pagina catalogo con filtri client-side**

`src/pages/fonti/index.astro`:

```astro
---
import Base from '../../layouts/Base.astro';
import BadgeTipo from '../../components/BadgeTipo.astro';
import { getCollection } from 'astro:content';
import { href } from '../../lib/percorsi';

const fonti = (await getCollection('fonti')).sort((a, b) =>
  a.data.titolo.localeCompare(b.data.titolo, 'it'),
);
const tipi = ['video', 'podcast', 'libro', 'paper', 'corso', 'sito'];
---
<Base titolo="Fonti" descrizione="Video, podcast, libri e paper selezionati dal gruppo, con i concetti da portarsi a casa.">
  <p class="kicker">Catalogo</p>
  <h1>Fonti</h1>
  <p class="muted">
    Ogni fonte ha una scheda: prima solo il link, poi — quando qualcuno la lavora — il riassunto
    con i concetti da portarsi a casa. Vuoi aggiungerne una?
    <a href={href('/come-contribuire')}>Si fa in due minuti</a>.
  </p>

  <div class="filtri" role="group" aria-label="Filtra per tipo">
    <button class="filtro attivo" data-tipo="tutti">tutte</button>
    {tipi.map((t) => <button class="filtro" data-tipo={t}>{t}</button>)}
  </div>

  <ul class="elenco-fonti">
    {fonti.map((f) => (
      <li data-tipo={f.data.tipo}>
        <BadgeTipo tipo={f.data.tipo} />
        <span>
          {f.data.stato === 'solo-link' ? (
            <a href={f.data.link} rel="noopener">{f.data.titolo}&thinsp;↗</a>
          ) : (
            <a href={href(`/fonti/${f.id}`)}>{f.data.titolo}</a>
          )}
          {f.data.autore && <span class="muted"> — {f.data.autore}</span>}
          {f.data.stato === 'riassunto' && <span class="badge stato">riassunto</span>}
          {f.data.stato === 'in-lavorazione' && <span class="badge stato">in lavorazione</span>}
        </span>
      </li>
    ))}
  </ul>
</Base>

<style>
  .filtri { display: flex; gap: .5rem; flex-wrap: wrap; margin: 1.4rem 0; }
  .filtro {
    background: none; border: 1px solid var(--hairline); border-radius: 3px;
    color: var(--muted); cursor: pointer; font-size: .78rem; letter-spacing: .05em;
    text-transform: uppercase; padding: .2rem .7rem;
  }
  .filtro.attivo { border-color: var(--accent); color: var(--accent); }
  .elenco-fonti { list-style: none; padding-left: 0 !important; }
  .elenco-fonti li {
    display: flex; gap: .8rem; align-items: baseline;
    padding: .55rem 0; border-bottom: 1px solid var(--hairline);
  }
  .elenco-fonti li.nascosta { display: none; }
  .badge.stato { margin-left: .5rem; }
</style>

<script>
  const bottoni = document.querySelectorAll<HTMLButtonElement>('.filtro');
  const voci = document.querySelectorAll<HTMLLIElement>('.elenco-fonti li');
  bottoni.forEach((b) =>
    b.addEventListener('click', () => {
      bottoni.forEach((x) => x.classList.remove('attivo'));
      b.classList.add('attivo');
      const tipo = b.dataset.tipo;
      voci.forEach((v) => v.classList.toggle('nascosta', tipo !== 'tutti' && v.dataset.tipo !== tipo));
    }),
  );
</script>
```

- [ ] **Step 6: Pagina della singola scheda (solo per fonti lavorate)**

`src/pages/fonti/[slug].astro`:

```astro
---
import Base from '../../layouts/Base.astro';
import BadgeTipo from '../../components/BadgeTipo.astro';
import { getCollection, render } from 'astro:content';
import { href } from '../../lib/percorsi';

export async function getStaticPaths() {
  const fonti = await getCollection('fonti', (f) => f.data.stato !== 'solo-link');
  return fonti.map((f) => ({ params: { slug: f.id }, props: { fonte: f } }));
}
const { fonte } = Astro.props;
const { Content } = await render(fonte);
---
<Base titolo={fonte.data.titolo}>
  <p class="kicker"><a href={href('/fonti')}>Fonti</a> / {fonte.data.tipo}</p>
  <h1>{fonte.data.titolo}</h1>
  <ul class="meta-riga">
    <li><BadgeTipo tipo={fonte.data.tipo} /></li>
    {fonte.data.autore && <li><b>Autore</b> {fonte.data.autore}</li>}
    <li><a href={fonte.data.link} rel="noopener">Apri la fonte&thinsp;↗</a></li>
    {fonte.data.linkAlternativi.map((l) => <li><a href={l.url} rel="noopener">{l.etichetta}&thinsp;↗</a></li>)}
    <li><b>Stato</b> {fonte.data.stato}</li>
  </ul>
  <Content />
</Base>
```

- [ ] **Step 7: Builda, verifica visivamente, micro-commit e merge**

Run: `npm run build`
Expected: PASS; nel log compaiono le route `/fonti` e le pagine delle fonti con stato ≠ solo-link (al momento 0 o poche: le schede migrate sono quasi tutte solo-link — la pagina [slug] esiste per quando arriveranno i riassunti).

Screenshot (entrambi i temi, vedi `DESIGN.md`) della pagina `/investiamo-pagio/fonti/`: filtri in alto, elenco con badge. GUARDA il risultato.

```bash
git add src/pages/fonti src/components/BadgeTipo.astro
git commit -m "feat: catalogo fonti filtrabile e pagina scheda"
git checkout main
git merge --no-ff feat/fonti -m "merge: feat/fonti"
```

---

### Task 5: Catalogo ETF con TER, label e copia-ISIN

**Branch:** `feat/catalogo-etf`

**Files:**
- Create: `dati/etf.yaml` (copiato da `docs/superpowers/plans/assets/etf.yaml`, versione ampliata con TER e label)
- Create: `src/lib/dati.ts`
- Create: `src/pages/etf.astro`

**Interfaces:**
- Consumes: `Base.astro`, `href()`, classi CSS (Task 2).
- Produces: `caricaEtf(): CatalogoEtf` da `src/lib/dati.ts` con tipo
  `{ aggiornato: string; categorie: { id: string; nome: string; nota?: string; video?: string; etf: { nome: string; isin: string; ticker?: string; ter?: number; label: string[]; note?: string; justetf?: string }[] }[] }`.
  Il Task 7 e 8 estendono QUESTO file con altri loader: non crearne un secondo.

- [ ] **Step 1: Crea il branch e copia il catalogo**

```powershell
git checkout -b feat/catalogo-etf
Copy-Item docs/superpowers/plans/assets/etf.yaml dati/etf.yaml
```

- [ ] **Step 2: Scrivi il loader con validazione (test = la build)**

`src/lib/dati.ts`:

```ts
import { readFileSync } from 'node:fs';
import yaml from 'js-yaml';
import { z } from 'zod';

const VoceEtf = z.object({
  nome: z.string(),
  isin: z.string().regex(/^[A-Z]{2}[A-Z0-9]{9}[0-9]$/, 'ISIN non valido'),
  ticker: z.string().optional(),
  ter: z.number().min(0).max(5).optional(), // percento annuo: 0.22 = 0,22%
  label: z.array(z.string()).default([]),
  note: z.string().optional(),
  justetf: z.string().url().optional(),
});

const CategoriaEtf = z.object({
  id: z.string(),
  nome: z.string(),
  nota: z.string().optional(),
  video: z.string().url().optional(),
  etf: z.array(VoceEtf),
});

const CatalogoEtfSchema = z.object({
  aggiornato: z.string(),
  categorie: z.array(CategoriaEtf),
});

export type CatalogoEtf = z.infer<typeof CatalogoEtfSchema>;

export function caricaEtf(): CatalogoEtf {
  return CatalogoEtfSchema.parse(yaml.load(readFileSync('dati/etf.yaml', 'utf8')));
}
```

- [ ] **Step 3: Test negativo del loader**

Modifica temporaneamente in `dati/etf.yaml` un ISIN in `NONVALIDO`; `npm run build` sulla pagina del passo 4 deve fallire con "ISIN non valido". (Se la pagina non esiste ancora, fai il passo 4 e poi torna qui.) Ripristina l'ISIN.

- [ ] **Step 4: Pagina ETF con filtro per label e copia-ISIN**

`src/pages/etf.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { caricaEtf } from '../lib/dati';

const catalogo = caricaEtf();
const tutteLeLabel = [...new Set(catalogo.categorie.flatMap((c) => c.etf.flatMap((e) => e.label)))].sort();
const fmtTer = (t?: number) => (t == null ? '—' : t.toLocaleString('it-IT', { minimumFractionDigits: 2 }) + '%');
---
<Base titolo="ETF selezionati" descrizione="Il catalogo curato dal gruppo: ISIN, TER e note pratiche.">
  <div class="colonna-larga">
    <p class="kicker">Catalogo</p>
    <h1>ETF selezionati</h1>
    <p class="muted">
      La lista curata dal gruppo, per categoria. I TER sono indicativi
      (aggiornati al {catalogo.aggiornato}): prima di comprare verifica sempre su JustETF.
      Clicca ⧉ per copiare l'ISIN.
    </p>

    <div class="filtri" role="group" aria-label="Filtra per caratteristica">
      <input id="cerca-etf" type="search" placeholder="Cerca nome, ISIN o ticker…" />
      <button class="filtro attivo" data-label="tutte">tutte</button>
      {tutteLeLabel.map((l) => <button class="filtro" data-label={l}>{l}</button>)}
    </div>

    {catalogo.categorie.map((cat) => (
      <section data-categoria={cat.id}>
        <h2>{cat.nome}</h2>
        {cat.nota && <p class="muted nota-categoria">{cat.nota}</p>}
        {cat.video && <p class="muted nota-categoria"><a href={cat.video} rel="noopener">Video di riferimento&thinsp;↗</a></p>}
        <div class="scorri">
          <table>
            <thead>
              <tr><th>Nome</th><th>ISIN</th><th>Ticker</th><th class="num-h">TER</th><th>Label</th><th>Note</th><th></th></tr>
            </thead>
            <tbody>
              {cat.etf.map((e) => (
                <tr data-label={e.label.join(' ')} data-cerca={`${e.nome} ${e.isin} ${e.ticker ?? ''}`.toLowerCase()}>
                  <td>{e.nome}</td>
                  <td class="mono">{e.isin} <button class="copia" data-isin={e.isin} title={`Copia ${e.isin}`}>⧉</button></td>
                  <td class="mono">{e.ticker ?? ''}</td>
                  <td class="num">{fmtTer(e.ter)}</td>
                  <td>{e.label.map((l) => <span class="badge">{l}</span>)}</td>
                  <td class="muted note">{e.note ?? ''}</td>
                  <td>{e.justetf && <a href={e.justetf} rel="noopener">JustETF&thinsp;↗</a>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    ))}
  </div>
</Base>

<style>
  .filtri { display: flex; gap: .45rem; flex-wrap: wrap; margin: 1.4rem 0; align-items: center; }
  .filtri input {
    font: inherit; font-size: .85rem; color: var(--ink); background: var(--bg);
    border: 1px solid var(--hairline); border-radius: 3px; padding: .25rem .6rem; min-width: 15rem;
  }
  .filtro {
    background: none; border: 1px solid var(--hairline); border-radius: 3px;
    color: var(--muted); cursor: pointer; font-size: .74rem; letter-spacing: .04em;
    text-transform: uppercase; padding: .15rem .55rem;
  }
  .filtro.attivo { border-color: var(--accent); color: var(--accent); }
  .num-h { text-align: right; }
  .mono { font-family: var(--mono); font-size: .8rem; white-space: nowrap; }
  .copia { cursor: pointer; border: none; background: none; color: var(--muted); font-size: .78rem; }
  .copia:hover, .copia.fatto { color: var(--accent); }
  td .badge { margin-right: .3rem; }
  td.note { max-width: 20rem; font-size: .82rem; }
  .nota-categoria { font-size: .85rem; max-width: 42rem; }
  tr.nascosta, section.vuota { display: none; }
</style>

<script>
  // Copia ISIN
  document.querySelectorAll<HTMLButtonElement>('.copia').forEach((b) =>
    b.addEventListener('click', async () => {
      await navigator.clipboard.writeText(b.dataset.isin ?? '');
      b.textContent = '✓';
      b.classList.add('fatto');
      setTimeout(() => { b.textContent = '⧉'; b.classList.remove('fatto'); }, 1200);
    }),
  );

  // Filtro per label + ricerca testuale
  const bottoni = document.querySelectorAll<HTMLButtonElement>('.filtro');
  const campo = document.getElementById('cerca-etf') as HTMLInputElement;
  let labelAttiva = 'tutte';

  function applica() {
    const testo = campo.value.trim().toLowerCase();
    document.querySelectorAll<HTMLTableRowElement>('tbody tr').forEach((r) => {
      const perLabel = labelAttiva === 'tutte' || (r.dataset.label ?? '').split(' ').includes(labelAttiva);
      const perTesto = !testo || (r.dataset.cerca ?? '').includes(testo);
      r.classList.toggle('nascosta', !(perLabel && perTesto));
    });
    document.querySelectorAll<HTMLElement>('section[data-categoria]').forEach((s) => {
      const visibili = s.querySelectorAll('tbody tr:not(.nascosta)').length;
      s.classList.toggle('vuota', visibili === 0);
    });
  }

  bottoni.forEach((b) =>
    b.addEventListener('click', () => {
      bottoni.forEach((x) => x.classList.remove('attivo'));
      b.classList.add('attivo');
      labelAttiva = b.dataset.label ?? 'tutte';
      applica();
    }),
  );
  campo.addEventListener('input', applica);
</script>
```

- [ ] **Step 5: Builda, prova i filtri, verifica visivamente**

Run: `npm run build`
Expected: PASS.

Con `npm run preview`: apri `/investiamo-pagio/etf`, prova un filtro label (es. `value`), la ricerca testuale (es. `VWCE`) e il bottone copia. Screenshot entrambi i temi: tabelle con testata maiuscoletto, ISIN monospace, badge label.

- [ ] **Step 6: Micro-commit e merge**

```bash
git add dati/etf.yaml src/lib/dati.ts src/pages/etf.astro
git commit -m "feat: catalogo ETF con TER, label filtrabili, ricerca e copia-ISIN"
git checkout main
git merge --no-ff feat/catalogo-etf -m "merge: feat/catalogo-etf"
```

---

### Task 6: Backtest Python (TDD)

**Branch:** `feat/backtest-python`

**Files:**
- Create: `dati/portafogli/*.yaml` (4 file copiati da `docs/superpowers/plans/assets/portafogli/`)
- Create: `backtest/requirements.txt`
- Create: `backtest/metriche.py`
- Create: `backtest/run_backtest.py`
- Create: `backtest/README.md`
- Create: `backtest/dati_grezzi/*.csv` (generati dallo script, committati)
- Create: `dati/backtest/*.json` (generati dallo script, committati)
- Test: `backtest/tests/test_metriche.py`

**Interfaces:**
- Consumes: niente dal sito (pipeline indipendente).
- Produces: 4 file `dati/backtest/<slug>.json` con struttura ESATTA (consumata dal Task 7):
  `{ "portafoglio": string, "aggiornato": "YYYY-MM-DD", "valuta": "EUR", "finestra": ["YYYY-MM", "YYYY-MM"], "serie": [["YYYY-MM", number], ...], "metriche": { "cagr": number, "volatilita": number, "max_drawdown": number, "peggior_anno": number } }`
  (frazioni decimali: `0.067` = 6,7%). Slug dei 4 portafogli: `golden-butterfly-the-bull`, `all-weather-eu`, `lifestrategy-60`, `azionario-globale-100`.

**Nota metodologica (va riportata anche in `backtest/README.md`):** gli ETF UCITS reali hanno storia breve, quindi si usano proxy USA con storia lunga e dividendi inclusi (Adj Close via yfinance): `VT` azionario globale, `TLT` obbligazioni lunghe, `SHY` brevi, `BND` aggregate, `GLD` oro, `DBC` commodities; conversione in EUR con `EURUSD=X`. La finestra utile parte da ~2008-07 (nascita di VT). I CSV grezzi si committano: build deterministica e rigenerabile offline.

- [ ] **Step 1: Crea il branch, copia i portafogli, scrivi requirements**

```powershell
git checkout -b feat/backtest-python
Copy-Item docs/superpowers/plans/assets/portafogli/*.yaml dati/portafogli/
```

`backtest/requirements.txt`:

```
pandas>=2.2
yfinance>=0.2.40
PyYAML>=6
pytest>=8
```

Run: `pip install -r backtest/requirements.txt`
Expected: installazione ok.

- [ ] **Step 2: Scrivi i test PRIMA (falliranno)**

`backtest/tests/test_metriche.py`:

```python
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import pandas as pd
import pytest

from metriche import (
    cagr,
    max_drawdown,
    peggior_anno,
    simula_portafoglio,
    volatilita_annualizzata,
)


def serie_mensile(valori, inizio="2020-01-31"):
    idx = pd.date_range(inizio, periods=len(valori), freq="ME")
    return pd.Series([float(v) for v in valori], index=idx)


def test_cagr_crescita_costante_1pc_al_mese():
    s = serie_mensile([100 * 1.01**i for i in range(25)])
    assert cagr(s) == pytest.approx(1.01**12 - 1)


def test_volatilita_serie_costante_e_zero():
    s = serie_mensile([100] * 12)
    assert volatilita_annualizzata(s) == pytest.approx(0.0)


def test_max_drawdown_picco_120_minimo_90():
    s = serie_mensile([100, 120, 90, 130])
    assert max_drawdown(s) == pytest.approx(90 / 120 - 1)


def test_peggior_anno_meno_20_percento():
    # 2020 piatto (0%), 2021 chiude a -20% rispetto a fine 2020
    s = serie_mensile([100] * 12 + [80] * 12, inizio="2020-01-31")
    assert peggior_anno(s) == pytest.approx(-0.20)


def test_simula_50_50_un_asset_sale_10pc():
    idx = pd.date_range("2020-01-31", periods=13, freq="ME")
    prezzi = pd.DataFrame(
        {"A": [100.0] * 13, "B": [100.0] + [110.0] * 12}, index=idx
    )
    serie = simula_portafoglio(prezzi, {"A": 0.5, "B": 0.5})
    assert serie.iloc[0] == pytest.approx(10_000)
    assert serie.iloc[1] == pytest.approx(10_500)  # 5000 + 5000 * 1.1
    assert serie.iloc[-1] == pytest.approx(10_500)  # poi tutto fermo


def test_simula_ribilanciamento_cambia_il_risultato():
    # B raddoppia ogni anno, A fermo: col ribilanciamento a inizio anno
    # i guadagni di B vengono in parte spostati su A.
    idx = pd.date_range("2020-01-31", periods=25, freq="ME")
    prezzi = pd.DataFrame(
        {"A": [100.0] * 25, "B": [100.0 * 2 ** (i // 12) for i in range(25)]},
        index=idx,
    )
    serie = simula_portafoglio(prezzi, {"A": 0.5, "B": 0.5})
    # Anno 1: 5000 + 5000*2 = 15000. Ribilanciato a 7500/7500.
    # Anno 2: 7500 + 7500*2 = 22500.
    assert serie.iloc[12] == pytest.approx(15_000)
    assert serie.iloc[24] == pytest.approx(22_500)
```

- [ ] **Step 3: Verifica che i test falliscano**

Run: `python -m pytest backtest/tests -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'metriche'`.

- [ ] **Step 4: Implementa le metriche**

`backtest/metriche.py`:

```python
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
```

- [ ] **Step 5: Verifica che i test passino**

Run: `python -m pytest backtest/tests -q`
Expected: `6 passed`.

```bash
git add backtest/metriche.py backtest/tests backtest/requirements.txt dati/portafogli
git commit -m "feat: metriche di backtest pure con test (cagr, vol, drawdown, ribilanciamento)"
```

- [ ] **Step 6: Scrivi la pipeline di scarico e generazione**

`backtest/run_backtest.py`:

```python
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
            f"maxDD {m['max_drawdown']:.2%}, finestra {risultato['finestra'][0]} → {risultato['finestra'][1]}"
        )


if __name__ == "__main__":
    main()
```

- [ ] **Step 7: Esegui la pipeline e controlla i numeri**

Run: `python backtest/run_backtest.py`
Expected: stampa dei 6 proxy + cambio, poi una riga per portafoglio con metriche plausibili (CAGR tra 3% e 12%, maxDD di `azionario-globale-100` più profondo degli altri, finestra ~2008-07 → mese scorso). Se yfinance dà errori di rete: riprova; se un ticker risulta vuoto, il messaggio d'errore dice quale.

Verifica file: `Get-ChildItem dati/backtest` → 4 JSON; `Get-ChildItem backtest/dati_grezzi` → 7 CSV.

- [ ] **Step 8: Scrivi il README della pipeline**

`backtest/README.md`:

```markdown
# Backtest — come rigenerare i dati

Chiunque del gruppo può aggiornare i numeri della dashboard:

1. `pip install -r backtest/requirements.txt` (una volta sola)
2. `python backtest/run_backtest.py` (dalla radice del repo)
3. commit di `backtest/dati_grezzi/` e `dati/backtest/` — al push il sito si aggiorna

`--offline` ricalcola senza scaricare (usa i CSV committati).

## Metodologia (e limiti, onestamente)

- Gli ETF UCITS reali hanno pochi anni di storia: usiamo proxy USA con
  dividendi reinvestiti (Adj Close): VT (azioni globali), TLT (bond lunghi),
  SHY (bond brevi), BND (aggregate), GLD (oro), DBC (commodities).
- Conversione in EUR col cambio EURUSD di Yahoo Finance.
- Serie mensili, ribilanciamento al primo mese dell'anno, niente costi,
  tasse o TER: i numeri servono a CONFRONTARE i portafogli, non a prevedere.
- La finestra parte da luglio 2008 (nascita di VT): include la coda della
  crisi 2008, il 2011, il 2020 e il 2022, ma non l'intero crollo Lehman.
- I test dei calcoli: `python -m pytest backtest/tests -q`
```

- [ ] **Step 9: Micro-commit e merge**

```bash
git add backtest/ dati/backtest dati/portafogli
git commit -m "feat: pipeline backtest con proxy EUR, dati grezzi committati e README metodologico"
git checkout main
git merge --no-ff feat/backtest-python -m "merge: feat/backtest-python"
```

---

### Task 7: Pagine portafogli e dashboard di confronto

**Branch:** `feat/portafogli-dashboard`

**Files:**
- Modify: `src/lib/dati.ts` (aggiunge loader portafogli e backtest)
- Create: `src/lib/formato.ts`
- Create: `src/components/GraficoLinee.astro`
- Create: `src/pages/portafogli/index.astro` (dashboard)
- Create: `src/pages/portafogli/[slug].astro`

**Interfaces:**
- Consumes: JSON del Task 6 (struttura esatta nel suo blocco Interfaces), `caricaEtf`/`dati.ts` (Task 5), `Base.astro` + classi (Task 2).
- Produces:
  - in `src/lib/dati.ts`: `caricaPortafogli(): DatiPortafoglio[]` e `caricaBacktest(slug: string): DatiBacktest | null` (tipi sotto);
  - in `src/lib/formato.ts`: `pct(v: number): string` (0.067 → "6,7%"), `dataIt(iso: string): string`;
  - `GraficoLinee.astro` con props `{ serie: { nome: string; colore: string; punti: [string, number][] }[] }` — riusabile per altri grafici.

- [ ] **Step 1: Crea il branch ed estendi il loader**

```bash
git checkout -b feat/portafogli-dashboard
```

Aggiungi in coda a `src/lib/dati.ts`:

```ts
import { existsSync, readdirSync } from 'node:fs';

const Allocazione = z.object({
  asset: z.string(),
  peso: z.number().positive().max(1),
  proxy: z.string(),
  etf_reale: z.object({ nome: z.string(), isin: z.string(), ticker: z.string().optional() }),
  commento: z.string().optional(),
});

const PortafoglioSchema = z.object({
  nome: z.string(),
  slug: z.string(),
  descrizione: z.string(),
  ribilanciamento: z.literal('annuale'),
  allocazioni: z.array(Allocazione),
});

export type DatiPortafoglio = z.infer<typeof PortafoglioSchema>;

export function caricaPortafogli(): DatiPortafoglio[] {
  return readdirSync('dati/portafogli')
    .filter((f) => f.endsWith('.yaml'))
    .map((f) => PortafoglioSchema.parse(yaml.load(readFileSync(`dati/portafogli/${f}`, 'utf8'))));
}

const BacktestSchema = z.object({
  portafoglio: z.string(),
  aggiornato: z.string(),
  valuta: z.string(),
  finestra: z.tuple([z.string(), z.string()]),
  serie: z.array(z.tuple([z.string(), z.number()])),
  metriche: z.object({
    cagr: z.number(),
    volatilita: z.number(),
    max_drawdown: z.number(),
    peggior_anno: z.number(),
  }),
});

export type DatiBacktest = z.infer<typeof BacktestSchema>;

export function caricaBacktest(slug: string): DatiBacktest | null {
  const percorso = `dati/backtest/${slug}.json`;
  if (!existsSync(percorso)) return null;
  return BacktestSchema.parse(JSON.parse(readFileSync(percorso, 'utf8')));
}
```

(nota: `z`, `yaml`, `readFileSync` sono già importati in testa al file dal Task 5).

`src/lib/formato.ts`:

```ts
/** 0.067 → "6,7%" (frazione decimale → percento it-IT) */
export function pct(v: number): string {
  return (v * 100).toLocaleString('it-IT', { maximumFractionDigits: 1 }) + '%';
}

/** "2026-07-04" → "4 luglio 2026" */
export function dataIt(iso: string): string {
  return new Date(iso).toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' });
}
```

- [ ] **Step 2: Componente grafico SVG a scala logaritmica**

`src/components/GraficoLinee.astro`:

```astro
---
interface Linea { nome: string; colore: string; punti: [string, number][] }
const { serie } = Astro.props as { serie: Linea[] };

const L = 640, A = 280, SX = 48, ALTO = 14, BASSO = 34;
const valori = serie.flatMap((s) => s.punti.map((p) => p[1]));
const lnMin = Math.log(Math.min(...valori));
const lnMax = Math.log(Math.max(...valori));
const X = (i: number, n: number) => SX + ((L - SX - 10) * i) / Math.max(n - 1, 1);
const Y = (v: number) => ALTO + (A - ALTO - BASSO) * (1 - (Math.log(v) - lnMin) / (lnMax - lnMin));

// griglia orizzontale: raddoppi dal minimo (scala log)
const griglia: number[] = [];
for (let v = Math.min(...valori); v <= Math.max(...valori); v *= 2) griglia.push(v);
const kEuro = (v: number) => (v >= 1000 ? Math.round(v / 1000) + 'k' : Math.round(v).toString());

// etichette x: prima, centrale, ultima data della prima serie
const date = serie[0].punti.map((p) => p[0]);
const etichetteX = [
  [date[0], X(0, date.length)],
  [date[Math.floor(date.length / 2)], X(Math.floor(date.length / 2), date.length)],
  [date[date.length - 1], X(date.length - 1, date.length)],
] as const;
---
<svg viewBox={`0 0 ${L} ${A}`} width="100%" role="img" aria-label="Confronto della crescita dei portafogli (scala logaritmica)">
  <g stroke="var(--hairline)" stroke-width="1">
    <line x1={SX} y1={ALTO} x2={SX} y2={A - BASSO} />
    <line x1={SX} y1={A - BASSO} x2={L - 10} y2={A - BASSO} />
    {griglia.slice(1).map((v) => (
      <line x1={SX} y1={Y(v)} x2={L - 10} y2={Y(v)} stroke-dasharray="3 5" />
    ))}
  </g>
  <g fill="var(--muted)" font-size="10" font-family="Consolas, monospace">
    {griglia.map((v) => (
      <text x={SX - 6} y={Y(v) + 3} text-anchor="end">{kEuro(v)}</text>
    ))}
    {etichetteX.map(([testo, x], i) => (
      <text x={x} y={A - BASSO + 16} text-anchor={i === 0 ? 'start' : i === 2 ? 'end' : 'middle'}>{testo}</text>
    ))}
  </g>
  {serie.map((s) => (
    <polyline
      fill="none"
      stroke={s.colore}
      stroke-width="1.8"
      points={s.punti.map((p, i) => `${X(i, s.punti.length).toFixed(1)},${Y(p[1]).toFixed(1)}`).join(' ')}
    />
  ))}
</svg>
```

- [ ] **Step 3: Dashboard di confronto**

`src/pages/portafogli/index.astro`:

```astro
---
import Base from '../../layouts/Base.astro';
import GraficoLinee from '../../components/GraficoLinee.astro';
import { caricaPortafogli, caricaBacktest } from '../../lib/dati';
import { pct, dataIt } from '../../lib/formato';
import { href } from '../../lib/percorsi';

const COLORI = ['#A85454', 'var(--accent)', '#B0813C', '#7A6FA8'];
const portafogli = caricaPortafogli();
const conDati = portafogli
  .map((p) => ({ p, bt: caricaBacktest(p.slug) }))
  .filter((x): x is { p: (typeof portafogli)[0]; bt: NonNullable<ReturnType<typeof caricaBacktest>> } => x.bt !== null)
  .sort((a, b) => b.bt.metriche.cagr - a.bt.metriche.cagr);

const serie = conDati.map((x, i) => ({ nome: x.p.nome, colore: COLORI[i % COLORI.length], punti: x.bt.serie }));
const aggiornato = conDati[0]?.bt.aggiornato;
const finestra = conDati[0]?.bt.finestra;
---
<Base titolo="Portafogli" descrizione="I lazy portfolio del gruppo a confronto, con backtest fatti in casa.">
  <div class="colonna-larga">
    <p class="kicker">Dashboard</p>
    <h1>Portafogli a confronto</h1>
    <p class="muted">
      Crescita di 10.000&thinsp;€ — {finestra?.[0]} → {finestra?.[1]}, scala logaritmica,
      ribilanciamento annuale. Backtest nostri: <a href={href('/portafogli') + '#metodo'}>metodo e limiti</a> sotto.
    </p>

    <div class="pannello">
      <GraficoLinee serie={serie} />
      <div class="legenda">
        {serie.map((s) => (
          <span style={`--c: ${s.colore}`}>{s.nome}</span>
        ))}
      </div>
    </div>

    <div class="scorri">
      <table>
        <thead>
          <tr><th>Portafoglio</th><th class="num-h">CAGR</th><th class="num-h">Volatilità</th><th class="num-h">Max drawdown</th><th class="num-h">Peggior anno</th></tr>
        </thead>
        <tbody>
          {conDati.map(({ p, bt }) => (
            <tr>
              <td><a href={href(`/portafogli/${p.slug}`)}>{p.nome}</a></td>
              <td class="num">{pct(bt.metriche.cagr)}</td>
              <td class="num">{pct(bt.metriche.volatilita)}</td>
              <td class="num">{pct(bt.metriche.max_drawdown)}</td>
              <td class="num">{pct(bt.metriche.peggior_anno)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>

    <h2 id="metodo">Metodo e limiti</h2>
    <p class="muted">
      I backtest usano indici/ETF USA come proxy (gli ETF UCITS reali hanno storia troppo breve),
      convertiti in euro, senza costi né tasse: servono a confrontare i portafogli tra loro,
      non a prevedere il futuro. Dettagli in <code>backtest/README.md</code>.
      <em>Niente qui è un consiglio d'investimento.</em>
    </p>
    <p class="mono-piccolo">dati aggiornati al {aggiornato && dataIt(aggiornato)} · rigenerati con backtest/run_backtest.py</p>
  </div>
</Base>

<style>
  .pannello { border: 1px solid var(--hairline); border-radius: 4px; padding: 1.2rem; background: var(--bg-raise); margin: 1.4rem 0; }
  .legenda { display: flex; gap: 1.4rem; flex-wrap: wrap; font-size: .8rem; color: var(--muted); margin-top: .8rem; }
  .legenda span::before { content: '—'; font-weight: 700; margin-right: .35rem; color: var(--c); }
  .num-h { text-align: right; }
  .mono-piccolo { font-family: var(--mono); font-size: .74rem; color: var(--muted); }
</style>
```

- [ ] **Step 4: Pagina del singolo portafoglio**

`src/pages/portafogli/[slug].astro`:

```astro
---
import Base from '../../layouts/Base.astro';
import { caricaPortafogli, caricaBacktest } from '../../lib/dati';
import { pct } from '../../lib/formato';
import { href } from '../../lib/percorsi';

export function getStaticPaths() {
  return caricaPortafogli().map((p) => ({ params: { slug: p.slug }, props: { portafoglio: p } }));
}
const { portafoglio } = Astro.props;
const bt = caricaBacktest(portafoglio.slug);
---
<Base titolo={portafoglio.nome}>
  <p class="kicker"><a href={href('/portafogli')}>Portafogli</a></p>
  <h1>{portafoglio.nome}</h1>
  <p>{portafoglio.descrizione}</p>

  {bt && (
    <ul class="meta-riga">
      <li><b>CAGR</b> {pct(bt.metriche.cagr)}</li>
      <li><b>Volatilità</b> {pct(bt.metriche.volatilita)}</li>
      <li><b>Max drawdown</b> {pct(bt.metriche.max_drawdown)}</li>
      <li><b>Finestra</b> {bt.finestra[0]} → {bt.finestra[1]}</li>
    </ul>
  )}

  <h2>Composizione</h2>
  <div class="scorri">
    <table>
      <thead>
        <tr><th class="num-h">Peso</th><th>Asset</th><th>ETF reale</th><th>ISIN</th><th>Proxy backtest</th><th>Commento</th></tr>
      </thead>
      <tbody>
        {portafoglio.allocazioni.map((a) => (
          <tr>
            <td class="num">{pct(a.peso)}</td>
            <td>{a.asset}</td>
            <td>{a.etf_reale.nome}</td>
            <td class="mono">{a.etf_reale.isin}</td>
            <td class="mono">{a.proxy}</td>
            <td class="muted">{a.commento ?? ''}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
  <p class="muted">
    Ribilanciamento: {portafoglio.ribilanciamento}. Il ribilanciamento è la parte difficile:
    va fatto davvero, anche quando fa male.
  </p>
</Base>

<style>
  .num-h { text-align: right; }
  .mono { font-family: var(--mono); font-size: .8rem; white-space: nowrap; }
</style>
```

- [ ] **Step 5: Builda e verifica visivamente**

Run: `npm run build`
Expected: PASS con route `/portafogli`, `/portafogli/golden-butterfly-the-bull`, `/portafogli/all-weather-eu`, `/portafogli/lifestrategy-60`, `/portafogli/azionario-globale-100`.

Screenshot della dashboard in ENTRAMBI i temi: grafico log con 4 linee leggibili su entrambi i fondi, legenda, tabella metriche coi numeri veri del Task 6. GUARDA che le linee non si sovrappongano illeggibilmente e che i colori reggano in dark.

- [ ] **Step 6: Micro-commit e merge**

```bash
git add src/lib/dati.ts src/lib/formato.ts src/components/GraficoLinee.astro src/pages/portafogli
git commit -m "feat: dashboard confronto portafogli con grafico SVG log e pagine composizione"
git checkout main
git merge --no-ff feat/portafogli-dashboard -m "merge: feat/portafogli-dashboard"
```

---

### Task 8: Pagine statiche — home, inizia qui, strumenti, lavagna, 404

**Branch:** `feat/pagine-statiche`

**Files:**
- Modify: `src/pages/index.astro` (home definitiva)
- Create: `src/pages/inizia-qui.astro`
- Create: `dati/strumenti.yaml` (copiato da `docs/superpowers/plans/assets/strumenti.yaml`)
- Modify: `src/lib/dati.ts` (aggiunge `caricaStrumenti()`)
- Create: `src/pages/strumenti.astro`
- Create: `contenuti/lavagna/domande-aperte.md`, `contenuti/lavagna/da-fare.md` (da `assets/lavagna/`)
- Create: `src/pages/lavagna.astro`
- Create: `src/pages/404.astro`

**Interfaces:**
- Consumes: collezioni `fonti`/`articoli`/`lavagna` (Task 3), `BadgeTipo` (Task 4), `dati.ts` (Task 5/7), `dataIt` (Task 7), `Base.astro` (Task 2).
- Produces: `caricaStrumenti(): GruppoStrumenti[]` con tipo `{ id: string; nome: string; nota?: string; strumenti: { nome: string; url: string; descrizione: string }[] }[]`.

- [ ] **Step 1: Crea il branch, copia dati e lavagna**

```powershell
git checkout -b feat/pagine-statiche
Copy-Item docs/superpowers/plans/assets/strumenti.yaml dati/strumenti.yaml
Copy-Item docs/superpowers/plans/assets/lavagna/*.md contenuti/lavagna/
```

- [ ] **Step 2: Loader strumenti**

Aggiungi in coda a `src/lib/dati.ts`:

```ts
const Strumento = z.object({ nome: z.string(), url: z.string().url(), descrizione: z.string() });
const GruppoStrumentiSchema = z.object({
  id: z.string(),
  nome: z.string(),
  nota: z.string().optional(),
  strumenti: z.array(Strumento),
});
export type GruppoStrumenti = z.infer<typeof GruppoStrumentiSchema>;

export function caricaStrumenti(): GruppoStrumenti[] {
  const grezzo = yaml.load(readFileSync('dati/strumenti.yaml', 'utf8')) as { gruppi: unknown };
  return z.array(GruppoStrumentiSchema).parse(grezzo.gruppi);
}
```

- [ ] **Step 3: Home definitiva (indice di rivista + ultime aggiunte)**

`src/pages/index.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import BadgeTipo from '../components/BadgeTipo.astro';
import { getCollection } from 'astro:content';
import { href } from '../lib/percorsi';

const fonti = await getCollection('fonti');
const articoli = await getCollection('articoli', (a) => !a.data.bozza);

type Voce = { data: Date; tipo: string; titolo: string; url: string };
const ultime: Voce[] = [
  ...fonti
    .filter((f) => f.data.aggiunta)
    .map((f) => ({
      data: f.data.aggiunta!,
      tipo: f.data.tipo,
      titolo: f.data.titolo,
      url: f.data.stato === 'solo-link' ? f.data.link : href(`/fonti/${f.id}`),
    })),
  ...articoli.map((a) => ({
    data: a.data.data,
    tipo: 'articolo',
    titolo: a.data.titolo,
    url: href(`/articoli/${a.id}`),
  })),
]
  .sort((a, b) => b.data.getTime() - a.data.getTime())
  .slice(0, 6);

const sezioni = [
  ['Inizia qui', '/inizia-qui', 'Il percorso consigliato se parti da zero'],
  ['Fonti', '/fonti', 'Video, podcast, libri e paper — con i concetti da portarsi a casa'],
  ['ETF', '/etf', 'La lista curata, con ISIN, TER e note pratiche'],
  ['Portafogli', '/portafogli', 'Lazy portfolio a confronto, coi nostri backtest'],
  ['Strumenti', '/strumenti', 'Fogli, calcolatori, siti di comparazione, script'],
  ['Articoli', '/articoli', 'Quello che scriviamo noi'],
] as const;
---
<Base titolo="Home">
  <p class="kicker">Second brain di finanza personale</p>
  <h1>Le cose che avremmo voluto sapere prima.</h1>
  <p class="muted sottotitolo">
    Fonti selezionate e riassunte, ETF scelti con criterio, portafogli modello con
    backtest fatti in casa. Curato dal gruppo, per il gruppo.
  </p>

  <ol class="indice">
    {sezioni.map(([nome, percorso, descr]) => (
      <li>
        <a class="nome" href={href(percorso)}>{nome}</a>
        <span class="descr">{descr}</span>
      </li>
    ))}
  </ol>

  <h2>Ultime aggiunte</h2>
  <ul class="aggiunte">
    {ultime.map((v) => (
      <li>
        <span class="data">{v.data.toLocaleDateString('it-IT', { day: '2-digit', month: 'short', year: 'numeric' })}</span>
        <BadgeTipo tipo={v.tipo} />
        <a href={v.url}>{v.titolo}</a>
      </li>
    ))}
  </ul>
</Base>

<style>
  .sottotitolo { font-size: 1.05rem; max-width: 36rem; }
  .aggiunte { list-style: none; padding-left: 0 !important; }
  .aggiunte li { display: flex; gap: 1rem; align-items: baseline; padding: .45rem 0; }
  .data { font-family: var(--mono); font-size: .76rem; color: var(--muted); min-width: 6.4rem; }
</style>
```

- [ ] **Step 4: Inizia qui**

`src/pages/inizia-qui.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { href } from '../lib/percorsi';
---
<Base titolo="Inizia qui" descrizione="Il percorso consigliato dal gruppo per chi parte da zero.">
  <p class="kicker">Percorso</p>
  <h1>Inizia qui</h1>
  <p class="muted">
    Se parti da zero, questo è l'ordine che consigliamo. Non serve fretta:
    prima si capisce, poi si investe. L'ordine è un consiglio, non un dogma.
  </p>
  <ol class="indice">
    <li><span class="nome">Le basi</span><span class="descr">Il videocorso <a href={href('/fonti')}>Educati e Finanziati</a> di Paolo Coletti: gratuito, sistematico, accademico ma comprensibile. Guarda almeno le prime lezioni prima di aprire qualunque conto.</span></li>
    <li><span class="nome">La pratica</span><span class="descr">La playlist <a href={href('/fonti')}>Guida Pratica di The Bull</a>: broker, ordini, piani di accumulo — le cose operative.</span></li>
    <li><span class="nome">L'abitudine</span><span class="descr">Il <a href={href('/fonti')}>podcast di The Bull</a> ogni settimana, partendo dalla selezione del gruppo. La finanza personale si impara per sedimentazione.</span></li>
    <li><span class="nome">Gli strumenti</span><span class="descr">Il <a href={href('/etf')}>catalogo ETF</a> per capire cosa compra la gente come noi, e perché domicilio e TER contano.</span></li>
    <li><span class="nome">Il portafoglio</span><span class="descr">I <a href={href('/portafogli')}>portafogli modello</a> a confronto: non per copiare, ma per capire i compromessi rendimento/volatilità.</span></li>
    <li><span class="nome">La disciplina</span><span class="descr">Scrivi il tuo Investment Policy Statement (modello negli <a href={href('/strumenti')}>strumenti</a>): la strategia si decide a mercati calmi.</span></li>
  </ol>
</Base>
```

- [ ] **Step 5: Strumenti**

`src/pages/strumenti.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { caricaStrumenti } from '../lib/dati';

const gruppi = caricaStrumenti();
---
<Base titolo="Strumenti" descrizione="Fogli, calcolatori, siti di comparazione e script del gruppo.">
  <p class="kicker">Cassetta degli attrezzi</p>
  <h1>Strumenti</h1>
  <p class="muted">Link commentati: fogli di calcolo, calcolatori, siti di analisi. I link Drive richiedono l'accesso del gruppo.</p>
  {gruppi.map((g) => (
    <section>
      <h2>{g.nome}</h2>
      {g.nota && <p class="muted">{g.nota}</p>}
      <ul class="strumenti">
        {g.strumenti.map((s) => (
          <li>
            <a href={s.url} rel="noopener">{s.nome}&thinsp;↗</a>
            <span class="muted"> — {s.descrizione}</span>
          </li>
        ))}
      </ul>
    </section>
  ))}
</Base>

<style>
  .strumenti { list-style: none; padding-left: 0 !important; }
  .strumenti li { padding: .5rem 0; border-bottom: 1px solid var(--hairline); }
</style>
```

- [ ] **Step 6: Lavagna (IDEE.md + collezione lavagna)**

`src/pages/lavagna.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { getCollection, render } from 'astro:content';
import { Content as Idee } from '../../IDEE.md';

const note = await getCollection('lavagna');
const rese = await Promise.all(
  note.map(async (n) => ({ titolo: n.data.titolo, Contenuto: (await render(n)).Content })),
);
---
<Base titolo="Lavagna" descrizione="Idee, cose da fare e domande aperte del gruppo.">
  <p class="kicker">Lavoro in corso</p>
  <h1>Lavagna</h1>
  <p class="muted">
    Il retrobottega del sito: idee, domande senza risposta, cose da scrivere.
    Si modifica dai file in <code>contenuti/lavagna/</code> e da <code>IDEE.md</code>.
  </p>
  {rese.map(({ titolo, Contenuto }) => (
    <section class="hairline-top">
      <h2>{titolo}</h2>
      <Contenuto />
    </section>
  ))}
  <section class="hairline-top">
    <h2>Idee</h2>
    <Idee />
  </section>
</Base>
```

Nota: `import { Content as Idee } from '../../IDEE.md'` funziona perché Astro compila i file `.md` importati direttamente; IDEE.md resta alla radice (è il file che il gruppo già conosce).

- [ ] **Step 7: 404**

`src/pages/404.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { href } from '../lib/percorsi';
---
<Base titolo="Pagina non trovata">
  <p class="kicker">Errore 404</p>
  <h1>Questa pagina non esiste.</h1>
  <p class="muted">Forse è stata spostata, o forse è un'idea non ancora scritta: in quel caso è sulla <a href={href('/lavagna')}>lavagna</a>.</p>
  <p><a href={href('/')}>← Torna alla home</a></p>
</Base>
```

- [ ] **Step 8: Builda, verifica, micro-commit e merge**

Run: `npm run build`
Expected: PASS con le nuove route. Screenshot home in entrambi i temi: indice numerato + ultime aggiunte con date vere (dai frontmatter `aggiunta`).

```bash
git add src/pages dati/strumenti.yaml src/lib/dati.ts contenuti/lavagna
git commit -m "feat: home a indice, inizia-qui, strumenti, lavagna (IDEE.md incluso) e 404"
git checkout main
git merge --no-ff feat/pagine-statiche -m "merge: feat/pagine-statiche"
```

---

### Task 9: Articoli

**Branch:** `feat/articoli`

**Files:**
- Create: `contenuti/articoli/confronto-emittenti-fondi.md` (da `assets/articoli/`)
- Create: `src/pages/articoli/index.astro`
- Create: `src/pages/articoli/[slug].astro`

**Interfaces:**
- Consumes: collezione `articoli` (Task 3), `Base.astro`, `href()`.
- Produces: route `/articoli` e `/articoli/<id>`; la home (Task 8) già linka `/articoli/${a.id}` — gli id sono i nomi file senza estensione.

- [ ] **Step 1: Crea il branch e copia il primo articolo**

```powershell
git checkout -b feat/articoli
Copy-Item docs/superpowers/plans/assets/articoli/confronto-emittenti-fondi.md contenuti/articoli/
```

- [ ] **Step 2: Indice articoli**

`src/pages/articoli/index.astro`:

```astro
---
import Base from '../../layouts/Base.astro';
import { getCollection } from 'astro:content';
import { href } from '../../lib/percorsi';

const articoli = (await getCollection('articoli', (a) => !a.data.bozza)).sort(
  (a, b) => b.data.data.getTime() - a.data.data.getTime(),
);
---
<Base titolo="Articoli" descrizione="Gli articoli scritti dal gruppo.">
  <p class="kicker">Di nostro pugno</p>
  <h1>Articoli</h1>
  <p class="muted">
    Quello che il gruppo scrive quando una domanda merita più di un link.
    Per aggiungerne uno: <a href={href('/come-contribuire')}>come contribuire</a>.
  </p>
  <ul class="elenco">
    {articoli.map((a) => (
      <li>
        <span class="data">{a.data.data.toLocaleDateString('it-IT', { day: '2-digit', month: 'short', year: 'numeric' })}</span>
        <span>
          <a href={href(`/articoli/${a.id}`)}>{a.data.titolo}</a>
          <span class="muted"> — {a.data.autore}</span>
        </span>
      </li>
    ))}
  </ul>
</Base>

<style>
  .elenco { list-style: none; padding-left: 0 !important; }
  .elenco li { display: flex; gap: 1rem; align-items: baseline; padding: .55rem 0; border-bottom: 1px solid var(--hairline); }
  .data { font-family: var(--mono); font-size: .76rem; color: var(--muted); min-width: 6.4rem; }
</style>
```

- [ ] **Step 3: Pagina articolo**

`src/pages/articoli/[slug].astro`:

```astro
---
import Base from '../../layouts/Base.astro';
import { getCollection, render } from 'astro:content';
import { href } from '../../lib/percorsi';

export async function getStaticPaths() {
  const articoli = await getCollection('articoli', (a) => !a.data.bozza);
  return articoli.map((a) => ({ params: { slug: a.id }, props: { articolo: a } }));
}
const { articolo } = Astro.props;
const { Content } = await render(articolo);
---
<Base titolo={articolo.data.titolo}>
  <p class="kicker"><a href={href('/articoli')}>Articoli</a></p>
  <h1>{articolo.data.titolo}</h1>
  <ul class="meta-riga">
    <li><b>Autore</b> {articolo.data.autore}</li>
    <li><b>Data</b> {articolo.data.data.toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' })}</li>
    {articolo.data.tag.length > 0 && <li>{articolo.data.tag.map((t) => <span class="badge">{t}</span>)}</li>}
  </ul>
  <Content />
</Base>
```

- [ ] **Step 4: Builda, verifica, micro-commit e merge**

Run: `npm run build`
Expected: PASS; route `/articoli` e `/articoli/confronto-emittenti-fondi`; l'articolo compare anche nelle "Ultime aggiunte" della home.

```bash
git add contenuti/articoli src/pages/articoli
git commit -m "feat: sezione articoli con primo articolo migrato (confronto emittenti)"
git checkout main
git merge --no-ff feat/articoli -m "merge: feat/articoli"
```

---

### Task 10: Ricerca (Pagefind)

**Branch:** `feat/ricerca`

**Files:**
- Create: `src/pages/cerca.astro`

**Interfaces:**
- Consumes: `Base.astro` (che ha già `data-pagefind-body` sul `<main>`, Task 2); lo script `build` di `package.json` già esegue `pagefind --site dist` (Task 1).
- Produces: pagina `/cerca` con l'interfaccia Pagefind.

- [ ] **Step 1: Crea il branch e la pagina**

```bash
git checkout -b feat/ricerca
```

`src/pages/cerca.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { href } from '../lib/percorsi';
const bundle = href('/pagefind/');
---
<Base titolo="Cerca">
  <p class="kicker">Ricerca</p>
  <h1>Cerca nel sito</h1>
  <p class="muted piccola">
    La ricerca indicizza tutto: fonti, articoli, ETF, lavagna.
    Funziona sul sito pubblicato (in sviluppo locale: <code>npm run build && npm run preview</code>).
  </p>
  <div id="ricerca"></div>
</Base>

<link rel="stylesheet" href={href('/pagefind/pagefind-ui.css')} />
<script is:inline src={href('/pagefind/pagefind-ui.js')}></script>
<script is:inline define:vars={{ bundle }}>
  window.addEventListener('DOMContentLoaded', () => {
    if (window.PagefindUI) {
      new window.PagefindUI({
        element: '#ricerca',
        bundlePath: bundle,
        showSubResults: true,
        translations: {
          placeholder: 'Cerca…',
          zero_results: 'Nessun risultato per «[SEARCH_TERM]»',
        },
      });
    } else {
      document.getElementById('ricerca').innerHTML =
        '<p class="muted">Indice di ricerca non trovato: in locale serve <code>npm run build</code>.</p>';
    }
  });
</script>

<style is:global>
  #ricerca { --pagefind-ui-primary: var(--accent); --pagefind-ui-text: var(--ink); --pagefind-ui-background: var(--bg); --pagefind-ui-border: var(--hairline); --pagefind-ui-font: inherit; }
</style>
```

- [ ] **Step 2: Builda e prova la ricerca sul sito buildato**

Run: `npm run build`
Expected: PASS; log Pagefind con decine di pagine indicizzate.

Run: `npm run preview`, apri `/investiamo-pagio/cerca`, cerca "VWCE" e "witholding".
Expected: risultati pertinenti (pagina ETF, schede fonte).

- [ ] **Step 3: Micro-commit e merge**

```bash
git add src/pages/cerca.astro
git commit -m "feat: pagina di ricerca Pagefind in italiano"
git checkout main
git merge --no-ff feat/ricerca -m "merge: feat/ricerca"
```

---

### Task 11: Guida contributi per non-programmatori

**Branch:** `docs/guida-contributi`

**Files:**
- Create: `CONTRIBUIRE.md`
- Create: `src/pages/come-contribuire.astro`

**Interfaces:**
- Consumes: template del Task 3, `Base.astro`.
- Produces: pagina `/come-contribuire` (già linkata dal footer, dal catalogo fonti e dagli articoli) che rende CONTRIBUIRE.md.

**Nota (deviazione consapevole dalla spec):** la spec prevede screenshot; qui la guida nasce testuale con i nomi esatti dei bottoni GitHub. Gli screenshot veri li aggiunge un membro del gruppo al primo giro (voce già in lavagna/da-fare tramite questo task, Step 2).

- [ ] **Step 1: Scrivi CONTRIBUIRE.md**

`CONTRIBUIRE.md`:

```markdown
# Come contribuire (anche se non hai mai programmato)

Il sito si aggiorna da solo ogni volta che qualcuno salva un file:
tu scrivi, il resto è automatico. Serve solo un account GitHub.

## Una volta sola: l'account

1. Vai su https://github.com/signup e crea un account gratuito.
2. Manda il tuo nome utente nel gruppo: chi amministra il repo ti
   aggiunge come collaboratore (arriva una mail "invitation", accettala).

## Aggiungere una fonte (video, podcast, libro, paper, sito)

1. Apri il repo su GitHub e entra nella cartella `template/`.
2. Apri `template-fonte.md` e copia tutto il contenuto (icona con i due
   quadratini, "Copy raw file").
3. Torna alla cartella `contenuti/fonti/`. In alto a destra:
   **Add file → Create new file**.
4. Nome del file: minuscole e trattini, per esempio
   `psicologia-dei-soldi.md`.
5. Incolla il template, compila i campi, cancella le righe che iniziano
   con `#`. Il riassunto va sotto i tre trattini di chiusura.
6. In alto a destra: **Commit changes…** → di nuovo **Commit changes**.
7. Fatto. Dopo un paio di minuti la fonte è sul sito (ricarica la pagina).

## Scrivere un articolo

Identico, ma si parte da `template/template-articolo.md` e si salva
in `contenuti/articoli/`.

## Correggere una pagina esistente

1. Trova il file in `contenuti/` e aprilo.
2. Clicca la matita in alto a destra (**Edit this file**).
3. Correggi, poi **Commit changes…**.

## Se qualcosa va storto

- Il sito non si aggiorna dopo 5 minuti? Probabilmente un campo del
  frontmatter è scritto male (il sistema rifiuta la modifica per
  proteggere il sito, che resta alla versione precedente). Apri il tuo
  file, controlla i due punti e le virgolette, oppure scrivi nel gruppo:
  chi è di turno guarda l'errore nella tab **Actions** del repo.
- Non si rompe niente di irreparabile: ogni modifica è reversibile.

## Regole della casa

- Niente PDF o materiale coperto da copyright nel repo: si linka
  l'originale (per il materiale del gruppo: il Drive privato).
- Niente consigli d'investimento personali: fonti, fatti, ragionamenti.
- In dubbio? Scrivi sulla lavagna (`contenuti/lavagna/`) o nel gruppo.
```

- [ ] **Step 2: Aggiungi il promemoria screenshot alla lavagna**

Aggiungi in coda a `contenuti/lavagna/da-fare.md`:

```markdown
- Aggiungere screenshot veri (passo per passo) alla guida "Come contribuire".
```

- [ ] **Step 3: Pagina che rende la guida**

`src/pages/come-contribuire.astro`:

```astro
---
import Base from '../layouts/Base.astro';
import { Content as Guida } from '../../CONTRIBUIRE.md';
---
<Base titolo="Come contribuire" descrizione="Aggiungere una fonte o un articolo in due minuti, senza saper programmare.">
  <p class="kicker">Partecipa</p>
  <Guida />
</Base>
```

- [ ] **Step 4: Builda, verifica, micro-commit e merge**

Run: `npm run build`
Expected: PASS; `/come-contribuire` rende la guida; il link nel footer funziona da ogni pagina.

```bash
git add CONTRIBUIRE.md src/pages/come-contribuire.astro contenuti/lavagna/da-fare.md
git commit -m "docs: guida contributi per non-programmatori + pagina sul sito"
git checkout main
git merge --no-ff docs/guida-contributi -m "merge: docs/guida-contributi"
```

---

### Task 12: Deploy su GitHub Pages, README e verifica finale

**Branch:** `feat/deploy`

**Files:**
- Create: `.github/workflows/deploy.yml`
- Create: `README.md`

**Interfaces:**
- Consumes: tutto.
- Produces: pubblicazione automatica su push a `main`; job `pytest` che blocca il deploy se i calcoli di backtest si rompono.

- [ ] **Step 1: Crea il branch e il workflow**

```bash
git checkout -b feat/deploy
```

`.github/workflows/deploy.yml`:

```yaml
name: Pubblica il sito

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  test-backtest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r backtest/requirements.txt
      - run: python -m pytest backtest/tests -q

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: [build, test-backtest]
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Scrivi il README**

`README.md`:

```markdown
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
- Spec e piani: `docs/superpowers/`

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
```

- [ ] **Step 3: Verifica finale completa in locale**

```powershell
npm run build
python -m pytest backtest/tests -q
```
Expected: build PASS, `6 passed`.

Checklist manuale con `npm run preview` (spuntare tutte):
- [ ] Home: indice + ultime aggiunte, date giuste
- [ ] Fonti: filtri funzionano, 29 schede (10 migrate + 19 paper)
- [ ] ETF: filtro label, ricerca, copia ISIN
- [ ] Portafogli: grafico leggibile, 4 righe in tabella, link alle pagine singole
- [ ] Strumenti, Lavagna (IDEE.md visibile), Articoli, Come contribuire, Cerca, 404
- [ ] Tema scuro: OGNI pagina sopra, di nuovo (toggle ◐)
- [ ] Screenshot finali di home, ETF e dashboard nei due temi: guardali davvero

- [ ] **Step 4: Micro-commit e merge**

```bash
git add .github/workflows/deploy.yml README.md
git commit -m "feat: workflow GitHub Pages (pytest + build + deploy) e README"
git checkout main
git merge --no-ff feat/deploy -m "merge: feat/deploy"
```

- [ ] **Step 5: Consegna all'utente**

Il push su GitHub e l'attivazione di Pages li fa l'utente (serve il suo account):
istruzioni pronte nel README, sezione "Pubblicazione (prima volta)".

---

## Fuori da questo piano (promemoria)

- Riassunti delle fonti: arrivano quando l'utente passa la lista dei video
  (promemoria in `IDEE.md`); ogni riassunto = modifica di una scheda esistente
  (`stato: riassunto` + corpo), zero codice.
- Screenshot veri nella guida contributi (voce in lavagna).
- Download di Excel e simulazioni dal Drive in `drive-locale/` (gitignored).
- CMS grafico, commenti, analytics: esplicitamente fuori scope v1 (spec §11).



