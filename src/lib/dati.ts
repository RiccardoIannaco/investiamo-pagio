import { existsSync, readFileSync, readdirSync } from 'node:fs';
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
