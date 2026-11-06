#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tipografía institucional y notación del sitio de exploradores (idempotente).

Tipografías del Manual de identidad gráfica de la ENES Juriquilla (nov. 2025, sección 11):
Century Gothic (títulos; respaldo web: Questrial, de diseño geométrico equivalente),
Arial/Helvética (texto, controles y lecturas, con cifras tabulares) y Calibri como
respaldo; las fórmulas en Cambria (respaldo: STIX Two Text), como en las hojas del curso.

El bloque también:
  - dibuja en los lienzos (canvas) los subíndices y superíndices escritos como Z_L,
    V_inc, f_c o e^(−z/δ) con su tamaño y posición correctos;
  - convierte en el texto que generan los scripts (lecturas, mensajes) la misma
    notación y los subíndices Unicode (Z₀, η₁) en <sub>/<sup>.

Uso: python3 add_tipografia_em.py [--dir RUTA] [--quitar]
"""
import os, re, sys

INI, FIN = "<!-- tipografia:inicio -->", "<!-- tipografia:fin -->"
FUENTES_VIEJAS = re.compile(r'\s*<link[^>]+fonts\.googleapis\.com/css2\?family=(Spectral|IBM\+Plex)[^>]*>', re.I)

BLOQUE = INI + r'''
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Questrial&family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
  :root:root{
    --f-tit:"Century Gothic","Questrial","URW Gothic","Avant Garde",sans-serif;
    --sans:Arial,"Helvetica Neue",Helvetica,"Liberation Sans",Calibri,sans-serif;
    --serif:Cambria,"STIX Two Text","Times New Roman",serif;
    --mono:Arial,"Helvetica Neue",Helvetica,"Liberation Sans",sans-serif;
  }
  body,button,input,select,textarea{font-family:var(--sans)}
  body{font-variant-numeric:tabular-nums}
  h1,h2,h3,.ct,.eyebrow,header .sub{font-family:var(--f-tit)!important;letter-spacing:0}
  sub,sup{font-size:.72em;line-height:0;position:relative;vertical-align:baseline}
  sub{bottom:-.25em} sup{top:-.45em}
</style>
<script>
(function(){
  // ---- lienzos: subíndices y superíndices escritos como Z_L, V_inc, e^(−z/δ) ----
  var RX=/([A-Za-zΑ-Ωα-ω])_(\{[^}]+\}|[A-Za-z0-9áéíóúñ]{1,6})|\^(\{[^}]+\}|\([^)]+\)|−?\d{1,3})/g;
  var P=CanvasRenderingContext2D.prototype, F=P.fillText;
  P.fillText=function(t,x,y,mw){
    t=String(t);
    if((t.indexOf('_')<0&&t.indexOf('^')<0)||/\.(html|py|png|csv|txt|svg|jpg|pdf)\b/i.test(t)) return F.call(this,t,x,y,mw);
    var sg=[],last=0,m; RX.lastIndex=0;
    while((m=RX.exec(t))){
      if(m[1]){sg.push([t.slice(last,m.index)+m[1],0]);sg.push([m[2].replace(/[{}]/g,''),1]);}
      else{sg.push([t.slice(last,m.index),0]);sg.push([m[3].replace(/[{}()]/g,''),2]);}
      last=RX.lastIndex;
    }
    if(!sg.length) return F.call(this,t,x,y,mw);
    sg.push([t.slice(last),0]);
    var f0=this.font, mm=/(\d+(?:\.\d+)?)px/.exec(f0), px=mm?+mm[1]:12,
        fs=mm?f0.replace(mm[0],(px*0.72).toFixed(1)+'px'):f0, W=0,i;
    for(i=0;i<sg.length;i++){this.font=sg[i][1]?fs:f0;sg[i][2]=this.measureText(sg[i][0]).width;W+=sg[i][2];}
    var a=this.textAlign, x0=x;
    if(a==='center') x0=x-W/2; else if(a==='right'||a==='end') x0=x-W;
    this.textAlign='left';
    for(i=0;i<sg.length;i++){
      this.font=sg[i][1]?fs:f0;
      F.call(this,sg[i][0],x0,y+(sg[i][1]===1?0.28*px:sg[i][1]===2?-0.38*px:0));
      x0+=sg[i][2];
    }
    this.font=f0; this.textAlign=a;
  };
  // ---- texto generado por los scripts: misma notación en <sub>/<sup> ----
  if(/AnatomiaGrafica/.test(location.pathname)) return;
  var US=/([A-Za-zΑ-Ωα-ω])_(\{[^}]+\}|[A-Za-z0-9áéíóúñ]{1,6})|\^(\{[^}]+\}|\([^)]+\)|−?\d{1,3})|([₀-₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ]+)/g;
  var UNI="₀₁₂₃₄₅₆₇₈₉ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ", ASC="0123456789aeoxhklmnpstiruvj";
  var SALTA={SCRIPT:1,STYLE:1,TEXTAREA:1,OPTION:1,PRE:1,CODE:1,TITLE:1,INPUT:1,SELECT:1};
  function arreglar(n){
    var p=n.parentNode; if(!p||SALTA[p.nodeName]||p.namespaceURI==='http://www.w3.org/2000/svg') return;
    var t=n.nodeValue; US.lastIndex=0; if(!US.test(t)||/\.(html|py|png|csv)\b/.test(t)) return;
    US.lastIndex=0; var fr=document.createDocumentFragment(), last=0, m, e;
    while((m=US.exec(t))){
      var antes=t.slice(last,m.index);
      if(m[1]){fr.appendChild(document.createTextNode(antes+m[1]));e=document.createElement('sub');e.textContent=m[2].replace(/[{}]/g,'');}
      else if(m[3]){fr.appendChild(document.createTextNode(antes));e=document.createElement('sup');e.textContent=m[3].replace(/[{}()]/g,'');}
      else{fr.appendChild(document.createTextNode(antes));e=document.createElement('sub');
        e.textContent=m[4].split('').map(function(c){return ASC[UNI.indexOf(c)];}).join('');}
      fr.appendChild(e); last=US.lastIndex;
    }
    fr.appendChild(document.createTextNode(t.slice(last)));
    p.replaceChild(fr,n);
  }
  function recorrer(r){
    if(r.nodeType===3){arreglar(r);return;}
    if(r.nodeType!==1||SALTA[r.nodeName]) return;
    var w=document.createTreeWalker(r,NodeFilter.SHOW_TEXT,null), l=[], n;
    while((n=w.nextNode())) l.push(n);
    l.forEach(arreglar);
  }
  function inicio(){
    recorrer(document.body);
    new MutationObserver(function(ms){ms.forEach(function(m){
      if(m.type==='characterData') arreglar(m.target); else m.addedNodes.forEach(recorrer);
    });}).observe(document.body,{childList:true,subtree:true,characterData:true});
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',inicio); else inicio();
})();
</script>
''' + FIN

def main():
    a = sys.argv[1:]; d = "."
    if "--dir" in a:
        i = a.index("--dir"); d = a[i + 1]
    n = 0
    for f in sorted(x for x in os.listdir(d) if x.endswith(".html")):
        p = os.path.join(d, f); s = open(p, encoding="utf-8").read()
        s = re.sub(re.escape(INI) + r".*?" + re.escape(FIN) + r"\n?", "", s, flags=re.S)
        s = FUENTES_VIEJAS.sub("", s)
        if "--quitar" not in a:
            m = re.search(r"<meta[^>]+charset[^>]*>", s, re.I) or re.search(r"<html[^>]*>", s, re.I)
            k = m.end() if m else 0
            s = s[:k] + "\n" + BLOQUE + "\n" + s[k:]
        # pilas de fuentes del sistema que quedaron escritas a mano
        s = s.replace("-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif", "var(--sans)")
        s = s.replace("-apple-system,Segoe UI,Roboto,sans-serif", "var(--sans)")
        open(p, "w", encoding="utf-8").write(s); n += 1
    print("tipografía", "quitada de" if "--quitar" in a else "aplicada a", n, "páginas")

if __name__ == "__main__":
    main()
