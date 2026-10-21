# Historial de versiones

La numeración sigue las etiquetas (*tags*) de GitHub, que son las versiones archivadas en Zenodo. Cada versión archivada tiene su propio DOI de versión; el DOI de concepto [10.5281/zenodo.23423156](https://doi.org/10.5281/zenodo.23423156) (citar «todas las versiones») resuelve siempre a la más reciente.

## [1.3.1] — 2026-10-21 · DOI de versión [10.5281/zenodo.23538848](https://doi.org/10.5281/zenodo.23538848)

Atiende el informe de verificación de la v1.3 (detalle en [`auditoria/RESPUESTA_AUDITORIA.md`](auditoria/RESPUESTA_AUDITORIA.md), sección 6).

### Corregido
- Efecto piel: forma numéricamente estable de α (antes «δ = Infinity» con σ muy pequeña); validación de σ y εᵣ; longitudes en km.
- Espectro: fronteras 750 nm y 380 nm calculadas exactamente.
- Fresnel: teflón con su índice óptico (1.35).
- CapaDielectrica: bloque «Cómo citar»; nombre accesible en los lienzos que faltaban (CapaDielectrica, Anatomía, Espectro).
- Metadatos: `.zenodo.json` presente en la raíz (tipo «lección»), sin número de versión fijo; páginas con «Versión 1.3.1» y el DOI de concepto.
- Matriz de respuesta: la auditoría se hizo sobre el commit `92f6190`, no sobre la v1.2.

### Añadido
- Datos para buscadores en las 20 páginas (título descriptivo, descripción, URL canónica, Open Graph, schema.org *LearningResource*), `sitemap.xml` y verificación de Google Search Console; script `add_seo_em.py`.
- Carpeta `auditoria/` con los informes de los auditores (auditoría de la v1.2+ y verificación de la v1.3, con sus anexos), publicados con su autorización, y la matriz de respuesta.

## [1.3] — 2026-10-19 · DOI de versión [10.5281/zenodo.23482923](https://doi.org/10.5281/zenodo.23482923)

Versión que atiende la auditoría externa del sitio (19 de octubre de 2026). El detalle hallazgo por hallazgo, con la decisión tomada y la verificación, está en [`auditoria/RESPUESTA_AUDITORIA.md`](auditoria/RESPUESTA_AUDITORIA.md).

### Añadido
- Seis exploradores nuevos: Ley de Gauss, Capacitor con dieléctrico, Inducción de Faraday (Unidad 1); Línea de transmisión, Carta de Smith y Guía de onda rectangular (Unidad 4). La colección pasa de 13 a 19 exploradores.
- Entradas numéricas directas, formulario plegable y código de color (constantes de la naturaleza / variables) en todas las fichas.
- Hipótesis de cada modelo declaradas en pantalla.
- Scripts de mantenimiento `add_doctype_em.py` (estructura para teléfono) y `set_version_em.py` (versión única en todo el sitio).

### Corregido
- Estructura HTML: doctype, `lang="es"` y `meta viewport` en las 20 páginas; el sitio se lee correctamente en pantalla de teléfono (390 px).
- Doppler: fórmula relativista para ondas electromagnéticas (antes, aproximación acústica).
- Efecto piel: α y β generales en todo régimen; fase de H (retrasada); umbrales de régimen.
- Espectro: frontera infrarrojo/visible en 750 nm.
- Inducción: el flujo mostrado es Φ (no NΦ); desfase y sentido de Lenz.
- RC (corchete Δt), Polarización (clasificación circular por relación axial), Microondas (frecuencia mínima), Guía de onda (conteo de modos TE/TM), Anatomía de una gráfica (código generado).
- Metadatos: README y `CITATION.cff` coherentes con el contenido; versión única citada en las páginas del repositorio. (`.zenodo.json` no llegó a subirse en esta versión: Zenodo la archivó como «software»; corregido en 1.3.1.)

> Nota: la copia archivada en Zenodo de la v1.3 rotula sus páginas con el número «1.2», porque la etiqueta v1.2 ya estaba ocupada por el depósito anterior y la etiqueta se cambió al publicar. El contenido es el descrito aquí; la rotulación se unificó a «1.3» en el repositorio inmediatamente después.

## [1.2] — 2026-10-16 · DOI de versión [10.5281/zenodo.23423157](https://doi.org/10.5281/zenodo.23423157)
- Primer depósito en Zenodo (páginas rotuladas internamente con el número «1.1»). Barra de navegación por temario, contador de visitas, portada ordenada por unidades, 13 exploradores. La auditoría externa se hizo sobre un commit posterior (`92f6190`, 19 de octubre), no depositado.

## [1.0]–[1.1] — septiembre–octubre de 2026 (sin depósito en Zenodo)
- Primera publicación en GitHub Pages: 9 exploradores; después, navegación y contador.
