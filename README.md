# IoT — Monitoreo Ergonómico

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=arduino&logoColor=white)
![Wokwi](https://img.shields.io/badge/Wokwi-Simulator-2EA043?style=flat-square)
![IoT](https://img.shields.io/badge/IoT-Sensores-FF6C37?style=flat-square)

## Descripción

Sistema IoT orientado al monitoreo ergonómico en puestos de trabajo. Captura dos variables fisiológicas mediante sensores físicos y evalúa un actuador para emitir alertas de postura incorrecta y sedentarismo prolongado.

## Objetivo

Detectar en tiempo real condiciones ergonómicas de riesgo (mala postura / tiempo sedentario excesivo) y activar una alerta física mediante un actuador, reduciendo lesiones musculoesqueléticas en entornos de oficina.

## Arquitectura del Sistema

```
[Sensor 1 — Postura]        [Sensor 2 — Sedentarismo]
         │                            │
         └────────────┬───────────────┘
                      │
               [Microcontrolador]
                      │
          ┌───────────┴───────────┐
   [Actuador / Alerta]    [Notebook análisis]
```

## Componentes

| Componente | Rol |
|---|---|
| Sensor de postura | Captura la inclinación / posición corporal |
| Sensor de movimiento | Detecta inactividad prolongada (sedentarismo) |
| Actuador | Emite alerta física (LED / buzzer) cuando se supera el umbral |
| Notebook Python | Análisis exploratorio y procesamiento de los datos capturados |
| Wokwi | Simulación del circuito antes del despliegue físico |

## Estructura del Repositorio

```
IoT-Monitoreo-Ergonomico/
├── Notebook/
│   └── Nodo_sensor.ipynb   # Análisis y procesamiento de datos del sensor
├── Datos/                   # Registros capturados por los sensores
├── Wokwi/                   # Esquema del circuito simulado
└── README.md
```

## Tecnologías

- **Python** — Procesamiento y análisis de datos del sensor
- **Arduino / Microcontrolador** — Lectura de sensores y control del actuador
- **Wokwi** — Simulación del circuito electrónico
- **Jupyter Notebook** — Exploración y visualización de los datos capturados

## Instalación

```bash
pip install pandas numpy matplotlib jupyter
jupyter notebook Notebook/Nodo_sensor.ipynb
```