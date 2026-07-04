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
