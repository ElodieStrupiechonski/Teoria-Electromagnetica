# Historial de versiones

Todas las versiones comparten el DOI de concepto [10.5281/zenodo.23423157](https://doi.org/10.5281/zenodo.23423157); cada una tiene además su DOI de versión en Zenodo.

## [1.2] — 2026-10-19

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
- Metadatos: README, `.zenodo.json` y `CITATION.cff` coherentes con el contenido; versión única citada en todas las páginas.

## [1.1] — 2026-10
- Barra de navegación por temario, contador de visitas, DOI de Zenodo, portada ordenada por unidades.

## [1.0] — 2026-09-29
- Primera publicación: 9 exploradores.
