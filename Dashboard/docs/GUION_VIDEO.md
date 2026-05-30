# Guion del video — Módulo 5 IoT (máximo 5 minutos)

**Curso:** Internet de las Cosas — Grupo 02 · 2026-1
**Proyecto:** ErgIoT — Monitoreo Ergonómico en Tiempo Real
**Duración objetivo:** 4:50

---

## Bloque 1 — Portada con créditos (0:00 – 0:10) · **OBLIGATORIO**

> **En pantalla** (texto grande, centrado, sobre fondo institucional):
> 
> **Proyecto ErgIoT — Monitoreo Ergonómico en Tiempo Real**
> Universidad de La Salle · Internet de las Cosas G02 · 2026-1
>
> **Integrantes:**
> - Mario Esteban Vargas Pisco
> - Yeison Esteven García Olaya
>
> *Módulo 5 — Visualización y análisis de datos IoT*

**Voz (lectura):**
> "Buenas, somos Mario Vargas y Yeison García, del grupo 02 del curso Internet de las Cosas. Presentamos el Módulo 5 del proyecto ErgIoT."

---

## Bloque 2 — Contexto del problema (0:10 – 0:40)

**Voz:**
> "Nuestro sistema captura postura sentada con un ESP32, un acelerómetro MPU-6050 y un sensor de presión FSR402. Las lecturas viajan por MQTT a la nube y se almacenan en InfluxDB Cloud. Pero los datos crudos no informan: necesitan una capa de visualización y análisis que permita interpretarlos y tomar decisiones."

**En pantalla:** Diagrama del pipeline
```
ESP32 → MQTT → InfluxDB Cloud → Streamlit
```

---

## Bloque 3 — Recorrido del dashboard (0:40 – 2:30)

**Acción:** abrir `http://localhost:8501` y mostrar la app en vivo.

**Voz mientras se navega:**

1. *(0:40 – 1:00)* "Arriba tenemos los KPIs: número total de lecturas, ángulo medio, percentil 95, porcentaje de postura correcta y ocupación del asiento. En este turno tenemos **88% de postura correcta** sobre 360 lecturas."

2. *(1:00 – 1:25)* "La serie temporal del ángulo tiene una línea roja punteada en 30 grados — nuestro umbral ergonómico. Cualquier pico por encima es una alerta potencial. Aquí podemos hacer zoom interactivo con Plotly."

3. *(1:25 – 1:45)* "Cambio a la pestaña de presión y luego a la de índice de riesgo. El índice está calculado en el ESP32 con la lógica `ángulo > 30° + presencia sostenida`."

4. *(1:45 – 2:05)* "La distribución del ángulo nos muestra que la mayoría del tiempo estamos por debajo del umbral, pero hay una cola larga hacia los 50 grados. El pie chart confirma: **CORRECTA 55%, INADECUADA 34%, LÍMITE 11%**."

5. *(2:05 – 2:30)* "El mapa de calor hora × día sirve para detectar **patrones**: las horas con peor ergonomía suelen ser después del almuerzo, cuando la atención baja."

---

## Bloque 4 — Análisis básico (2:30 – 3:30)

**Voz:**

1. *(2:30 – 2:50)* "Bajamos al panel de análisis. La tabla descriptiva muestra media, desviación, mínimos y máximos para cada variable."

2. *(2:50 – 3:10)* "La matriz de correlación tiene un hallazgo clave: el **ángulo correlaciona 0.69 con el índice de riesgo**, validando que nuestra fórmula en el ESP32 es coherente. La presión tiene correlación baja, lo cual confirma que es información independiente — útil como detector de ocupación."

3. *(3:10 – 3:30)* "Abajo, los **eventos sostenidos de mala postura**: 1 evento de 60 segundos en este turno. El dashboard prioriza por duración × ángulo máximo: lo que el supervisor debe revisar primero."

---

## Bloque 5 — Justificación de tecnologías (3:30 – 4:20)

**En pantalla:** tabla resumen.

**Voz:**

> "Tres decisiones clave:
> 
> Primero, **InfluxDB Cloud** como almacenamiento porque está diseñado para series temporales IoT: compresión nativa, retención automática y Flux para consultas — comparado con PostgreSQL o MongoDB, ahorra 70% de espacio sin perder fidelidad.
> 
> Segundo, **MQTT con HiveMQ Cloud** porque cada mensaje pesa 80 bytes contra 400 de HTTP — crítico para un ESP32 que en fase futura irá con batería.
> 
> Tercero, **Streamlit + Plotly** en lugar de Grafana porque nos permite mezclar visualización con análisis estadístico en pandas dentro de la misma aplicación. Grafana es excelente para dashboards puros, pero Streamlit nos da control total del diseño y el análisis correlacional que la rúbrica exige."

---

## Bloque 6 — Cierre y toma de decisiones (4:20 – 4:50)

**Voz:**

> "El dashboard responde tres preguntas operativas:
> 
> 1. ¿Está la persona sentada correctamente ahora mismo? → KPI y línea de umbral.
> 2. ¿Cuándo durante el día empeora la postura? → mapa de calor horario.
> 3. ¿Qué eventos requieren intervención? → tabla priorizada por duración.
> 
> Con esta información, un supervisor puede programar pausas activas en las franjas críticas o ajustar la altura del escritorio. Esa es la promesa de IoT: datos que se traducen en acción.
> 
> Gracias."

**En pantalla:** logos Universidad de La Salle + ErgIoT + frame final con nombres de integrantes.

---

## Checklist técnico antes de grabar

- [ ] App corriendo en `http://localhost:8501` con datos cargados (ventana 7d)
- [ ] Cerrar pestañas innecesarias del navegador
- [ ] Ajustar zoom del navegador a 110-125% para legibilidad en video
- [ ] Probar audio del micrófono (silenciar Discord/Slack)
- [ ] OBS Studio o Loom con resolución 1080p a 30 fps
- [ ] Habilitar puntero del mouse resaltado para que se vea bien en pantalla
- [ ] Guardar como MP4 H.264 (compatible con la plataforma de entrega)
- [ ] **Crítico:** los nombres deben estar visibles entre 0:00 y 0:10
