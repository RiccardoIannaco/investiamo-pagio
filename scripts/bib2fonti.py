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
    if not url:
        doi = pulisci(campi.get("doi", ""))
        if not doi:
            raise SystemExit(f"ERRORE: la voce {chiave} non ha né url né doi")
        url = f"https://doi.org/{doi}"
    rivista = pulisci(campi.get("journal", campi.get("publisher", "")))
    slug = chiave.strip().replace("_", "-").lower()
    dove = f", pubblicato su *{rivista}*" if rivista else ""
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
