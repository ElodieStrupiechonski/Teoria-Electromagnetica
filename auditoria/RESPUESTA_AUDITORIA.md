# Respuesta a la auditoría del sitio — versión 1.2

**Recurso:** Teoría Electromagnética — Exploradores interactivos (ENES Juriquilla, UNAM) · DOI de concepto [10.5281/zenodo.23423157](https://doi.org/10.5281/zenodo.23423157)
**Auditoría recibida:** 19 de octubre de 2026, sobre la versión 1.1 del sitio.
**Respuesta:** versión 1.2, 19 de octubre de 2026.

## Método de atención

Cada hallazgo se reprodujo primero en la versión 1.1 con los valores indicados por la auditoría; se aplicó la corrección; y se volvió a medir en la versión 1.2 con un navegador automatizado (Chromium/Playwright). Además de los casos de la auditoría, se verificó la ausencia de errores de JavaScript en las 20 páginas y la ausencia de desborde horizontal a 390 px de ancho.

Leyenda: **Adoptado** — corregido tal como se propuso · **Adoptado (variante)** — corregido con una solución distinta, explicada · **Diferido** — aceptado, programado para una versión posterior · **No adoptado** — con justificación.

## 1. Estructura y metadatos

| ID | Hallazgo | Decisión | Cambio | Verificación en v1.2 |
|---|---|---|---|---|
| S1 | 18 de 20 páginas sin doctype, `lang` ni viewport: miniatura en teléfono | Adoptado | Script idempotente `add_doctype_em.py` aplicado a las 20 páginas; CSS móvil (ancho mínimo de tarjetas e inputs, ecuaciones envolventes) | Las 20 páginas miden ≤ 390 px de ancho a 390 px de pantalla |
| S2 | README (13), Zenodo («nueve») y sitio (19) no coinciden; tipo y fecha de CITATION.cff | Adoptado (variante) | Tabla del README con los 19 exploradores; descripción de Zenodo por unidades; fecha de publicación actualizada. Además, `zenodo.json` se renombra a `.zenodo.json`, nombre que Zenodo lee en la integración con GitHub (sin el punto, Zenodo usaba CITATION.cff). `CITATION.cff` conserva `type: dataset` porque el formato CFF solo admite `software` o `dataset`; el tipo «lección» se declara en `.zenodo.json` | Inspección de archivos |
| S3 | Versiones citadas 1.0 / 1.1 / 2.0 según la página | Adoptado | Script `set_version_em.py`: una sola versión (1.2) en las 20 páginas, README, `.zenodo.json` y CITATION.cff | Búsqueda de «Versión»: 1.2 en todas |
| S4 | Orden distinto entre portada y barra de navegación | Adoptado | Unidad 4 antes de Transversales en la portada | Inspección |
| S5 | Inducción etiquetada «1.6–1.7» sin tratar 1.7 | Adoptado | «tema 1.6» en portada, menú y página | Inspección |

## 2. Errores de física y coherencia

| ID | Archivo | Hallazgo | Decisión | Verificación en v1.2 (caso de la auditoría) |
|---|---|---|---|---|
| E1 | Doppler | Fórmula acústica para ondas EM (error del 40 % a v/c = 0.7) | Adoptado (variante) | f′ = f√((1+β)/(1−β)); la aproximación clásica se conserva punteada en la gráfica para que el estudiante vea dónde diverge; corrimiento al rojo z relativista exacto. β = 0.5 → 1.73 f (antes 2.00 f); v/c = 0.1 → z = 0.106 |
| E2 | Efecto piel | H dibujada adelantada respecto de E | Adoptado | H retrasada θ_η |
| E3 | Efecto piel | δ de buen conductor aplicado en todo régimen | Adoptado | α y β generales; agua de mar a 1 GHz: δ = 12.91 mm (antes 7.96 mm). Umbrales de régimen 100/0.01, tan δ visible, R_s solo en buen conductor, nota de validez (Debye, σ(ω)) |
| E4 | Espectro | Frontera infrarrojo/visible en 703 nm | Adoptado | 740 nm → «Visible · rojo» |
| E5 | Inducción | Tesela «Flujo Φ» mostraba NΦ | Adoptado | Pico de Φ = 56.5 µWb (antes 2.83 mWb); FEM sin cambio |
| E6 | Inducción | «FEM adelantada 90°» | Adoptado | Texto: FEM 90° retrasada respecto de Φ |
| E7 | Inducción | Sentido de Lenz invertido respecto del dibujo | Adoptado | Sentido corregido y referido a la vista correcta en cada modo. *Verificado por la regla de la mano derecha, como indicó la auditoría* |
| E8 | RC | Corchete Δt medía T − Δt | Adoptado | Ceros del mismo ciclo |
| E9 | Polarización | «Circular» con relación axial hasta 1.33 | Adoptado | Clasificación por relación axial (< 1.05). A = B, δ = 74° → «Elíptica, AR 1.33» |
| E10 | Microondas | c = −70 % para f < 188 MHz | Adoptado | Frecuencia mínima 200 MHz; 100 MHz tecleados → 200 MHz, c = 2.998×10⁸ m/s |
| E11 | Guía de onda | Conteo de modos saturado en 6 | Adoptado | Modos hasta m, n = 12; TE y TM contados por separado; WR-90 a 40 GHz → «17 TE + 9 TM»; guía cuadrada → «TE₁₀/TE₀₁ degenerados» |
| E12 | Anatomía | `np.linspace(1e2.5, …)` inválido | Adoptado | `np.linspace(10**a, 10**b, N)` |

## 3. Propuestas importantes (sección 7.2 de la auditoría)

| Propuesta | Decisión | Estado |
|---|---|---|
| Declarar hipótesis de cada modelo | Adoptado | Reflexión, Capa de tres medios, Fresnel, Capacitor, Gauss, Efecto piel, Doppler, Inducción |
| Etiquetar régimen óptico/microondas de las tablas de n | Adoptado (variante) | Nota en Capa de tres medios y Fresnel; tablas separadas: diferido |
| Snell: «ir al ángulo crítico»; tema 3.5 | Adoptado | Botón añadido |
| Guía de onda: presets a la frecuencia central de banda; banda EIA | Adoptado | WR-90 → 10.3 GHz; nota banda teórica vs. EIA |
| Capacitor: aviso de ruptura del aire | Adoptado | Aviso a E > 3 MV/m |
| Línea de transmisión: Γ como \|Γ\|∠θ | Adoptado | 0.333 ∠ 0.0° |
| Accesibilidad: nombre accesible de lienzos | Adoptado | `role="img"` y `aria-label` en los lienzos de 17 páginas |
| Accesibilidad: `<label for>` en todos los controles; fuente mínima 11 px en lienzos | Diferido | Versión 1.3 |
| Fresnel: τ, T, R + T = 1, fase en reflexión total | Diferido | Versión 1.3 |
| Smith: admitancia, stubs, escala en λ | Diferido | Versión 1.3 |
| Guía de onda: modos TM y Z_TE | Diferido (parcial) | Etiquetas TE/TM ya en 1.2; Z_TE en 1.3 |
| Snell: apertura numérica | Diferido | Versión 1.3 |
| Preguntas guía y recuadro «Para la práctica Pn» | Diferido | Prioridad pedagógica para 1.3 |

## 4. Ampliación de cobertura (sección 7.3)

Aceptada como hoja de ruta, en el orden propuesto por la auditoría: onda TEM y teorema de Poynting; ecuaciones de Maxwell fasoriales; condiciones de frontera; línea de transmisión con parámetros distribuidos y pérdidas; ley de Ampère y potencial vectorial; guía cilíndrica y de placas paralelas; continuidad y corriente de desplazamiento.

## 5. Puntos de criterio de la autoría (sección 6)

Se adoptaron los umbrales de régimen 100/0.01 en efecto piel y la nota sobre la convención de signo de Γ∥ en Fresnel. Los demás puntos (valor del teflón, umbral L/d del solenoide, convención del triángulo de impedancias, nomenclatura RHCP/LHCP) quedan para revisión en la versión 1.3.

---
Agradecemos a la auditoría su rigor: todos los errores reportados se reprodujeron y resultaron reales.
