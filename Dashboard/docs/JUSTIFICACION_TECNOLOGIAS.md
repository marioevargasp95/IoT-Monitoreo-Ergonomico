# Justificación de tecnologías — Módulo 5

**Curso:** Internet de las Cosas — Grupo 02 · 2026-1
**Autores:** Mario Esteban Vargas Pisco · Yeison Esteven García Olaya

---

## 1. Pipeline completo

```
ESP32 (MicroPython)
  └── MPU-6050 (I2C)  → ángulo de tronco (arctan2)
  └── FSR402   (ADC)  → presión asiento / ocupación
  └── LED RGB  (PWM)  → alerta local
      │
      ▼
  WiFi + MQTT (HiveMQ Cloud, broker público)
      │
      ▼
  Telegraf / agente de ingesta → InfluxDB Cloud (AWS us-east-1)
      └── bucket: ErgIoT_Bucket
      └── measurement: telemetria_ergonomica
      └── fields: angulo_grados, presion_adc, ocupado,
                  indice_riesgo, clasificacion_riesgo,
                  tiempo_sentado, alerta_pausa
      │
      ▼
  Streamlit + Plotly  (capa de visualización y análisis)
      └── InfluxDB Python Client v2  (Flux query)
      └── pandas + scipy             (análisis básico)
      └── plotly.express + go        (gráficas interactivas)
```

---

## 2. Justificación por capa

### 2.1 Almacenamiento — **InfluxDB Cloud 2.x**

| Criterio | Decisión |
|---|---|
| Tipo de dato | Series temporales con timestamp obligatorio (1 muestra cada 2 s, 24/7) |
| Volumen esperado | ~43 000 puntos/día por dispositivo → optimización por TSI requerida |
| Alternativas evaluadas | PostgreSQL + TimescaleDB, MongoDB, ThingsBoard Cloud |
| Razón de elección | InfluxDB está diseñado nativamente para IoT: compresión por bloques, retención automática, lenguaje Flux para downsampling, free tier sin tarjeta de crédito y conector oficial Python. ThingsBoard mezcla almacenamiento + UI; nosotros queríamos desacoplar capas para poder reemplazar el dashboard sin tocar la fuente de verdad. |

### 2.2 Mensajería — **MQTT sobre HiveMQ Cloud**

| Criterio | Decisión |
|---|---|
| Restricción | ESP32 con 320 KB RAM y batería futura → protocolo ligero obligatorio |
| Alternativas evaluadas | HTTP REST, CoAP, WebSocket directo |
| Razón de elección | MQTT publica con QoS 1 en ~80 bytes/mensaje frente a ~400 bytes de un POST HTTP equivalente. El modelo publicar/suscribir desacopla productor y consumidor, y HiveMQ Cloud ofrece broker free hasta 100 conexiones — suficiente para el MVP y validable con MQTT Explorer antes de pasar a InfluxDB. |

### 2.3 Visualización — **Streamlit + Plotly**

| Criterio | Decisión |
|---|---|
| Requisito de la rúbrica | "Implementa una plataforma de visualización... con consideraciones de diseño" |
| Alternativas evaluadas | Grafana Cloud, Power BI, Data Explorer nativo InfluxDB |
| Razón de elección | Streamlit permite unir **visualización + análisis básico** en una sola aplicación Python: el mismo archivo contiene los `pandas.describe()`, la matriz de correlación, la detección de eventos y los gráficos Plotly. Grafana hace excelentes dashboards pero el análisis estadístico queda fuera de la herramienta. Plotly aporta interactividad (zoom, hover, descarga PNG) sin escribir JavaScript. Free tier total: 0 USD. |

### 2.4 Análisis — **pandas + numpy + scipy**

| Análisis implementado | Función |
|---|---|
| Estadística descriptiva | `df.describe()` sobre ángulo, presión, índice de riesgo, tiempo sentado |
| Correlación lineal | `df.corr()` para identificar relación ángulo ↔ índice de riesgo |
| Detección de eventos | Algoritmo de *run-length encoding* sobre `angulo > 30°` agrupando muestras consecutivas |
| Agregación temporal | `groupby(hora, día)` para mapa de calor de uso |
| KPIs operativos | % postura correcta, P95 del ángulo, % ocupación, índice de riesgo medio |

---

## 3. Consideraciones de diseño del dashboard

| Decisión de UX | Razón |
|---|---|
| Sidebar fija con ventana temporal (1h / 6h / 24h / 7d / 30d) | El operador suele querer "lo de la última hora" o "la última semana"; un selector evita escribir consultas Flux |
| Tarjetas KPI arriba | Patrón F (eye-tracking): el ojo entra por la esquina superior-izquierda |
| Umbral de 30° dibujado como línea roja punteada | El usuario ve **al instante** si está por encima del límite ergonómico sin leer la leyenda |
| Pestañas para series (ángulo / presión / riesgo) | Reduce *cognitive load*: un gráfico a la vez en lugar de tres apilados |
| Mapa de calor hora × día con escala roja-amarilla-verde | Codificación de color culturalmente consistente con semáforo: rojo = malo |
| Cache con TTL 30 s | Evita pegarle a InfluxDB en cada interacción; balancea "tiempo real" con costo de API |
| Tabla de eventos con duración y ángulo máximo | El operador puede priorizar: un evento de 5 min con 45° es más urgente que diez de 11 s con 31° |
| Cero hardcoding de fechas | Todo se mueve con `range(start: -7d)` → el dashboard sigue siendo válido sin mantenimiento |

---

## 4. Cumplimiento de la rúbrica

| Criterio (1.5 / 1.5 / 1.0 / 1.0) | Evidencia |
|---|---|
| Plataforma de visualización con diseño | App Streamlit con 5 KPIs, 3 series temporales, histograma, pie chart de riesgo, mapa de calor horario, tabla de eventos. Umbral ergonómico señalado. Caché y refresh manual. |
| Análisis básico de los datos | Estadística descriptiva, matriz de correlación, detección de eventos sostenidos, % postura correcta, agregación hora × día. |
| Justificación de tecnologías | Este documento + el video que recorre cada decisión. |
| Presentación clara y estructurada | Guion en `GUION_VIDEO.md` con tiempos y nombres de los integrantes en los primeros 10 s. |
