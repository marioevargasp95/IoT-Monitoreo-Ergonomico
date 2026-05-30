# Guion del video — Módulo 5 IoT (máx. 5 min)

**Curso:** Internet de las Cosas — Grupo 02 · 2026-1
**Proyecto:** ErgIoT — Monitoreo Ergonómico en Tiempo Real
**Duración objetivo:** 4:50

> Cifras tomadas del bucket `ErgIoT_Bucket` con 1440 lecturas reales
> (3–7 de mayo de 2026). Si vuelves a grabar y los datos cambiaron,
> ejecuta `python _kpis_video.py` para obtener las nuevas cifras.

---

## Bloque 1 — Portada con créditos (0:00 – 0:10) · **OBLIGATORIO**

**En pantalla** (texto grande, sobre fondo institucional azul marino + dorado):

> **ErgIoT — Monitoreo Ergonómico en Tiempo Real**
> Universidad de La Salle · Internet de las Cosas G02 · 2026-1
>
> **Integrantes:**
> - Mario Esteban Vargas Pisco
> - Yeison Esteven García Olaya
>
> *Módulo 5 — Visualización y análisis de datos IoT*

**Voz:**
> "Buenas, somos Mario Vargas y Yeison García, del grupo 02 de Internet de las Cosas. Presentamos el Módulo 5 del proyecto ErgIoT, dashboard de visualización y análisis."

---

## Bloque 2 — Contexto y arquitectura (0:10 – 0:50)

**Voz:**
> "Construimos un sistema IoT que captura postura sentada con un ESP32, un acelerómetro MPU-6050 y un sensor de presión FSR402. Las lecturas viajan por MQTT a HiveMQ Cloud, se almacenan en InfluxDB Cloud y se visualizan en un dashboard Streamlit que diseñamos con la paleta institucional de la Universidad de La Salle."

**En pantalla:** diagrama del pipeline
```
[MPU-6050]  →  ESP32 (MicroPython)  →  MQTT  →  InfluxDB Cloud  →  Streamlit + Plotly
[FSR402]    →
[LED RGB]   ←
```

**Voz:**
> "Capturamos 7 variables: ángulo del tronco, presión del asiento, presencia, clasificación de riesgo, índice de riesgo, tiempo sentado acumulado y la bandera de pausa activa."

---

## Bloque 3 — Demo del dashboard (0:50 – 2:30)

> Abrir en vivo `http://localhost:8501` y navegar las tres páginas.

### Página 1 — Monitoreo Ergonómico (0:50 – 1:30)

**Voz:**
> "Esta es la vista principal. Arriba están los KPIs sobre 1440 lecturas reales: ángulo medio de 17.9 grados, percentil 95 de 36 grados, y **84% del tiempo en postura correcta**. La línea roja punteada en 30 grados es nuestro umbral ergonómico — visualmente sabemos cuándo el operador cruzó el límite."

> "El mapa de calor hora × día muestra que el **7 de mayo tuvimos peor postura** — solo 67% correcta — frente al 97% del 5 de mayo. Eso es el tipo de patrón accionable que un dashboard debe revelar."

### Página 2 — Buena Postura (1:30 – 2:00)

**Voz:**
> "Cambiamos a la vista de Buena Postura, donde aplicamos refuerzo positivo en vez de solo alertar. El banner muestra el estado actual del sensor, hay un sistema de 6 logros desbloqueables, y un gráfico de las **116 sesiones doradas** detectadas: períodos largos de postura correcta. Esto es importante: no solo regañamos, también motivamos."

### Página 3 — Pausas Activas (2:00 – 2:30)

**Voz:**
> "La tercera vista usa los campos `tiempo_sentado` y `alerta_pausa`. El sistema **detecta automáticamente el umbral del firmware en 50.5 minutos**. En este turno se disparó una alerta cuando el usuario llegó a 68 minutos sin levantarse. Las bandas doradas pintan los intervalos en alerta. Cuando se dispara, el dashboard recomienda rutinas de pausa activa de 2–3 minutos."

---

## Bloque 4 — Análisis básico de los datos (2:30 – 3:30)

**Voz:**
> "Implementamos análisis estadístico embebido en el dashboard:"

1. *(2:30 – 2:50)* "Estadística descriptiva sobre las 1440 lecturas: media, desviación, mínimos, máximos por variable."

2. *(2:50 – 3:10)* "Matriz de correlación con hallazgo clave: **el ángulo correlaciona 0.76 con el índice de riesgo**, validando que la fórmula que programamos en el ESP32 es coherente. Es la evidencia matemática de que el firmware está funcionando bien."

3. *(3:10 – 3:30)* "Detección automática de eventos: **31 eventos de mala postura sostenida** detectados, con 24.5 minutos totales. El evento más largo duró 2 minutos y medio. La tabla los prioriza por duración × ángulo máximo: lo que el supervisor debe revisar primero."

---

## Bloque 5 — Justificación de tecnologías (3:30 – 4:20)

**En pantalla:** tabla resumen 4 columnas.

**Voz:**

> "Cuatro decisiones técnicas clave:"

1. **InfluxDB Cloud** — *"Diseñado nativamente para series temporales IoT. Comprime mejor que PostgreSQL, tiene lenguaje Flux para downsampling, y free tier sin tarjeta. Comparado con ThingsBoard, separa almacenamiento de visualización: podemos cambiar de dashboard sin tocar los datos."*

2. **MQTT con HiveMQ Cloud** — *"Cada mensaje pesa 80 bytes contra 400 de HTTP. Crítico para un ESP32 que en fase futura irá con batería."*

3. **Streamlit + Plotly** — *"Permite unir visualización y análisis estadístico de pandas en una sola aplicación Python. Grafana es excelente para dashboards puros, pero Streamlit nos da control total del diseño institucional y permite mezclar análisis con vista en vivo."*

4. **Paleta La Salle** — *"Extraída del sitio oficial: azul marino `#003057` como primario, dorado `#f2a900` como acento. Identidad visual coherente en las tres páginas."*

---

## Bloque 6 — Cierre y toma de decisiones (4:20 – 4:50)

**Voz:**

> "El dashboard responde tres preguntas operativas:"
>
> 1. **¿Cómo estoy ahora?** → flag y KPIs en tiempo real.
> 2. **¿Cuándo durante el día empeoro?** → mapa de calor horario.
> 3. **¿Qué intervenciones priorizar?** → tabla de eventos y alertas de pausa.
>
> "Con esta información, un supervisor puede programar pausas activas en franjas críticas o ajustar la altura del escritorio. Esa es la promesa de IoT: **datos que se traducen en acción**."
>
> "El proyecto está publicado en GitHub: `marioevargasp95/IoT-Monitoreo-Ergonomico`. Gracias."

**En pantalla:** logo La Salle + ErgIoT + nombres de integrantes + URL del repo.

---

## Checklist técnico antes de grabar

- [ ] App corriendo en `http://localhost:8501` con ventana 30 días (1440 puntos)
- [ ] Verificar que las tres páginas cargan (`Monitoreo`, `Buena_Postura`, `Pausas_Activas`)
- [ ] Cerrar pestañas innecesarias del navegador
- [ ] Zoom del navegador a 110-125% para legibilidad en video
- [ ] Audio del micrófono probado, silenciar Discord/Slack/Teams
- [ ] OBS Studio o Loom a 1080p / 30 fps
- [ ] Cursor del mouse resaltado
- [ ] Guardar como MP4 H.264
- [ ] **Crítico:** los dos nombres deben estar visibles entre 0:00 y 0:10
