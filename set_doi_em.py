#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fija el DOI de Zenodo en todas las páginas y metadatos del sitio de
exploradores de Teoría Electromagnética.

Uso (desde la carpeta del repo):
    python3 set_doi_em.py 10.5281/zenodo.23423157
    python3 set_doi_em.py 10.5281/zenodo.23423157 --dir RUTA

Reemplaza el marcador 10.5281/zenodo.XXXXXXX — o cualquier DOI de Zenodo
anterior — en .html, .md, .cff y .json; quita la nota «(se completa al
publicar en Zenodo)»; en las páginas HTML convierte el DOI en enlace a
doi.org, y añade la insignia de Zenodo al inicio del README si no está.
Es idempotente: puede correrse de nuevo con un DOI más reciente.
"""
import os, re, sys

PAT = re.compile(r"10\.5281/zenodo\.(XXXXXXX|\d+)")
NOTA = re.compile(r"\s*\(se completa al publicar en Zenodo\)\.?")

def main():
    if len(sys.argv) < 2 or not re.fullmatch(r"10\.5281/zenodo\.\d+", sys.argv[1]):
        sys.exit(__doc__)
    doi = sys.argv[1]
    d = sys.argv[sys.argv.index("--dir")+1] if "--dir" in sys.argv else "."
    enlace = f'<a href="https://doi.org/{doi}" target="_blank" rel="noopener">{doi}</a>'
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith((".html", ".md", ".cff", ".json")):
            continue
        p = os.path.join(d, f)
        s0 = open(p, encoding="utf-8").read()
        s = NOTA.sub("", PAT.sub(doi, s0))
        if f.endswith(".html"):
            # DOI como enlace (sin duplicar si ya es enlace)
            s = re.sub(r"(?<!>)" + re.escape(doi) + r"(?!</a>)",
                       enlace.replace("\\", "\\\\"), s) if f'href="https://doi.org/{doi}"' not in s else s
        if f == "README.md" and "zenodo.org/badge" not in s:
            badge = f"[![DOI](https://zenodo.org/badge/DOI/{doi}.svg)](https://doi.org/{doi})\n\n"
            s = re.sub(r"^(# .+\n)", r"\1\n" + badge, s, count=1)
        if s != s0:
            open(p, "w", encoding="utf-8").write(s); n += 1
    resto = sum(open(os.path.join(d, f), encoding="utf-8").read().count("XXXXXXX")
                for f in os.listdir(d) if f.endswith((".html", ".md", ".cff", ".json")))
    print(f"DOI {doi} fijado en {n} archivos; marcadores restantes: {resto}")

if __name__ == "__main__":
    main()
