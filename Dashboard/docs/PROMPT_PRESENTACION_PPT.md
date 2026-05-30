# Prompt para generar presentación PowerPoint

Copia y pega TODO el bloque siguiente en una IA generadora de presentaciones
(**Gamma.app**, **ChatGPT con plugin de PPT**, **Tome**, **Beautiful.ai**,
**SlidesAI**, **Microsoft Copilot en PowerPoint**, o pídelo en texto a
**Claude/Gemini** para que te dé las diapositivas en markdown y las copies
a PowerPoint manualmente).

---

## ── INICIO DEL PROMPT ──

Eres un diseñador experto en presentaciones académicas y técnicas. Crea una
presentación en PowerPoint de **12 diapositivas** sobre el siguiente proyecto.
La presentación se usará como apoyo visual a un video de 5 minutos para una
exposición universitaria.

### Contexto del proyecto

**Título:** ErgIoT — Monitoreo Ergonómico en Tiempo Real
**Curso:** Internet de las Cosas — Grupo 02 · 2026-1
**Universidad:** Universidad de La Salle (Bogotá, Colombia)
**Autores:** Mario Esteban Vargas Pisco · Yeison Esteven García Olaya
**Módulo:** 5 — Visualización y análisis de datos IoT
**Repositorio:** https://github.com/marioevargasp95/IoT-Monitoreo-Ergonomico

### Identidad visual (OBLIGATORIA)

Usa la paleta institucional de la Universidad de La Salle:

- **Azul marino primario** `#003057` → titulares, fondos oscuros, headers
- **Azul medio** `#02416c` → subtítulos, segundas variantes
- **Dorado institucional** `#f2a900` → acentos, líneas decorativas, KPIs
- **Dorado oscuro** `#d4a017` → hover/realces
- **Rojo de alerta** `#C73E1D` → solo cuando sea necesario alertar
- **Blanco/crema** `#ffffff` y `#f5f7fa` → fondos limpios

**Tipografía:** sans-serif moderna (Calibri, Inter, Montserrat o similar).
**Estilo:** minimalista, mucho espacio en blanco, jerarquía clara, 1 idea
por diapositiva.

### Estructura solicitada (12 diapositivas)

**Slide 1 — Portada**
- Logo Universidad de La Salle (placeholder si no está disponible)
- Título: "ErgIoT — Monitoreo Ergonómico en Tiempo Real"
- Subtítulo: "Módulo 5 · Visualización y análisis de datos IoT"
- Integrantes: Mario Esteban Vargas Pisco · Yeison Esteven García Olaya
- Curso: Internet de las Cosas — Grupo 02 · 2026-1
- Fondo azul marino con franja dorada inferior

**Slide 2 — Problema**
- Título: "El problema que abordamos"
- Bullets cortos:
  - Trabajadores de oficina pasan 6–8 horas sentados al día
  - La mala postura genera lesiones musculoesqueléticas crónicas
  - El sedentarismo prolongado incrementa el riesgo cardiovascular
  - No existe retroalimentación inmediata sobre la postura
- Una imagen sugerente (persona encorvada en escritorio)

**Slide 3 — Objetivo**
- Título: "Objetivo del Módulo 5"
- Texto destacado: "Construir una plataforma de visualización y análisis
  básico que transforme los datos IoT en decisiones ergonómicas accionables."
- 3 sub-objetivos con íconos:
  1. Dashboard interactivo con identidad institucional
  2. Análisis estadístico embebido (descriptivos, correlación, eventos)
  3. Justificación técnica de cada tecnología elegida

**Slide 4 — Arquitectura del sistema**
- Título: "Arquitectura completa"
- Diagrama horizontal de 5 etapas (con iconos):
  `[ESP32 + Sensores] → [WiFi/MQTT] → [HiveMQ Cloud] → [InfluxDB Cloud] → [Dashboard Streamlit]`
- Etiquetas debajo de cada etapa:
  - Percepción · Red · Broker · Almacenamiento · Visualización
- Pie de slide: "MicroPython + arctan2 a 0.5 Hz"

**Slide 5 — Hardware y modelo de datos**
- Dos columnas:
  - **Izquierda — Hardware:** ESP32 DevKit v1, MPU-6050 (acelerómetro),
    FSR402 (sensor de presión), LED RGB cátodo común
  - **Derecha — 7 fields en InfluxDB:**
    `angulo_grados`, `presion_adc`, `ocupado`, `clasificacion_riesgo`,
    `indice_riesgo`, `tiempo_sentado`, `alerta_pausa`
- Bucket: `ErgIoT_Bucket` · Measurement: `telemetria_ergonomica`

**Slide 6 — Dashboard: vista principal**
- Título: "Página 1 · Monitoreo Ergonómico"
- Screenshot/mockup del dashboard principal mostrando:
  - 5 KPIs en tarjetas con borde dorado
  - Serie temporal del ángulo con umbral en 30°
  - Mapa de calor hora × día
- Caption: "5 KPIs en vivo · Series temporales · Heatmap · Detección de eventos"

**Slide 7 — Dashboard: Buena Postura (refuerzo positivo)**
- Título: "Página 2 · Buena Postura"
- Screenshot/mockup mostrando:
  - Banner grande con flag actual (estado EXCELENTE/BUENA/LÍMITE/MALA)
  - Logros desbloqueables con barras de progreso
  - Gráfico de sesiones doradas
- Mensaje destacado: **"No solo alertamos — también motivamos."**

**Slide 8 — Dashboard: Pausas Activas**
- Título: "Página 3 · Pausas Activas"
- Screenshot/mockup mostrando:
  - Tiempo sentado acumulado con banda dorada de alerta
  - Banner de recomendación de pausa
- Texto destacado: "El firmware auto-detectado activa la alerta a los **50.5 min**"

**Slide 9 — Resultados clave (CIFRAS REALES)**
- Título: "Resultados sobre 1440 lecturas reales (3–7 mayo 2026)"
- 4 KPIs grandes en cuadrículas con fondo dorado:
  - **84%** postura correcta del tiempo
  - **17.9°** ángulo medio del tronco
  - **31** eventos de mala postura sostenida detectados
  - **0.76** correlación ángulo ↔ índice de riesgo
- Nota: "La correlación valida que la fórmula del ESP32 es coherente."

**Slide 10 — Análisis básico implementado**
- Título: "Análisis básico embebido"
- Lista en 2 columnas con íconos:
  1. Estadística descriptiva (media, std, percentiles)
  2. Matriz de correlación entre las 4 variables
  3. Detección de eventos por run-length encoding
  4. Sesiones doradas (postura correcta sostenida)
  5. Agregación temporal hora × día
  6. Auto-detección del umbral del firmware

**Slide 11 — Justificación de tecnologías**
- Tabla de 4 filas × 3 columnas:

| Capa | Tecnología | Por qué |
|---|---|---|
| Almacenamiento | InfluxDB Cloud | Series temporales nativas, compresión, Flux |
| Mensajería | MQTT (HiveMQ) | 80 bytes/msg vs 400 de HTTP (crítico para ESP32) |
| Visualización | Streamlit + Plotly | UI + análisis Python en un solo archivo |
| Identidad | Paleta La Salle | Coherencia visual institucional |

**Slide 12 — Cierre**
- Título: "Conclusiones"
- 3 mensajes:
  1. El dashboard convierte 1440 puntos de sensor en **3 preguntas operativas resueltas**
  2. La correlación de 0.76 valida la fórmula implementada en el firmware
  3. El stack IoT-cloud-Streamlit es **reproducible y de costo cero**
- Línea final: "Repositorio: github.com/marioevargasp95/IoT-Monitoreo-Ergonomico"
- Pie: "Universidad de La Salle · IoT G02 · 2026-1"

### Requisitos generales

- Formato 16:9 widescreen
- Máximo 6 bullets por slide
- 1 idea grande por slide, no recargar
- Usa íconos minimalistas (no clipart)
- Cuando incluyas screenshots: deja placeholder con bordes redondeados
- Espacio en blanco generoso
- Cifras en grande cuando sean KPIs (slide 9)
- Pie de cada slide: número de slide + nombre del proyecto
- Las primeras dos diapositivas y la última deben tener los nombres de los
  integrantes visibles

### Output esperado

- Archivo `.pptx` editable
- O en su defecto, el contenido por slide en formato markdown que pueda
  copiarse a PowerPoint

## ── FIN DEL PROMPT ──

---

## Tips para usar el prompt

| Herramienta | Cómo usar |
|---|---|
| **Gamma.app** | Crear cuenta gratis, pegar el prompt en "Generate". Genera la presentación en ~30 s con diseño profesional. Exportable a `.pptx`. |
| **Microsoft Copilot en PowerPoint 365** | En PowerPoint → Copilot → "Create presentation about..." → pegar el prompt completo. |
| **ChatGPT** | Pegar prompt, pedir output en markdown, copiar slide por slide a PowerPoint. |
| **Claude (este modelo)** | Pegar el prompt en una conversación nueva pidiendo el output en markdown. |
| **Tome.app** | Pegar el prompt en "Create with AI". |
| **SlidesAI** | Plugin de Google Slides; pegar el prompt en el panel lateral. |

## Imágenes y screenshots que vas a necesitar

Para los slides 6, 7 y 8, exporta capturas del dashboard:

1. Abre el dashboard (`Iniciar Dashboard.bat`)
2. Cambia ventana a "-30d" para que tengas todos los 1440 puntos
3. Saca screenshot de cada página con `Win + Shift + S` (Recortes de Windows):
   - **Página 1:** Captura desde el header hasta el heatmap
   - **Página 2 (Buena Postura):** Captura el banner + logros
   - **Página 3 (Pausas Activas):** Captura el banner + serie con bandas doradas
4. Reemplaza los placeholders en los slides 6/7/8 con estas capturas

## Logo de La Salle

Descargable en:
https://lasalle.edu.co/identidad-corporativa
(o pedir la versión oficial al área de comunicaciones de la universidad)
