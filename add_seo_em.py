#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara el sitio de exploradores de Teoría EM para buscadores (Google):
título descriptivo, meta description, URL canónica, Open Graph y datos
estructurados schema.org (LearningResource) en cada página, y sitemap.xml.

Uso (desde la carpeta del repo):
    python3 add_seo_em.py                         añade/actualiza todo
    python3 add_seo_em.py --google CODIGO         además, la verificación de
                                                  Google Search Console en index.html
    python3 add_seo_em.py --quitar                elimina los bloques

Idempotente (bloques delimitados por marcadores). Al añadir un explorador,
agregarlo a PAGINAS y re-correr.
"""
import os, re, sys, json, datetime

BASE = "https://elodiestrupiechonski.github.io/Teoria-Electromagnetica/"
DOI = "https://doi.org/10.5281/zenodo.23423156"
SITIO = "Exploradores de Teoría Electromagnética (UNAM)"
INI, FIN = "<!-- seo:inicio -->", "<!-- seo:fin -->"

# archivo: (título, descripción ≤ ~160 caracteres, temas)
PAGINAS = {
 "index.html": ("Teoría Electromagnética — Exploradores interactivos (ENES Juriquilla, UNAM)",
   "19 simuladores gratuitos de electromagnetismo en español: Gauss, inducción, ondas planas, Fresnel, líneas de transmisión, carta de Smith y guías de onda.",
   ["electromagnetismo", "ondas electromagnéticas", "líneas de transmisión"]),
 "CampoGauss_explorador.html": ("Ley de Gauss: simulador interactivo de flujo eléctrico",
   "Arrastra una superficie gaussiana alrededor de una carga puntual, una esfera cargada o una lámina y comprueba que el flujo solo depende de la carga encerrada.",
   ["ley de Gauss", "campo eléctrico", "flujo eléctrico"]),
 "Capacitor_explorador.html": ("Capacitor de placas paralelas con dieléctrico: simulador",
   "Inserta un dieléctrico entre las placas y compara voltaje fijo y carga fija: capacitancia, campo, carga y energía, con aviso de ruptura del aire.",
   ["capacitor", "dieléctrico", "capacitancia"]),
 "Solenoide_explorador.html": ("Campo magnético de un solenoide finito: efecto de borde",
   "Compara el campo real B(z) de un solenoide corto con el ideal μ₀nI y entiende el factor de borde cos α a partir de Biot–Savart.",
   ["solenoide", "campo magnético", "Biot-Savart"]),
 "Induccion_explorador.html": ("Ley de Faraday: inducción con imán y osciloscopio interactivo",
   "Acerca un imán a una espira o aplica un B(t) senoidal y observa el flujo y la FEM inducida sincronizados, con el sentido de la ley de Lenz.",
   ["ley de Faraday", "inducción electromagnética", "ley de Lenz"]),
 "RC_interactivo.html": ("Circuito RC en serie: desfase, fasores y osciloscopio",
   "Ajusta R, C y la frecuencia y observa cómo la corriente adelanta al voltaje: osciloscopio virtual, diagrama fasorial y triángulo de impedancias.",
   ["circuito RC", "fasores", "impedancia"]),
 "MicroondasC_explorador.html": ("Medir la velocidad de la luz con un horno de microondas",
   "Onda estacionaria dentro del horno: mide la distancia entre puntos calientes y calcula c = 2·d·f con tus propios datos.",
   ["velocidad de la luz", "onda estacionaria", "microondas"]),
 "EfectoPiel_explorador.html": ("Efecto piel y profundidad de penetración: simulador",
   "Cómo se atenúa una onda dentro de un conductor: profundidad de penetración δ contra frecuencia y material, con la expresión general de α y β.",
   ["efecto piel", "profundidad de penetración", "blindaje electromagnético"]),
 "Polarizacion_explorador.html": ("Polarización lineal, circular y elíptica: simulador",
   "Cambia amplitudes y desfase y observa la figura que traza el campo eléctrico; pérdida por polarización en un enlace satelital.",
   ["polarización", "ondas electromagnéticas", "antenas"]),
 "Doppler_explorador.html": ("Efecto Doppler relativista y corrimiento al rojo: simulador",
   "Frentes de onda de una fuente en movimiento, la señal de cada observador, el corrimiento al rojo de galaxias y el Doppler de un radar.",
   ["efecto Doppler", "corrimiento al rojo", "radar"]),
 "Reflexion_interactivo.html": ("Reflexión de ondas planas con incidencia normal: simulador",
   "Onda estacionaria, coeficientes de reflexión y transmisión, razón de onda estacionaria e impedancia de onda η(d) en un plano móvil.",
   ["reflexión", "coeficiente de reflexión", "onda estacionaria"]),
 "CapaTresMedios_interactivo.html": ("Capa dieléctrica entre dos medios: radomo y antirreflejante",
   "Mueve la segunda interfaz y elige materiales para ver la impedancia efectiva: capa de media onda transparente y capa de cuarto de onda antirreflejante.",
   ["recubrimiento antirreflejante", "radomo", "capa de cuarto de onda"]),
 "CapaDielectrica_explorador.html": ("Impedancia efectiva de una capa dieléctrica: curva de diseño",
   "Potencia reflejada contra el espesor de la capa, con los ceros en λ/2 y λ/4 y la condición η₂ = √(η₁η₃).",
   ["impedancia de onda", "capa dieléctrica", "adaptación de impedancias"]),
 "Snell_explorador.html": ("Ley de Snell, reflexión total interna y ángulo de Brewster",
   "Trazado de rayos interactivo: refracción, ángulo crítico, reflexión total interna (fibra óptica) y ángulo de Brewster.",
   ["ley de Snell", "reflexión total interna", "fibra óptica"]),
 "Fresnel_explorador.html": ("Coeficientes de Fresnel: reflexión contra ángulo de incidencia",
   "Potencia reflejada de las polarizaciones perpendicular y paralela contra el ángulo, con el ángulo de Brewster y el ángulo crítico.",
   ["ecuaciones de Fresnel", "ángulo de Brewster", "incidencia oblicua"]),
 "LineaTransmision_interactivo.html": ("Línea de transmisión: coeficiente de reflexión y VSWR",
   "Onda estacionaria de voltaje en una línea con carga compleja: Γ, VSWR, mínimos de voltaje e impedancia de entrada Z_in(d).",
   ["línea de transmisión", "VSWR", "impedancia de entrada"]),
 "Smith_explorador.html": ("Carta de Smith interactiva",
   "La carga como un punto en el plano de Γ: arrástrala, gira hacia el generador y lee la impedancia de entrada y el VSWR sobre la carta.",
   ["carta de Smith", "adaptación de impedancias", "líneas de transmisión"]),
 "GuiaOnda_explorador.html": ("Guía de onda rectangular: modos y frecuencia de corte",
   "Frecuencias de corte TE y TM, banda monomodo, longitud de onda guiada y velocidades de fase y de grupo en guías WR-90, WR-284 y WR-42.",
   ["guía de onda", "frecuencia de corte", "modo TE10"]),
 "Espectro_explorador.html": ("Espectro electromagnético interactivo: λ, f, energía y color",
   "Convierte entre longitud de onda, frecuencia, energía del fotón y número de onda; bandas, tecnologías y zoom del visible con nombres de colores.",
   ["espectro electromagnético", "longitud de onda", "energía del fotón"]),
 "AnatomiaGrafica_explorador.html": ("Anatomía de una gráfica científica con Python y matplotlib",
   "Miniproyecto guiado: construye paso a paso una figura científica (profundidad de penetración) con ejes, escalas, leyenda y el código matplotlib.",
   ["matplotlib", "gráficas científicas", "Python"]),
}

def bloque(f, titulo, desc, temas):
    url = BASE + ("" if f == "index.html" else f)
    ld = {
      "@context": "https://schema.org",
      "@type": "LearningResource",
      "name": titulo, "description": desc, "url": url,
      "inLanguage": "es", "isAccessibleForFree": True,
      "learningResourceType": "simulación interactiva",
      "educationalLevel": "Licenciatura",
      "about": temas,
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "identifier": DOI,
      "isPartOf": {"@type": "Collection", "name": "Teoría Electromagnética — Exploradores interactivos", "url": BASE},
      "author": [
        {"@type": "Person", "name": "Elodie Strupiechonski", "sameAs": "https://orcid.org/0000-0001-8991-8499"},
        {"@type": "Person", "name": "Andrés de Luna Bugallo", "sameAs": "https://orcid.org/0000-0002-7591-5235"}],
      "provider": {"@type": "CollegeOrUniversity", "name": "Universidad Nacional Autónoma de México — ENES Juriquilla"}
    }
    esc = lambda t: t.replace("&", "&amp;").replace('"', "&quot;")
    return f'''{INI}
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(SITIO)}">
<meta property="og:title" content="{esc(titulo)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="es_MX">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
{FIN}'''

def quitar(s):
    s = re.sub(re.escape(INI) + r".*?" + re.escape(FIN) + r"\n?", "", s, flags=re.S)
    return re.sub(r'<meta name="google-site-verification"[^>]*>\n?', "", s)

def main():
    args = sys.argv[1:]
    d = "."
    if "--dir" in args:
        i = args.index("--dir"); d = args[i+1]; del args[i:i+2]
    google = None
    if "--google" in args:
        i = args.index("--google"); google = args[i+1]; del args[i:i+2]
    faltan = [f for f in sorted(os.listdir(d)) if f.endswith(".html") and f not in PAGINAS]
    if faltan and "--quitar" not in args:
        sys.exit("páginas sin datos en PAGINAS: " + ", ".join(faltan))
    for f, (tit, desc, temas) in PAGINAS.items():
        p = os.path.join(d, f)
        if not os.path.exists(p): continue
        s = quitar(open(p, encoding="utf-8").read())
        if "--quitar" not in args:
            s = re.sub(r"<title>.*?</title>", "<title>" + tit.replace("&", "&amp;") + "</title>", s, count=1, flags=re.S)
            extra = bloque(f, tit, desc, temas)
            if f == "index.html" and google:
                extra = '<meta name="google-site-verification" content="%s">\n' % google + extra
            s = re.sub(r"(</title>)", r"\1\n" + extra.replace("\\", "\\\\"), s, count=1)
        open(p, "w", encoding="utf-8").write(s)
    if "--quitar" not in args:
        hoy = datetime.date.today().isoformat()
        urls = "\n".join('  <url><loc>%s</loc><lastmod>%s</lastmod></url>' %
                         (BASE + ("" if f == "index.html" else f), hoy) for f in PAGINAS)
        open(os.path.join(d, "sitemap.xml"), "w", encoding="utf-8").write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n")
    print(("datos para buscadores quitados de" if "--quitar" in args else "datos para buscadores y sitemap.xml en"),
          len(PAGINAS), "páginas", "(con verificación de Google)" if google else "")

if __name__ == "__main__":
    main()
