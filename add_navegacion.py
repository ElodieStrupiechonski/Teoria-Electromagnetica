#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Añade (o actualiza) el panel lateral de navegación del sitio de exploradores
de Teoría Electromagnética en todas las páginas.

Uso (desde la carpeta del repo):
    python3 add_navegacion.py              añade/actualiza la barra
    python3 add_navegacion.py --quitar     la elimina
    python3 add_navegacion.py --dir RUTA   otra carpeta

El panel queda fijo a la izquierda (en pantallas angostas se abre con «☰ Temario»), enlaza al índice, tiene anterior/siguiente, buscador y la lista
agrupada por unidades del curso; resalta la página actual.
El bloque es idempotente (delimitado por marcadores) y usa las variables
CSS de cada página con valores de respaldo, de modo que respeta el tema
claro/oscuro. Para añadir un explorador nuevo, agrégalo a NAV y re-corre
el script.
"""
import os, re, sys

INI, FIN = "<!-- navegacion:inicio -->", "<!-- navegacion:fin -->"

# (archivo, etiqueta corta, subtema) : agrupados por unidad del temario ENES
NAV = [
 ("Unidad 1 · Conceptos fundamentales y ecuaciones de Maxwell", [
   ("CampoGauss_explorador.html",     "Ley de Gauss",                "1.1 · P1"),
   ("Capacitor_explorador.html",      "Capacitor con dieléctrico",   "1.2 · P1"),
   ("Solenoide_explorador.html",      "Solenoide finito",            "1.4 · P3"),
   ("Induccion_explorador.html",      "Inducción de Faraday",        "1.6 · P3"),
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
   ("TDR_explorador.html",            "TDR en cable coaxial",        "3.2 · P8"),
   ("CapaTresMedios_interactivo.html","Capa dieléctrica (3 medios)", "3.3"),
   ("CapaDielectrica_explorador.html","Impedancia efectiva η(d)",    "3.3"),
   ("Snell_explorador.html",          "Ley de Snell",                "3.5 · P10, P11"),
   ("Fresnel_explorador.html",        "Coeficientes de Fresnel",     "3.6–3.8"),
 ]),
 ("Unidad 4 · Líneas de transmisión y guías de onda", [
   ("LineaTransmision_interactivo.html","Línea de transmisión · Γ y VSWR","4.3–4.4"),
   ("Smith_explorador.html",          "Carta de Smith",              "4.7–4.8"),
   ("GuiaOnda_explorador.html",       "Guía de onda rectangular",    "4.10–4.12"),
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
            partes.append(f'<a href="{f}" data-nv="{f}">{et}<small>{sub}</small></a>')
    return "\n".join(partes)

def bloque():
    return f"""{INI}
<style>
  :root{{--nv-w:272px}}
  body{{margin-top:0!important}}
  @media (min-width:1100px){{ body{{margin-left:var(--nv-w)!important}} }}
  .nvside{{position:fixed;top:0;left:0;bottom:0;width:var(--nv-w);z-index:9999;display:flex;flex-direction:column;
    background:var(--card,#fff);border-right:1px solid var(--line,#e2dcc9);
    font-family:Arial,"Helvetica Neue",Helvetica,sans-serif;font-size:14px;color:var(--ink,#1a1a1a);
    box-shadow:1px 0 8px rgba(0,0,0,.05);transition:transform .2s ease}}
  .nvside a{{text-decoration:none;color:inherit}}
  .nv-cab{{padding:14px 16px 10px;border-bottom:1px solid var(--line,#e2dcc9)}}
  .nv-marca{{display:block;font-family:"Century Gothic","Questrial",Arial,sans-serif;font-weight:700;font-size:15px;
    line-height:1.25;color:var(--navy,var(--ink,#1F3864))}}
  .nv-marca small{{display:block;font-weight:400;font-size:12px;color:var(--muted,#5a5a5a);margin-top:2px}}
  .nv-pasos{{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px}}
  .nv-paso{{display:flex;flex-direction:column;gap:1px;padding:6px 8px;border:1px solid var(--line,#e2dcc9);border-radius:8px;
    font-size:11px;color:var(--muted,#5a5a5a);min-width:0}}
  .nv-paso b{{font-size:12.5px;color:var(--ink,#1a1a1a);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
  .nv-paso.sig{{text-align:right}}
  .nv-paso:hover{{background:var(--bg,#f4f1ea)}}
  .nv-paso[aria-disabled="true"]{{opacity:.3;pointer-events:none}}
  .nv-busca{{margin-top:8px;width:100%;box-sizing:border-box;padding:7px 9px;border:1px solid var(--line,#e2dcc9);border-radius:8px;
    font:inherit;background:var(--bg,#f8f6f0);color:inherit}}
  .nv-lista{{flex:1;overflow-y:auto;padding:6px 8px 10px}}
  .nv-grp{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted,#8a8fa0);padding:12px 8px 4px}}
  .nv-lista a{{display:block;padding:6px 8px 6px 10px;border-radius:6px;border-left:3px solid transparent;line-height:1.3}}
  .nv-lista a small{{display:block;font-size:11px;color:var(--muted,#8a8fa0)}}
  .nv-lista a:hover{{background:var(--bg,#f4f1ea)}}
  .nv-lista a.nv-aqui{{background:var(--bg,#f4f1ea);border-left-color:var(--accent,#C1571B);font-weight:700}}
  .nv-pie{{padding:8px 14px;border-top:1px solid var(--line,#e2dcc9);font-size:11px;color:var(--muted,#8a8fa0)}}
  .nv-boton{{display:none;position:fixed;top:10px;left:10px;z-index:10000;gap:6px}}
  .nv-boton a,.nv-boton button{{display:flex;align-items:center;justify-content:center;height:38px;min-width:38px;padding:0 10px;
    border:1px solid var(--line,#e2dcc9);border-radius:9px;background:var(--card,#fff);color:var(--ink,#1a1a1a);
    font:600 14px Arial,sans-serif;text-decoration:none;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.12)}}
  .nv-boton [aria-disabled="true"]{{opacity:.3;pointer-events:none}}
  .nv-velo{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:10001}}
  .nv-cierra{{display:none;position:absolute;top:10px;right:10px;width:32px;height:32px;border:1px solid var(--line,#e2dcc9);border-radius:8px;background:var(--card,#fff);color:inherit;font-size:16px;cursor:pointer}}
  .nv-cab{{position:relative}}
  @media (max-width:1099px){{
    body{{margin-top:56px!important}}
    .nvside{{transform:translateX(-102%);width:min(320px,88vw)}}
    .nvside.abierto{{transform:none;z-index:10002}}
    .nv-cierra{{display:block}}
    .nv-boton{{display:flex}}
    .nvside.abierto ~ .nv-velo{{display:block}}
  }}
  @media print{{.nvside,.nv-boton,.nv-velo{{display:none}} body{{margin:0!important}}}}
</style>
<nav class="nvside" id="nvside" aria-label="Exploradores del curso">
  <div class="nv-cab">
    <button class="nv-cierra" id="nv-cierra" aria-label="Cerrar el temario">✕</button>
    <a class="nv-marca" href="index.html">Exploradores de Teoría Electromagnética<small>ENES Juriquilla, UNAM · inicio</small></a>
    <div class="nv-pasos">
      <a class="nv-paso" id="nv-ant" href="#" aria-label="Explorador anterior">‹ anterior<b id="nv-ant-t">…</b></a>
      <a class="nv-paso sig" id="nv-sig" href="#" aria-label="Explorador siguiente">siguiente ›<b id="nv-sig-t">…</b></a>
    </div>
    <input class="nv-busca" id="nv-busca" type="search" placeholder="Buscar (tecla /)" aria-label="Buscar explorador">
  </div>
  <div class="nv-lista" id="nv-lista">
{menu_html()}
  </div>
  <div class="nv-pie">Teclas: ← anterior · → siguiente · / buscar · Esc cerrar</div>
</nav>
<div class="nv-boton"><button id="nv-abre" aria-controls="nvside" aria-expanded="false">☰ Temario</button>
  <a id="nv-ant2" href="#" aria-label="Anterior">‹</a><a id="nv-sig2" href="#" aria-label="Siguiente">›</a></div>
<div class="nv-velo" id="nv-velo"></div>
<script>
(function(){{
  var lista=document.getElementById('nv-lista'), side=document.getElementById('nvside');
  var l=lista.querySelectorAll('a[data-nv]'), orden=[], dat={{}};
  for(var i=0;i<l.length;i++){{var f=l[i].getAttribute('data-nv');orden.push(f);
    dat[f]={{el:l[i],t:l[i].childNodes[0].textContent.trim()}};}}
  var aqui=(location.pathname.split('/').pop()||'index.html'), k=orden.indexOf(aqui);
  function paso(idA,idT,j){{var a=document.getElementById(idA);
    if(j<0||j>=orden.length){{a.setAttribute('aria-disabled','true');if(idT)document.getElementById(idT).textContent='';return;}}
    a.href=orden[j];a.title=dat[orden[j]].t+(j<k?' (tecla ←)':' (tecla →)');if(idT)document.getElementById(idT).textContent=dat[orden[j]].t;}}
  if(k>=0){{dat[aqui].el.className='nv-aqui';dat[aqui].el.setAttribute('aria-current','page');
    paso('nv-ant','nv-ant-t',k-1);paso('nv-sig','nv-sig-t',k+1);paso('nv-ant2',null,k-1);paso('nv-sig2',null,k+1);
    setTimeout(function(){{var r=dat[aqui].el;lista.scrollTop=r.offsetTop-lista.clientHeight/3;}},0);}}
  else{{paso('nv-ant','nv-ant-t',-1);paso('nv-sig','nv-sig-t',0);paso('nv-ant2',null,-1);paso('nv-sig2',null,0);}}
  var bus=document.getElementById('nv-busca');
  bus.addEventListener('input',function(){{var q=bus.value.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
    var grp=null,vis=0;
    Array.prototype.forEach.call(lista.children,function(c){{
      if(c.classList.contains('nv-grp')){{if(grp)grp.style.display=vis?'':'none';grp=c;vis=0;return;}}
      var t=c.textContent.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
      var ok=!q||t.indexOf(q)>=0;c.style.display=ok?'':'none';if(ok)vis++;}});
    if(grp)grp.style.display=vis?'':'none';}});
  bus.addEventListener('keydown',function(e){{if(e.key==='Enter'){{var v=lista.querySelector('a[data-nv]:not([style*="none"])');if(v)location.href=v.href;}}}});
  var abre=document.getElementById('nv-abre'), velo=document.getElementById('nv-velo');
  function cambia(on){{side.classList.toggle('abierto',on);abre.setAttribute('aria-expanded',on?'true':'false');}}
  abre.addEventListener('click',function(){{cambia(!side.classList.contains('abierto'));}});
  velo.addEventListener('click',function(){{cambia(false);}});
  document.getElementById('nv-cierra').addEventListener('click',function(){{cambia(false);}});
  document.addEventListener('keydown',function(e){{
    var t=(e.target.tagName||'').toUpperCase();
    if(e.key==='Escape'){{cambia(false);if(t==='INPUT')e.target.blur();return;}}
    if(t==='INPUT'||t==='TEXTAREA'||t==='SELECT'||e.altKey||e.ctrlKey||e.metaKey) return;
    if(e.key==='/'){{e.preventDefault();if(innerWidth<1100)cambia(true);bus.focus();return;}}
    if(k<0) return;
    if(e.key==='ArrowLeft'&&k>0) location.href=orden[k-1];
    if(e.key==='ArrowRight'&&k<orden.length-1) location.href=orden[k+1];
  }});
}})();
</script>
{FIN}
"""

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
