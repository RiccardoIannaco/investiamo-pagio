/** 0.067 → "6,7%" (frazione decimale → percento it-IT) */
export function pct(v: number): string {
  return (v * 100).toLocaleString('it-IT', { maximumFractionDigits: 1 }) + '%';
}

/** "2026-07-04" → "4 luglio 2026" */
export function dataIt(iso: string): string {
  return new Date(iso).toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' });
}
