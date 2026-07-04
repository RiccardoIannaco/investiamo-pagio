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
