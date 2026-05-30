"""Dashboard ergonómico — Módulo 5 IoT.

Universidad de La Salle | Internet de las Cosas G02 | 2026-1
Autores: Mario Esteban Vargas Pisco · Yeison Esteven García Olaya
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import analytics
from config import (
    UMBRAL_ANGULO_DEG,
    LASALLE_AZUL_PRIMARIO,
    LASALLE_AZUL_MEDIO,
    LASALLE_DORADO,
    LASALLE_DORADO_OSCURO,
    LASALLE_TEXTO,
    LASALLE_FONDO_GRIS,
    COLOR_MALA,
    ESCALA_RIESGO,
)
from data_loader import fetch_dataframe

st.set_page_config(
    page_title="ErgIoT — Monitoreo Ergonómico",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Estilos institucionales La Salle ----------
st.markdown(
    f"""
    <style>
      /* Header franja institucional */
      header[data-testid="stHeader"] {{
        background: linear-gradient(90deg, {LASALLE_AZUL_PRIMARIO} 0%, {LASALLE_AZUL_MEDIO} 100%);
      }}
      header[data-testid="stHeader"] * {{ color: #fff !important; }}

      /* Sidebar */
      section[data-testid="stSidebar"] {{
        background-color: {LASALLE_FONDO_GRIS};
        border-right: 4px solid {LASALLE_DORADO};
      }}

      /* Títulos */
      h1, h2, h3 {{ color: {LASALLE_AZUL_PRIMARIO}; }}
      h1 {{ border-bottom: 3px solid {LASALLE_DORADO}; padding-bottom: 8px; }}

      /* KPI cards */
      div[data-testid="stMetric"] {{
        background: #fff;
        border-left: 4px solid {LASALLE_DORADO};
        border-radius: 6px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,48,87,.08);
      }}
      div[data-testid="stMetricLabel"] {{ color: {LASALLE_AZUL_MEDIO}; font-weight: 600; }}
      div[data-testid="stMetricValue"] {{ color: {LASALLE_AZUL_PRIMARIO}; }}

      /* Botones */
      .stButton > button {{
        background-color: {LASALLE_DORADO};
        color: {LASALLE_TEXTO};
        border: none;
        font-weight: 600;
      }}
      .stButton > button:hover {{
        background-color: {LASALLE_DORADO_OSCURO};
        color: #fff;
      }}

      /* Tabs */
      .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {LASALLE_AZUL_PRIMARIO};
        border-bottom-color: {LASALLE_DORADO};
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=30)
def cargar(rango: str) -> pd.DataFrame:
    return fetch_dataframe(rango)


# ---------------------------------------------------------------- Sidebar
with st.sidebar:
    st.markdown("## ErgIoT")
    st.caption("Universidad de La Salle · IoT G02 · 2026-1")
    st.markdown("**Autores:**")
    st.markdown("- Mario Esteban Vargas Pisco")
    st.markdown("- Yeison Esteven García Olaya")
    st.divider()

    rango = st.selectbox(
        "Ventana temporal",
        options=["-1h", "-6h", "-24h", "-7d", "-30d", "-90d"],
        index=4,
        format_func=lambda x: {
            "-1h": "Última hora",
            "-6h": "Últimas 6 horas",
            "-24h": "Últimas 24 horas",
            "-7d": "Últimos 7 días",
            "-30d": "Últimos 30 días",
            "-90d": "Últimos 90 días",
        }[x],
    )
    refrescar = st.button("Refrescar datos", use_container_width=True)
    if refrescar:
        st.cache_data.clear()

    st.divider()
    st.caption(
        f"Umbral ángulo: **{UMBRAL_ANGULO_DEG}°**\n\n"
        "Fuente: InfluxDB Cloud · bucket `ErgIoT_Bucket`"
    )


# ---------------------------------------------------------------- Header
st.title("Monitoreo Ergonómico en Tiempo Real")
st.caption(
    "Sistema IoT — ESP32 + MPU-6050 + FSR402 → MQTT → InfluxDB Cloud → Streamlit"
)

df = cargar(rango)

if df.empty:
    st.warning("Sin datos en la ventana seleccionada. Ajusta el rango temporal.")
    st.stop()

k = analytics.kpis(df)


# ---------------------------------------------------------------- KPIs
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Lecturas", f"{k['n_puntos']:,}")
c2.metric("Ángulo medio", f"{k['angulo_medio']:.1f}°")
c3.metric("Ángulo P95", f"{k['angulo_p95']:.1f}°", help="Percentil 95 de inclinación")
c4.metric("Postura correcta", f"{k['pct_postura_correcta']:.1f}%",
          help=f"% de tiempo con ángulo ≤ {UMBRAL_ANGULO_DEG}° estando sentado")
c5.metric("Ocupación silla", f"{k['pct_ocupacion']:.1f}%")

st.caption(
    f"Rango: **{k['rango_inicio']:%Y-%m-%d %H:%M}** → "
    f"**{k['rango_fin']:%Y-%m-%d %H:%M}** (hora Bogotá)"
)
st.divider()


# ---------------------------------------------------------------- Series temporales
st.subheader("Series temporales")
tab1, tab2, tab3 = st.tabs([" Ángulo de inclinación ", " Presión del asiento ", " Índice de riesgo "])

with tab1:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["time"], y=df["angulo_grados"], mode="lines",
            name="Ángulo (°)", line=dict(color=LASALLE_AZUL_PRIMARIO, width=2),
        )
    )
    fig.add_hline(
        y=UMBRAL_ANGULO_DEG, line_dash="dash", line_color=COLOR_MALA,
        annotation_text=f"Umbral mala postura: {UMBRAL_ANGULO_DEG}°",
        annotation_position="top left",
    )
    fig.update_layout(
        height=380, margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="Tiempo", yaxis_title="Ángulo (°)",
        hovermode="x unified",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    if "presion_adc" in df:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["time"], y=df["presion_adc"], mode="lines",
                name="Presión (ADC)", line=dict(color=LASALLE_AZUL_MEDIO, width=2),
            )
        )
        fig.update_layout(
            height=380, margin=dict(l=0, r=0, t=20, b=0),
            xaxis_title="Tiempo", yaxis_title="Lectura ADC (0-4095)",
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos de presión en esta ventana.")

with tab3:
    if "indice_riesgo" in df and df["indice_riesgo"].notna().any():
        fig = px.area(
            df, x="time", y="indice_riesgo",
            color_discrete_sequence=[LASALLE_DORADO],
            labels={"time": "Tiempo", "indice_riesgo": "Índice de riesgo"},
        )
        fig.update_layout(height=380, margin=dict(l=0, r=0, t=20, b=0), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin datos de índice de riesgo en esta ventana.")


# ---------------------------------------------------------------- Distribución + clasif riesgo
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Distribución del ángulo")
    fig = px.histogram(
        df, x="angulo_grados", nbins=30,
        color_discrete_sequence=[LASALLE_AZUL_PRIMARIO],
        labels={"angulo_grados": "Ángulo (°)"},
    )
    fig.add_vline(
        x=UMBRAL_ANGULO_DEG, line_dash="dash", line_color=COLOR_MALA,
        annotation_text=f"{UMBRAL_ANGULO_DEG}°", annotation_position="top",
    )
    fig.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0),
                      yaxis_title="Frecuencia")
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("Clasificación de riesgo")
    dist = analytics.distribucion_riesgo(df)
    if not dist.empty:
        fig = px.pie(
            names=dist.index, values=dist.values, hole=0.4,
            color_discrete_sequence=[LASALLE_AZUL_PRIMARIO, LASALLE_DORADO, COLOR_MALA, LASALLE_AZUL_MEDIO],
        )
        fig.update_layout(height=320, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sin clasificación de riesgo disponible.")


# ---------------------------------------------------------------- Heatmap horario
st.subheader("Mapa de calor — ángulo medio por hora y día")
heat = analytics.heatmap_horario(df)
if not heat.empty and heat.size > 1:
    fig = px.imshow(
        heat, color_continuous_scale=ESCALA_RIESGO,
        labels=dict(x="Hora del día", y="Día", color="Ángulo °"),
        aspect="auto",
    )
    fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Necesitas datos en varias horas/días para ver el mapa de calor.")


# ---------------------------------------------------------------- Análisis básico
st.divider()
st.subheader("Análisis básico de los datos")

col_a, col_b = st.columns([1, 1])

with col_a:
    st.markdown("**Estadísticas descriptivas**")
    desc_cols = [c for c in ["angulo_grados", "presion_adc", "indice_riesgo", "tiempo_sentado"] if c in df]
    if desc_cols:
        st.dataframe(
            df[desc_cols].describe().round(2),
            use_container_width=True,
        )

with col_b:
    st.markdown("**Correlación entre variables**")
    corr = analytics.matriz_correlacion(df)
    if not corr.empty:
        fig = px.imshow(
            corr.round(2),
            text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1,
        )
        fig.update_layout(height=340, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Insuficientes columnas numéricas para correlación.")


# ---------------------------------------------------------------- Eventos
st.subheader("Eventos de mala postura detectados")
ev = analytics.detectar_eventos_mala_postura(df)
if ev.empty:
    st.success(
        f"No se detectaron eventos sostenidos de mala postura "
        f"(umbral {UMBRAL_ANGULO_DEG}° por más de 10s)."
    )
else:
    total_min = ev["duracion_s"].sum() / 60
    c1, c2, c3 = st.columns(3)
    c1.metric("Eventos", len(ev))
    c2.metric("Tiempo total en mala postura", f"{total_min:.1f} min")
    c3.metric("Evento más largo", f"{ev['duracion_s'].max():.0f} s")
    st.dataframe(
        ev.assign(
            inicio=lambda d: d["inicio"].dt.strftime("%Y-%m-%d %H:%M:%S"),
            fin=lambda d: d["fin"].dt.strftime("%H:%M:%S"),
            duracion_s=lambda d: d["duracion_s"].round(0),
            angulo_max=lambda d: d["angulo_max"].round(1),
            angulo_medio=lambda d: d["angulo_medio"].round(1),
        ),
        use_container_width=True, hide_index=True,
    )


# ---------------------------------------------------------------- Footer
st.divider()
st.caption(
    "Dashboard construido con Streamlit + Plotly · Datos en vivo desde InfluxDB Cloud · "
    "Pipeline: ESP32 → MQTT → InfluxDB Cloud → Streamlit"
)
