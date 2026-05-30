# Dashboard ErgIoT — Módulo 5

Plataforma de visualización y análisis básico de los datos recolectados por el
prototipo IoT de monitoreo ergonómico. Consume las series temporales desde
InfluxDB Cloud y las presenta en una aplicación Streamlit multi-página con
identidad visual de la Universidad de La Salle.

## Páginas

| Página | Propósito |
|---|---|
| **Monitoreo Ergonómico** (`app.py`) | KPIs, series temporales, distribución, mapa de calor horario y eventos de mala postura. |
| **Buena Postura** (`pages/1_Buena_Postura.py`) | Refuerzo positivo: flag actual, racha consecutiva, sesiones doradas, logros y tendencia diaria. |
| **Pausas Activas** (`pages/2_Pausas_Activas.py`) | Monitoreo del `tiempo_sentado` y del flag `alerta_pausa`. Recomienda pausas activas cuando se supera el umbral. |

## Stack

```
ESP32 (MicroPython) → MQTT → InfluxDB Cloud → Streamlit + Plotly + pandas
```

| Capa | Tecnología | Por qué |
|---|---|---|
| Almacenamiento | InfluxDB Cloud 2.x | Series temporales con timestamp, compresión nativa, Flux. |
| Visualización | Streamlit | Une UI + análisis Python en un solo archivo. Cero JS. |
| Gráficos | Plotly | Interactividad (zoom, hover, descarga) sin escribir frontend. |
| Análisis | pandas + numpy | Estadística descriptiva, correlación, detección de eventos. |

Detalle en [`docs/JUSTIFICACION_TECNOLOGIAS.md`](docs/JUSTIFICACION_TECNOLOGIAS.md).

## Cómo correrlo

```powershell
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Copiar la plantilla de variables y rellenar credenciales
copy .env.example .env
# editar .env con tu token de InfluxDB

# 3. Lanzar
streamlit run app.py
```

La app queda en `http://localhost:8501`. Refresca cada 30 s automáticamente.

## Estructura

```
Dashboard/
├── app.py                          # Página principal
├── analytics.py                    # KPIs, eventos, correlaciones, achievements
├── data_loader.py                  # Consulta Flux a InfluxDB
├── config.py                       # Carga env vars + paleta institucional
├── requirements.txt                # Dependencias Python
├── .env.example                    # Plantilla de credenciales (sin secrets)
├── .streamlit/
│   └── config.toml                 # Tema institucional La Salle
├── pages/
│   ├── 1_Buena_Postura.py          # Vista positiva con flags y logros
│   └── 2_Pausas_Activas.py         # Vista de tiempo_sentado y alerta_pausa
└── docs/
    ├── JUSTIFICACION_TECNOLOGIAS.md
    └── GUION_VIDEO.md
```

## Análisis básico implementado

| Función | Ubicación | Para qué sirve |
|---|---|---|
| Estadística descriptiva | `app.py` (panel inferior) | media, std, percentiles de ángulo, presión, riesgo |
| Matriz de correlación | `analytics.matriz_correlacion()` | Relación entre variables; valida fórmula del ESP32 |
| Detección de eventos | `analytics.detectar_eventos_mala_postura()` | Agrupa muestras consecutivas con ángulo > 30° |
| Sesiones doradas | `analytics.sesiones_doradas()` | Períodos largos en postura correcta |
| Tiempo por flag | `analytics.tiempo_por_flag()` | Minutos en cada categoría EXCELENTE/BUENA/LÍMITE/MALA |
| KPIs de pausa | `analytics.kpis_pausa()` | Auto-detecta el umbral del firmware y cuenta eventos |
| Heatmap horario | `analytics.heatmap_horario()` | Promedio de ángulo por hora del día y día de la semana |

## Identidad visual

Paleta extraída de [lasalle.edu.co](https://lasalle.edu.co/es):

| Color | Hex | Uso |
|---|---|---|
| Azul marino primario | `#003057` | Headers, títulos, primary |
| Azul medio | `#02416c` | Variantes, líneas secundarias |
| Dorado institucional | `#f2a900` | Acento, botones, borde KPI |
| Dorado oscuro | `#d4a017` | Hover, énfasis |
| Rojo de alerta | `#C73E1D` | Solo cuando es necesario alertar |

## Seguridad de credenciales

El token de InfluxDB **nunca** se guarda en el código fuente. Se carga desde
`.env` (ignorado por Git) o de variables de entorno reales. La plantilla
[`.env.example`](.env.example) muestra qué variables hay que definir.

Si por error subieras un token a Git: ve a InfluxDB Cloud → Load Data → API
Tokens → revoca el token comprometido y genera uno nuevo.
