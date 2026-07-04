/** Antepone il base path di GitHub Pages: href('/fonti') → '/investiamo-pagio/fonti'. */
export function href(percorso: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return base + percorso;
}
