# Presentación HTML — Módulo 5

12 diapositivas autocontenidas en un solo archivo HTML. Sin dependencias
externas: usa la paleta y el logo institucional de la Universidad de La Salle.

## Cómo usarla

**Doble-clic en `index.html`** — se abre en tu navegador y ya está lista.

## Controles

| Acción | Cómo |
|---|---|
| Siguiente slide | `→`, `Espacio`, `PgDn`, o clic en la mitad derecha |
| Anterior slide | `←`, `PgUp`, o clic en la mitad izquierda |
| Ir al inicio | `Home` |
| Ir al final | `End` |
| Pantalla completa | `F` o botón ⛶ |
| Imprimir / exportar PDF | `P`, `Ctrl + P`, o botón 🖨️ |

## Exportar a PDF (para entregar)

1. Abre la presentación
2. `Ctrl + P` (o botón 🖨️)
3. Destino: **Guardar como PDF**
4. Orientación: **Horizontal**
5. Tamaño: **A4** o **Letter**
6. Márgenes: **Ninguno** (importante)
7. Guardar

## Estructura

```
presentacion/
├── index.html         # Las 12 slides
├── README.md
└── assets/
    └── logo_lasalle.png
```

## Contenido por slide

1. Portada con créditos
2. Problema (sedentarismo y postura)
3. Objetivo del Módulo 5
4. Arquitectura del sistema (pipeline)
5. Hardware + modelo de datos InfluxDB
6. Dashboard · Monitoreo Ergonómico
7. Dashboard · Buena Postura
8. Dashboard · Pausas Activas
9. **Resultados reales** (4 KPIs grandes sobre 1440 lecturas)
10. Análisis básico embebido
11. Justificación de tecnologías
12. Conclusiones y cierre

## Si los datos cambian

Las cifras de los slides 6, 9 y 10 están calculadas sobre 1440 lecturas reales
del 3 al 7 de mayo. Si quieres actualizarlas, ejecuta:

```powershell
cd ..
python _kpis_video.py
```

Y edita los valores en el HTML.
