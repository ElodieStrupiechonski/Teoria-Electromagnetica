# Teoría Electromagnética: exploradores interactivos

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23423156.svg)](https://doi.org/10.5281/zenodo.23423156)


Colección de recursos educativos abiertos (REA) para el curso de **Teoría Electromagnética** de la licenciatura en **Ingeniería Aeroespacial**, ENES Juriquilla, UNAM. Cada explorador es una página HTML autónoma e interactiva: se mueve un control y se observa cómo responde el fenómeno físico, en vivo.

**Versión 1.3.1 (2026)**

## Cómo usar

Abre **`index.html`** en cualquier navegador moderno (Chrome, Firefox, Safari, Edge). Desde esa portada puedes entrar a cada explorador. No se necesita conexión a internet ni instalar nada: todo el código va incluido en cada archivo. Las páginas se adaptan al tema claro u oscuro del sistema y funcionan también en pantalla de teléfono.

Para que los enlaces de la portada funcionen, **mantén todos los archivos en la misma carpeta**.

## Contenido

| Archivo | Tema | Unidad · práctica |
|---|---|---|
| `index.html` | Portada de la colección |: |
| `CampoGauss_explorador.html` | Ley de Gauss: carga puntual, esfera y lámina con superficie gaussiana arrastrable | U1 · 1.1 · P1 |
| `Capacitor_explorador.html` | Capacitor de placas paralelas con dieléctrico deslizable, a V fijo o Q fija | U1 · 1.2 · P1 |
| `Solenoide_explorador.html` | Campo de un solenoide finito frente al ideal μ₀nI (efecto de borde) | U1 · 1.4 · P3 |
| `Induccion_explorador.html` | Inducción de Faraday: imán arrastrable o B(t) senoidal, Φ y FEM en osciloscopio | U1 · 1.6 · P3 |
| `RC_interactivo.html` | Circuito RC: desfase corriente–voltaje, fasores, triángulo de impedancias | U2 · fasores · P4 |
| `MicroondasC_explorador.html` | Velocidad de propagación: medición de c con microondas (onda estacionaria, c = f·λ) | U2 · 2.3 · P5 |
| `EfectoPiel_explorador.html` | Efecto piel: penetración e^(−z/δ), desfase E–H, α y β generales, δ vs frecuencia | U2 · 2.6 · P6 |
| `Polarizacion_explorador.html` | Polarización lineal, circular y elíptica; enlace satélite–estación terrena | U2 · 2.8 · P7 |
| `Doppler_explorador.html` | Efecto Doppler relativista: frentes de onda, señal por observador y corrimiento al rojo | U2 · 2.9 |
| `Reflexion_interactivo.html` | Reflexión con incidencia normal: onda estacionaria, Γ, τ, SWR y plano móvil que mide η(d) | U3 · 3.2 · P8 |
| `TDR_explorador.html` | Reflectometría en cable coaxial (TDR): escalón que rebota en la carga, osciloscopio simulado en la T o sobre la carga, onda en el cable y guía para la tabla de la P8 | U3 · 3.2 · P8 |
| `CapaTresMedios_interactivo.html` | Capa dieléctrica entre dos medios: interfaz móvil en z = −d, radomo (λ/2) y antirreflejante (λ/4) | U3 · 3.3 |
| `CapaDielectrica_explorador.html` | Impedancia efectiva η(d): potencia reflejada contra d/λ₂ y condición η₂ = √(η₁η₃) | U3 · 3.3 |
| `Snell_explorador.html` | Ley de Snell, reflexión total interna y ángulo de Brewster | U3 · 3.5 · P10, P11 |
| `Fresnel_explorador.html` | Coeficientes de Fresnel: R⊥ y R∥ contra el ángulo, Brewster y reflexión total | U3 · 3.6–3.8 |
| `LineaTransmision_interactivo.html` | Línea de transmisión: Γ, onda estacionaria de voltaje, VSWR y Z_in(d) | U4 · 4.3–4.4 |
| `ImpedanciaEntrada_explorador.html` | Líneas cortas como reactancias: Z_in contra la longitud, stubs en corto y abierto, Z₀ = √(Z_sc Z_oc), pérdidas y condición de Heaviside | U4 · 4.5–4.6 · P14 |
| `Smith_explorador.html` | Carta de Smith: la carga como punto, giro hacia el generador, VSWR, admitancias, V_máx/V_mín, escala en λ y modo práctica | U4 · 4.7 · P15 |
| `Acoplamiento_explorador.html` | Acoplamiento de impedancias: transformador λ/4 y stub en paralelo, recorrido en la carta de Smith y ancho de banda | U4 · 4.8–4.9 · P15 |
| `GuiaOnda_explorador.html` | Guía de onda rectangular: cortes TE/TM, tabla de modos, Z_TE y Z_TM, atenuación bajo el corte, diagrama de dispersión, patrones de campo | U4 · 4.10–4.12 · P16 |
| `Espectro_explorador.html` | Espectro electromagnético: cuatro ejes (λ, f, energía, número de onda), zoom del visible | transversal |
| `AnatomiaGrafica_explorador.html` | Anatomía de una gráfica científica, con el código matplotlib equivalente | transversal · P6 |

## Requisitos técnicos

Navegador con HTML5 y `<canvas>`. Sin dependencias externas ni servidor. Las tipografías se cargan de Google Fonts cuando hay internet; sin conexión se usan tipografías del sistema como respaldo.

## Autoría

- **Elodie Strupiechonski**, ENES Juriquilla, UNAM. ORCID [0000-0001-8991-8499](https://orcid.org/0000-0001-8991-8499)
- **Andrés de Luna Bugallo**, CFATA, UNAM. ORCID [0000-0002-7591-5235](https://orcid.org/0000-0002-7591-5235)

## Licencia

[Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.es). Puedes compartir y adaptar el material, incluso con fines comerciales, siempre que des el crédito correspondiente.

## Cómo citar

> Strupiechonski, E., & de Luna Bugallo, A. (2026). *Teoría Electromagnética: exploradores interactivos* (Versión 1.3.1) [Recurso educativo abierto]. UNAM, ENES Juriquilla. DOI: 10.5281/zenodo.23423156

