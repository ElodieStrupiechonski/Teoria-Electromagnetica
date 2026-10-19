#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Añade (o actualiza) la barra de navegación fija del sitio de exploradores
de Teoría Electromagnética en todas las páginas.

Uso (desde la carpeta del repo):
    python3 add_navegacion.py              añade/actualiza la barra
    python3 add_navegacion.py --quitar     la elimina
    python3 add_navegacion.py --dir RUTA   otra carpeta

La barra es fija (siempre visible), enlaza al índice y despliega el menú
«Temario» agrupado por unidades del curso; resalta la página actual.
El bloque es idempotente (delimitado por marcadores) y usa las variables
CSS de cada página con valores de respaldo, de modo que respeta el tema
claro/oscuro. Para añadir un explorador nuevo, agrégalo a NAV y re-corre
el script.
"""
import os, re, sys

INI, FIN = "<!-- navegacion:inicio -->", "<!-- navegacion:fin -->"

# (archivo, etiqueta corta, subtema)  — agrupados por unidad del temario ENES
NAV = [
 ("Unidad 1 · Conceptos fundamentales y ecuaciones de Maxwell", [
   ("Solenoide_explorador.html",      "Solenoide finito",            "1.4 · P3"),
 ]),
 ("Unidad 2 · Ondas planas electromagnéticas", [
   ("RC_interactivo.html",            "Circuito RC y fasores",       "fasores · P4"),
   ("MicroondasC_explorador.html",    "c con microondas",            "2.3 · P5"),
   ("EfectoPiel_explorador.html",     "Efecto piel",                 "2.6 · P6"),
   ("Polarizacion_explorador.html",   "Polarización",                "2.8 · P7"),
   ("Doppler_explorador.html",        "Efecto Doppler",              "2.9"),
 ]),
 ("Unidad 3 · Reflexión y refracción de ondas planas", [
   ("Reflexion_interactivo.html",     "Incidencia normal",           "3.2 · P8"),
   ("CapaTresMedios_interactivo.html","Capa dieléctrica (3 medios)", "3.3"),
   ("CapaDielectrica_explorador.html","Impedancia efectiva η(d)",    "3.3"),
   ("Snell_explorador.html",          "Ley de Snell",                "3.5 · P10, P11"),
   ("Fresnel_explorador.html",        "Coeficientes de Fresnel",     "3.6–3.8"),
 ]),
 ("Transversales", [
   ("Espectro_explorador.html",       "Espectro electromagnético",   "todo el curso"),
   ("AnatomiaGrafica_explorador.html","Anatomía de una gráfica",     "cómputo · P6"),
 ]),
]

def menu_html():
    partes = []
    for grupo, items in NAV:
        partes.append(f'<div class="nv-grp">{grupo}</div>')
        for f, et, sub in items:
            partes.append(f'<a href="{f}" data-nv="{f}">{et} <small>{sub}</small></a>')
    return "\n".join(partes)

def bloque():
    return f'''{INI}
<style>
  body{{margin-top:50px!important}}
  .nvbar{{position:fixed;top:0;left:0;right:0;z-index:9999;height:44px;display:flex;align-items:center;
    gap:10px;padding:0 14px;background:var(--card,#fff);border-bottom:1px solid var(--line,#e2dcc9);
    font-family:-apple-system,Segoe UI,Roboto,sans-serif;font-size:14px;box-shadow:0 1px 6px rgba(0,0,0,.06)}}
  .nvbar a{{text-decoration:none;color:var(--navy,var(--ink,#1F3864))}}
  .nv-home{{font-weight:700;white-space:nowrap}}
  .nv-home small{{font-weight:400;color:var(--muted,#5a5a5a)}}
  .nv-step{{display:flex;align-items:center;justify-content:center;width:34px;height:30px;border:1px solid var(--line,#e2dcc9);
    border-radius:8px;font-size:17px;line-height:1}}
  .nv-step:hover{{background:var(--bg,#f4f1ea)}}
  .nv-step[aria-disabled="true"]{{opacity:.25;pointer-events:none}}
  .nv-aquibar{{flex:1;min-width:0;text-align:center;font-weight:700;color:var(--ink,#1a1a1a);
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
  .nv-aquibar small{{font-weight:400;color:var(--muted,#8a8fa0)}}
  .nvbar details{{position:relative}}
  .nvbar summary{{list-style:none;cursor:pointer;font-weight:700;color:var(--accent,#C1571B);
    border:1px solid var(--line,#e2dcc9);border-radius:8px;padding:5px 12px;user-select:none;white-space:nowrap}}
  .nvbar summary::-webkit-details-marker{{display:none}}
  .nv-menu{{position:absolute;right:0;top:40px;width:min(640px,calc(100vw - 24px));max-height:calc(100vh - 70px);overflow:auto;
    background:var(--card,#fff);border:1px solid var(--line,#e2dcc9);border-radius:12px;
    box-shadow:0 8px 30px rgba(0,0,0,.18);padding:10px;column-count:2;column-gap:18px}}
  .nv-grp{{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted,#8a8fa0);
    padding:10px 10px 5px;break-after:avoid;border-top:1px solid var(--line,#eee)}}
  .nv-menu .nv-grp:first-child{{border-top:0;padding-top:4px}}
  .nv-menu a{{display:block;padding:8px 10px;border-radius:7px;color:var(--ink,#1a1a1a);break-inside:avoid}}
  .nv-menu a small{{color:var(--muted,#8a8fa0);margin-left:4px}}
  .nv-menu a:hover{{background:var(--bg,#f4f1ea)}}
  .nv-menu a.nv-aqui{{background:var(--bg,#f4f1ea);font-weight:700;color:var(--accent,#C1571B)}}
  .nv-pie{{column-span:all;margin-top:6px;padding:7px 10px 2px;border-top:1px solid var(--line,#eee);
    font-size:11.5px;color:var(--muted,#8a8fa0)}}
  @media (max-width:720px){{
    .nv-home small{{display:none}}
    .nv-aquibar{{display:none}}
    .nv-menu{{column-count:1;position:fixed;left:12px;right:12px;top:50px;width:auto}}
  }}
  @media print{{.nvbar{{display:none}} body{{margin-top:0!important}}}}
</style>
<nav class="nvbar" aria-label="Navegación del sitio">
  <a class="nv-home" href="index.html">⌁ Exploradores EM <small>· ENES Juriquilla</small></a>
  <a class="nv-step" id="nv-ant" href="#" title="Explorador anterior (tecla ←)" aria-label="Anterior">‹</a>
  <span class="nv-aquibar" id="nv-aqui-bar"></span>
  <a class="nv-step" id="nv-sig" href="#" title="Explorador siguiente (tecla →)" aria-label="Siguiente">›</a>
  <details id="nvdet"><summary>Temario ▾</summary>
    <div class="nv-menu">
{menu_html()}
    <div class="nv-pie">Atajos: ← anterior · → siguiente · Esc cierra el menú</div>
    </div>
  </details>
</nav>
<script>
(function(){{
  var orden=[], datos={{}};
  var l=document.querySelectorAll('.nv-menu a[data-nv]');
  for(var i=0;i<l.length;i++){{
    var f=l[i].getAttribute('data-nv'); orden.push(f);
    datos[f]={{el:l[i], titulo:l[i].childNodes[0].textContent.trim(),
               sub:(l[i].querySelector('small')||{{textContent:''}}).textContent}};
  }}
  var aqui=(location.pathname.split('/').pop()||'index.html');
  var idx=orden.indexOf(aqui);
  var ant=document.getElementById('nv-ant'), sig=document.getElementById('nv-sig'),
      bar=document.getElementById('nv-aqui-bar');
  if(idx>=0){{
    datos[aqui].el.className='nv-aqui';
    bar.innerHTML=datos[aqui].titulo+' <small>'+datos[aqui].sub+'</small>';
    if(idx>0) ant.href=orden[idx-1]; else ant.setAttribute('aria-disabled','true');
    if(idx<orden.length-1) sig.href=orden[idx+1]; else sig.setAttribute('aria-disabled','true');
    if(idx>0) ant.title='Anterior: '+datos[orden[idx-1]].titulo+'  (tecla ←)';
    if(idx<orden.length-1) sig.title='Siguiente: '+datos[orden[idx+1]].titulo+'  (tecla →)';
  }} else {{
    // índice u otra página: sin anterior/siguiente
    ant.setAttribute('aria-disabled','true'); sig.setAttribute('aria-disabled','true');
    bar.textContent='';
  }}
  document.addEventListener('click',function(e){{
    var d=document.getElementById('nvdet');
    if(d&&d.open&&!d.contains(e.target)) d.open=false;
  }});
  document.addEventListener('keydown',function(e){{
    var t=(e.target.tagName||'').toUpperCase();
    if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||e.altKey||e.ctrlKey||e.metaKey) return;
    var d=document.getElementById('nvdet');
    if(e.key==='Escape'&&d&&d.open){{d.open=false;return;}}
    if(idx<0) return;
    if(e.key==='ArrowLeft'&&idx>0) location.href=orden[idx-1];
    if(e.key==='ArrowRight'&&idx<orden.length-1) location.href=orden[idx+1];
  }});
}})();
</script>
{FIN}
'''

def quitar(s):
    return re.sub(re.escape(INI) + r".*?" + re.escape(FIN) + r"\n?", "", s, flags=re.S)

def main():
    args = sys.argv[1:]
    d = "."
    if "--dir" in args:
        i = args.index("--dir"); d = args[i+1]; del args[i:i+2]
    htmls = sorted(f for f in os.listdir(d) if f.endswith(".html"))
    if not htmls:
        sys.exit("no hay archivos .html en " + os.path.abspath(d))
    for f in htmls:
        p = os.path.join(d, f)
        s = quitar(open(p, encoding="utf-8").read())
        if "--quitar" not in args:
            s = s.rstrip() + "\n" + bloque()
        open(p, "w", encoding="utf-8").write(s)
    print(("navegación quitada de" if "--quitar" in args else "navegación añadida a"),
          len(htmls), "páginas en", os.path.abspath(d))

if __name__ == "__main__":
    main()
