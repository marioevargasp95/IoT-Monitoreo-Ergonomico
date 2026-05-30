# IoT — Monitoreo Ergonómico

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![InfluxDB](https://img.shields.io/badge/InfluxDB-22ADF6?style=flat-square&logo=influxdb&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white)
![Wokwi](https://img.shields.io/badge/Wokwi-Simulator-2EA043?style=flat-square)
![IoT](https://img.shields.io/badge/IoT-Sensores-FF6C37?style=flat-square)

**Universidad de La Salle (Bogotá)** · Curso Internet de las Cosas · Grupo 02 · 2026-1
**Autores:** Mario Esteban Vargas Pisco · Yeison Esteven García Olaya

## Descripción

Sistema IoT orientado al monitoreo ergonómico en puestos de trabajo. Captura
variables fisiológicas mediante sensores físicos (o simulados) y emite alertas
en tiempo real cuando se detecta postura incorrecta o sedentarismo prolongado.
Los datos viajan por MQTT a la nube y se visualizan en un dashboard
multi-página con análisis básico embebido.

## Objetivo

Detectar en tiempo real condiciones ergonómicas de riesgo (mala postura,
tiempo sedentario excesivo) y activar una alerta física mediante un actuador,
contribuyendo a reducir lesiones musculoesqueléticas en entornos de oficina.

---

## Arquitectura

```
[MPU-6050]  →  I2C  ┐
[FSR402]    →  ADC  ┤→  ESP32 (MicroPython)  →  WiFi/MQTT  →  HiveMQ Cloud  →  InfluxDB Cloud  →  Streamlit Dashboard
[LED RGB]   ←  PWM  ┘
```

| Capa | Componente |
|---|---|
| Percepción | ESP32 + MPU-6050 (ángulo) + FSR402 (presión) + LED RGB (alerta) |
| Red | WiFi 802.11 b/g/n + MQTT puerto 1883 |
| Procesamiento | Cálculo de ángulo con `arctan2` en el ESP32 + reglas de umbral |
| Almacenamiento | InfluxDB Cloud (bucket `ErgIoT_Bucket`) |
| Visualización | Streamlit + Plotly multi-página con identidad La Salle |

## Componentes

| Componente | Rol |
|---|---|
| Sensor de postura (MPU-6050) | Captura la inclinación del tronco vía acelerómetro |
| Sensor de presión (FSR402) | Detecta si el usuario está sentado |
| Actuador (LED RGB) | Emite alerta visual cuando se supera el umbral |
| Microcontrolador (ESP32) | Lee sensores, calcula ángulo y publica por MQTT |
| Wokwi | Simulación del circuito antes del despliegue físico |
| Notebook Python | Generación de datos de simulación y análisis exploratorio |
| Dashboard Streamlit | Visualización en tiempo real + análisis básico |

---

## Estructura del repositorio

```
IoT-Monitoreo-Ergonomico/
├── Wokwi/                     # Firmware MicroPython y diagrama del circuito
│   ├── main.py
│   ├── imu.py
│   └── diagram.json
├── Notebook/
│   └── Nodo_sensor.ipynb     # Simulación de la jornada laboral
├── Datos/                     # CSV/Excel con las 360 observaciones + gráficas
├── Dashboard/                 # Módulo 5 — App Streamlit multi-página
│   ├── app.py                # Vista principal: KPIs, series, análisis
│   ├── analytics.py          # Funciones de análisis y detección
│   ├── data_loader.py        # Cliente InfluxDB
│   ├── config.py             # Carga env vars + paleta institucional
│   ├── pages/
│   │   ├── 1_Buena_Postura.py    # Refuerzo positivo + logros
│   │   └── 2_Pausas_Activas.py   # tiempo_sentado + alerta_pausa
│   ├── docs/
│   │   ├── JUSTIFICACION_TECNOLOGIAS.md
│   │   └── GUION_VIDEO.md
│   ├── requirements.txt
│   └── .env.example          # Plantilla de credenciales (sin secrets)
└── README.md
```

---

## Modelo de datos (InfluxDB)

**Bucket:** `ErgIoT_Bucket` · **Measurement:** `telemetria_ergonomica`

| Field | Tipo | Descripción |
|---|---|---|
| `angulo_grados` | float | Ángulo de inclinación del tronco calculado en el ESP32 |
| `presion_adc` | int | Lectura cruda del FSR402 (0–4095) |
| `ocupado` | int (0/1) | 1 si hay presencia detectada en el asiento |
| `clasificacion_riesgo` | str | CORRECTA / LÍMITE / INADECUADA |
| `indice_riesgo` | int (0/1) | 1 cuando ángulo > umbral y hay presencia |
| `tiempo_sentado` | float | Minutos acumulados sentado continuo |
| `alerta_pausa` | int (0/1) | 1 cuando `tiempo_sentado` supera el umbral (50 min) |

## Lógica de alertas (firmware)

| Estado | LED | Condición |
|---|---|---|
| Postura correcta | 🟢 Verde | `angulo ≤ 30°` y `ocupado = 1` |
| Mala postura | 🔴 Rojo | `angulo > 30°` durante ≥ 10 s y `ocupado = 1` |
| Usuario ausente | 🔵 Azul | `presion_adc < umbral` |
| Pausa activa | 🟠 Naranja | `tiempo_sentado ≥ 50 min` |

**Muestreo:** 0.5 Hz (1 lectura cada 2 s).

---

## Tecnologías

- **MicroPython** — Firmware del ESP32 (lectura de sensores, cálculo de ángulo, publicación MQTT).
- **MQTT (HiveMQ Cloud)** — Mensajería ligera para IoT con QoS 1.
- **InfluxDB Cloud** — Almacenamiento de series temporales con compresión nativa y Flux.
- **Python** — Procesamiento, análisis y dashboard.
- **Streamlit + Plotly** — Visualización interactiva con análisis estadístico embebido.
- **pandas + numpy** — Estadística descriptiva, correlación, detección de eventos.
- **Wokwi** — Simulación del circuito ESP32 sin hardware físico.
- **Jupyter Notebook** — Exploración y generación de datos.

---

## Avance por módulos

| Módulo | Tema | Entregable |
|---|---|---|
| 1 | Introducción a IoT, sensores y actuadores | Diagrama de arquitectura |
| 2 | Simulación con Wokwi y generación de datos | Nodo sensor + 360 observaciones |
| 3 | Transmisión MQTT a la nube | Datos publicándose a HiveMQ → InfluxDB |
| 4 | Modelo de clasificación | Notebook con `ergodesk` clasificador |
| **5** | **Visualización y análisis** | **[Dashboard Streamlit](Dashboard/) con flags, logros y pausas activas** |
| 6 | Cierre y demo | Informe, video y repositorio organizado |

---

## Cómo correr el dashboard (Módulo 5)

```powershell
cd Dashboard
pip install -r requirements.txt
copy .env.example .env       # editar .env con tu token de InfluxDB
streamlit run app.py
```

La app queda en `http://localhost:8501` con tres vistas:
- **Monitoreo Ergonómico** — KPIs, series temporales, distribución, mapa de calor.
- **Buena Postura** — Flag actual, rachas, sesiones doradas y logros.
- **Pausas Activas** — `tiempo_sentado` y `alerta_pausa` con recomendaciones.

Más detalle en [`Dashboard/README.md`](Dashboard/README.md).

---

## Instalación rápida (solo notebook)

```bash
pip install pandas numpy matplotlib jupyter
jupyter notebook Notebook/Nodo_sensor.ipynb
```

---

## Licencia

Proyecto académico para el curso de Internet de las Cosas en la Universidad
de La Salle (Bogotá), 2026-1. Reutilizable con fines educativos citando a
los autores.
