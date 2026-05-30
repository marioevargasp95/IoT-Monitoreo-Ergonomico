# IoT — Monitoreo Ergonómico

**Universidad de La Salle (Bogotá)** · Curso Internet de las Cosas · Grupo 02 · 2026-1
**Autores:** Mario Esteban Vargas Pisco · Yeison Esteven García Olaya

Sistema IoT de prototipo funcional que detecta posturas inadecuadas en tiempo
real mediante dos sensores físicos (o simulados), genera alertas visuales
locales y transmite datos a un dashboard en la nube para visualización y
análisis básico.

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

---

## Contenido del repositorio

| Carpeta | Contenido |
|---|---|
| [`Wokwi/`](Wokwi/) | Firmware MicroPython del ESP32 (`main.py`, `imu.py`) y diagrama del circuito (`diagram.json`) para simulación en [wokwi.com](https://wokwi.com). |
| [`Notebook/`](Notebook/) | Jupyter notebook con la simulación de la jornada laboral y generación de datos sintéticos. |
| [`Datos/`](Datos/) | CSV y Excel con las 360 observaciones simuladas, más gráficas de la jornada. |
| [`Dashboard/`](Dashboard/) | **Módulo 5** — Aplicación Streamlit multi-página con KPIs, análisis básico, flags positivos y monitoreo de pausas activas. |

---

## Modelo de datos (InfluxDB)

**Bucket:** `ErgIoT_Bucket`
**Measurement:** `telemetria_ergonomica`

| Field | Tipo | Descripción |
|---|---|---|
| `angulo_grados` | float | Ángulo de inclinación del tronco calculado en el ESP32 |
| `presion_adc` | int | Lectura cruda del FSR402 (0–4095) |
| `ocupado` | int (0/1) | 1 si hay presencia detectada en el asiento |
| `clasificacion_riesgo` | str | CORRECTA / LÍMITE / INADECUADA |
| `indice_riesgo` | int (0/1) | 1 cuando ángulo > umbral y hay presencia |
| `tiempo_sentado` | float | Minutos acumulados sentado continuo |
| `alerta_pausa` | int (0/1) | 1 cuando `tiempo_sentado` supera el umbral (50 min) |

---

## Lógica de alertas (firmware)

| Estado | LED | Condición |
|---|---|---|
| Postura correcta | 🟢 Verde | `angulo ≤ 30°` y `ocupado = 1` |
| Mala postura | 🔴 Rojo | `angulo > 30°` durante ≥ 10 s y `ocupado = 1` |
| Usuario ausente | 🔵 Azul | `presion_adc < umbral` |
| Pausa activa | 🟠 Naranja | `tiempo_sentado ≥ 50 min` |

**Muestreo:** 0.5 Hz (1 lectura cada 2 s).

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
copy .env.example .env       # luego pegar tu token de InfluxDB en .env
streamlit run app.py
```

Más detalles en [`Dashboard/README.md`](Dashboard/README.md).

---

## Licencia

Proyecto académico para el curso de Internet de las Cosas en la Universidad
de La Salle (Bogotá), 2026-1. Reutilizable con fines educativos citando a
los autores.
