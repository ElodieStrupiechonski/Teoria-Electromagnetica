#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fija UNA sola cadena de versión en todo el sitio de exploradores de
Teoría EM: bloques «Cómo citar» de todas las páginas, README.md,
.zenodo.json y CITATION.cff (incluida la fecha de publicación).

Uso (desde la carpeta del repo):
    python3 set_version_em.py 1.3.1 2026-10-20
    python3 set_version_em.py 1.3.1 2026-10-20 --dir RUTA

No modifica CHANGELOG.md (su historial cita versiones anteriores a propósito).

Idempotente: puede correrse de nuevo con una versión más reciente.
"""
import os, re, sys

def main():
    if len(sys.argv) < 3 or not re.fullmatch(r"\d+(\.\d+){1,2}", sys.argv[1]) \
       or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sys.argv[2]):
        sys.exit(__doc__)
    ver, fecha = sys.argv[1], sys.argv[2]
    d = sys.argv[sys.argv.index("--dir")+1] if "--dir" in sys.argv else "."
    n = 0
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if f.endswith((".html", ".md")) and f != "CHANGELOG.md":
            s0 = open(p, encoding="utf-8").read()
            s = re.sub(r"Versión \d+(?:\.\d+){1,2}", "Versión " + ver, s0)
            if s != s0: open(p, "w", encoding="utf-8").write(s); n += 1
        elif f in ("zenodo.json", ".zenodo.json"):
            s0 = open(p, encoding="utf-8").read()
            s = re.sub(r'"version":\s*"\d+(?:\.\d+){1,2}"', '"version": "%s"' % ver, s0)
            if s != s0: open(p, "w", encoding="utf-8").write(s); n += 1
        elif f == "CITATION.cff":
            s0 = open(p, encoding="utf-8").read()
            s = re.sub(r'version:\s*"\d+(?:\.\d+){1,2}"', 'version: "%s"' % ver, s0)
            s = re.sub(r'date-released:\s*"\d{4}-\d{2}-\d{2}"', 'date-released: "%s"' % fecha, s)
            if s != s0: open(p, "w", encoding="utf-8").write(s); n += 1
    print("versión %s (fecha %s) fijada en %d archivos en %s" % (ver, fecha, n, os.path.abspath(d)))

if __name__ == "__main__":
    main()
