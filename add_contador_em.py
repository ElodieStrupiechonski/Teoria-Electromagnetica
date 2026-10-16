#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Añade (o actualiza) el contador de visitas de GoatCounter en todas las páginas
del sitio de exploradores de Teoría Electromagnética.

Uso (desde la carpeta del repo, donde está index.html):
    python3 add_contador_em.py CODIGO          CODIGO = subdominio de GoatCounter (p. ej. 'teoriaem')
    python3 add_contador_em.py CODIGO --dir RUTA   para otra carpeta
    python3 add_contador_em.py --quitar        elimina el bloque de todas las páginas

Diferencias respecto al script de Vibraciones:
  · estas páginas no llevan </body> explícito: el bloque se inserta antes de
    </body> si existe y, si no, se añade al final del archivo (equivalente).
  · los colores usan las variables CSS del sitio EM (--card, --line, --muted,
    --navy / --ink) con valores de respaldo, así que respeta el modo oscuro.
El bloque es idempotente (delimitado por marcadores) y en una copia local
(file://) no se muestra ni hace peticiones.
"""
import os, re, sys

INI, FIN = "<!-- contador:inicio -->", "<!-- contador:fin -->"

def bloque(code):
    return f'''{INI}
<style>
  .visitas{{max-width:940px;margin:0 auto;padding:0 18px 26px;font-size:11.5px;
    color:var(--muted,#7A8699);display:none;font-family:inherit}}
  .visitas span{{display:inline-block;background:var(--card,#fff);
    border:1px solid var(--line,#D3DEEE);border-radius:20px;padding:3px 11px}}
  .visitas b{{color:var(--navy,var(--ink,#1F3864));font-weight:700}}
  .visitas a{{color:var(--muted,#7A8699);text-decoration:none;margin-left:6px}}
  .visitas a:hover{{text-decoration:underline}}
</style>
<div class="visitas" id="visitas"><span>👁 Esta página: <b id="vis-pag">–</b> visitas · Todo el sitio: <b id="vis-tot">–</b>
<a href="https://{code}.goatcounter.com" target="_blank" rel="noopener" title="Estadísticas públicas del sitio (GoatCounter, sin cookies)">estadísticas ↗</a></span></div>
<script>
(function(){{
  if(location.protocol!=='http:' && location.protocol!=='https:') return;   // copia local: sin contador ni peticiones
  var sc=document.createElement('script'); sc.async=true;
  sc.setAttribute('data-goatcounter','https://{code}.goatcounter.com/count');
  sc.src='https://gc.zgo.at/count.js'; document.head.appendChild(sc);
  var base='https://{code}.goatcounter.com/counter/';
  function pide(path){{
    return fetch(base+encodeURIComponent(path).replace(/%2F/g,'/')+'.json',{{cache:'no-cache'}})
      .then(function(r){{ return r.ok ? r.json() : null; }}).catch(function(){{ return null; }});
  }}
  var p=location.pathname;
  if(/\\/index\\.html$/.test(p)) p=p.replace(/index\\.html$/,'');
  Promise.all([pide(p), pide('TOTAL')]).then(function(res){{
    var a=res[0], b=res[1];
    if(!a && !b) return;
    document.getElementById('vis-pag').textContent = a ? a.count : '–';
    document.getElementById('vis-tot').textContent = b ? b.count : '–';
    document.getElementById('visitas').style.display='block';
  }});
}})();
</script>
{FIN}
'''

def quitar(s):
    return re.sub(re.escape(INI) + r".*?" + re.escape(FIN) + r"\n?", "", s, flags=re.S)

def poner(s, code):
    s = quitar(s)
    blk = bloque(code)
    n = s.count("</body>")
    if n == 1:
        return s.replace("</body>", blk + "</body>", 1)
    if n > 1:
        sys.exit("página con más de un </body>; revísala a mano")
    # páginas sin </body> explícito (los exploradores EM): el bloque va al final
    return s.rstrip() + "\n" + blk

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    args = sys.argv[1:]
    d = "."
    if "--dir" in args:
        i = args.index("--dir"); d = args[i+1]; del args[i:i+2]
    arg = args[0].strip()
    htmls = sorted(f for f in os.listdir(d) if f.endswith(".html"))
    if not htmls:
        sys.exit("no hay archivos .html en " + os.path.abspath(d))
    for f in htmls:
        p = os.path.join(d, f)
        s = open(p, encoding="utf-8").read()
        if arg == "--quitar":
            s = quitar(s)
        else:
            if not re.fullmatch(r"[a-z0-9-]{2,}", arg):
                sys.exit("código no válido: " + arg)
            s = poner(s, arg)
        open(p, "w", encoding="utf-8").write(s)
    print(("contador quitado de" if arg == "--quitar" else "contador «%s» añadido a" % arg),
          len(htmls), "páginas en", os.path.abspath(d))

if __name__ == "__main__":
    main()
