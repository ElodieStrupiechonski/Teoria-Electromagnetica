#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Asegura que todas las páginas del sitio de exploradores de Teoría EM estén
bien formadas para el móvil: <!doctype html>, <html lang="es"> y la etiqueta
<meta name="viewport">, más una regla CSS para que las cajas de ecuaciones
envuelvan en pantallas angostas.

Uso (desde la carpeta del repo):
    python3 add_doctype_em.py              añade lo que falte
    python3 add_doctype_em.py --dir RUTA   otra carpeta

Idempotente: las páginas que ya tienen doctype/lang/viewport no se duplican;
el bloque CSS móvil va delimitado por marcadores y se reemplaza al re-correr.
"""
import os, re, sys

INI, FIN = "<!-- movil:inicio -->", "<!-- movil:fin -->"
VIEWPORT = '<meta name="viewport" content="width=device-width, initial-scale=1">'
CSS = f'''{INI}
<style>
  .card{{min-width:0}}
  pre{{overflow-x:auto;max-width:100%}}
  /* evitar que inputs/selects fijen un ancho mínimo que desborde en teléfono */
  .calc-grid label,.inrow,.inbox,.ctl,.controls>*{{min-width:0}}
  .calc-grid input,.calc-grid select{{width:100%;min-width:0;box-sizing:border-box}}
  input[type=number],select{{max-width:100%;min-width:0}}
  @media (max-width:480px){{
    .eq{{font-size:14px;overflow-wrap:anywhere;white-space:normal}}
    .tiles{{grid-template-columns:1fr 1fr}}
  }}
</style>
{FIN}'''

def arregla(s):
    # quitar bloque móvil previo
    s = re.sub(re.escape(INI) + r".*?" + re.escape(FIN) + r"\n?", "", s, flags=re.S)
    tiene_doctype = re.match(r"\s*<!doctype html>", s, re.I)
    if not tiene_doctype:
        s = "<!doctype html>\n" + s
    if not re.search(r"<html\b", s, re.I):
        s = s.replace("<!doctype html>\n", '<!doctype html>\n<html lang="es">\n', 1)
    if 'name="viewport"' not in s:
        # después del charset si existe; si no, tras <html>
        if '<meta charset="utf-8">' in s:
            s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + VIEWPORT, 1)
        else:
            s = re.sub(r'(<html[^>]*>\n?)', r"\1" + VIEWPORT + "\n", s, count=1)
    # bloque CSS móvil justo después de la etiqueta de viewport existente
    s = re.sub(r'(<meta name="viewport"[^>]*>)', r"\1\n" + CSS.replace("\\", "\\\\"), s, count=1)
    return s

def main():
    args = sys.argv[1:]
    d = "."
    if "--dir" in args:
        i = args.index("--dir"); d = args[i+1]
    htmls = sorted(f for f in os.listdir(d) if f.endswith(".html"))
    if not htmls:
        sys.exit("no hay archivos .html en " + os.path.abspath(d))
    n = 0
    for f in htmls:
        p = os.path.join(d, f)
        s0 = open(p, encoding="utf-8").read()
        s = arregla(s0)
        if s != s0:
            open(p, "w", encoding="utf-8").write(s); n += 1
    print("estructura móvil asegurada en", n, "de", len(htmls), "páginas en", os.path.abspath(d))

if __name__ == "__main__":
    main()
