#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estilo académico del sitio de exploradores de Teoría Electromagnética (idempotente).

1. Sustituye la raya (—) por la puntuación académica correspondiente (dos puntos,
   comas o punto medio); los intervalos conservan la semirraya (–). Se respeta el
   título original de una referencia citada (marshmallows—A take-home lab).
2. En el texto visible del HTML convierte subíndices y superíndices escritos a mano
   (Z_L, Z_in(d), v_p, e^(−z/δ)) y los subíndices Unicode (Z₀, η₁, TE₁₀) en
   <sub>/<sup>, para que toda la notación tenga el mismo tamaño y posición.
   No toca <title>, <script>, <style>, <textarea>, <option>, <pre>, <code>, <svg> ni atributos.

Uso: python3 estilo_academico_em.py [--dir RUTA] [--seco]   (--seco solo informa)
"""
import os, re, sys

ARCHIVOS_EXT = (".html", ".py", ".md", ".cff", ".json")
NO_TOCAR = {"estilo_academico_em.py"}
CITA_ORIGINAL = "marshmallows—A take-home lab"

def limpiar_rayas(s):
    s = s.replace(CITA_ORIGINAL, "\0CITA\0")
    reglas = [
        (r" — Explorador interactivo", ": explorador interactivo"),
        (r"Electromagnética — Exploradores interactivos", "Electromagnética: exploradores interactivos"),
        (r"México — ENES Juriquilla", "México, ENES Juriquilla"),
        (r"científica — Miniproyecto", "científica: miniproyecto"),
        (r"\*\* — (CFATA|ENES Juriquilla), UNAM — ORCID", r"**, \1, UNAM. ORCID"),
        (r"(?m)^(##[^\n]*?) — ", r"\1 · "),
        (r"</a> —: ", "</a>: "),
        (r"geometría —refracción", "geometría (refracción"),
        (r"segunda fibra\)—;", "segunda fibra));"),
        (r"polarización —coeficientes", "polarización (coeficientes"),
        (r"XXXXXXX — o cualquier DOI de Zenodo\nanterior — en", "XXXXXXX, o cualquier DOI de Zenodo\nanterior, en"),
        (r"(['\"])—\1", r"\1…\1"),          # marcador de valor vacío en JS
        (r">—<", ">…<"),                     # marcador de valor vacío en HTML
        (r"(['\"])— \(", r"\1("),            # '— (TIR)' -> '(TIR)'
    ]
    for a, b in reglas:
        s = re.sub(a, b, s)
    # incisos entre rayas en una misma línea: « — X — » -> «, X, »
    s = re.sub(r" — ([^—\n<]{1,160}?) — ", r", \1, ", s)
    # raya restante: coma si sigue una conjunción, dos puntos en otro caso
    s = re.sub(r" — (?=(y|o|porque|pero|si|aunque|sino)\b)", ", ", s)
    s = re.sub(r" — ", ": ", s)
    s = re.sub(r"(\S)—(\S)", r"\1, \2", s)
    return s.replace("\0CITA\0", CITA_ORIGINAL)

SUBS = dict(zip("₀₁₂₃₄₅₆₇₈₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ", "0123456789aeoxhklmnpstiruvj"))
SALTA = {"title", "script", "style", "textarea", "option", "pre", "code", "svg"}
RE_TAG = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>", re.S)
RE_US = re.compile(r"(?<![\w./-])([A-Za-zΑ-Ωα-ω])_(\{[^}<]{1,12}\}|[A-Za-z0-9áéíóúñ]{1,6})(?![\w.]*\.(html|py|png|csv))")
RE_SUP = re.compile(r"\^(\{[^}<]{1,14}\}|\([^)<]{1,14}\)|−?\d{1,3})")

def notacion(texto):
    texto = RE_US.sub(lambda m: m.group(1) + "<sub>" + m.group(2).strip("{}") + "</sub>", texto)
    texto = RE_SUP.sub(lambda m: "<sup>" + m.group(1).strip("{}()") + "</sup>", texto)
    texto = re.sub("[" + "".join(SUBS) + "]+", lambda m: "<sub>" + "".join(SUBS[c] for c in m.group(0)) + "</sub>", texto)
    return texto

def svg_notacion(t):
    t = RE_US.sub(lambda m: m.group(1) + '<tspan baseline-shift="sub" font-size="72%">' + m.group(2).strip("{}") + "</tspan>", t)
    return t

def html_notacion(s):
    out, pila, pos = [], [], 0
    while True:
        m = RE_TAG.search(s, pos)
        if not m:
            out.append(s[pos:] if pila else notacion(s[pos:]))
            break
        txt = s[pos:m.start()]
        if pila and pila[-1] == "svg":
            out.append(svg_notacion(txt) if re.search(r"<text\b[^>]*>$", s[max(0, pos - 200):pos]) else txt)
        else:
            out.append(txt if pila else notacion(txt))
        out.append(m.group(0)); pos = m.end()
        if m.group(0).startswith("<!--"):
            continue
        cierre, nombre, auto = m.group(1), (m.group(2) or "").lower(), m.group(3)
        if nombre in ("script", "style") and not cierre:
            fin = re.compile(r"</%s\s*>" % nombre, re.I).search(s, pos)
            if fin:
                out.append(s[pos:fin.start()]); pos = fin.start()
            continue
        if nombre in SALTA:
            if cierre:
                if nombre in pila: pila.remove(nombre)
            elif not auto:
                pila.append(nombre)
    return "".join(out)

def main():
    a = sys.argv[1:]; d = "."
    if "--dir" in a:
        i = a.index("--dir"); d = a[i + 1]
    seco = "--seco" in a
    cambios = 0
    for raiz, _, fs in os.walk(d):
        if "auditoria" in raiz.split(os.sep) or "/." in raiz:
            continue
        for f in fs:
            if not f.endswith(ARCHIVOS_EXT) or f in NO_TOCAR:
                continue
            p = os.path.join(raiz, f)
            s0 = open(p, encoding="utf-8").read()
            s = limpiar_rayas(s0)
            if f.endswith(".html") and not f.startswith("AnatomiaGrafica"):
                s = html_notacion(s)
            if s != s0:
                cambios += 1
                if not seco:
                    open(p, "w", encoding="utf-8").write(s)
                print(("cambiaría " if seco else "actualizado ") + p)
    print(cambios, "archivos", "por cambiar" if seco else "actualizados")

if __name__ == "__main__":
    main()
