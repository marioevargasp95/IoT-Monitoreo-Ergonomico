"""Vista de Pausas Activas — usa `alerta_pausa` y `tiempo_sentado`.

Detecta cuando la persona lleva demasiado tiempo sentada y muestra
cuándo y por cuánto se disparó la bandera de pausa activa.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import analytics
from config import (
    UMBRAL_ANGULO_DEG,
    LASALLE_AZUL_PRIMARIO,
    LASALLE_AZUL_MEDIO,
    LASALLE_AZUL_CLARO,
    LASALLE_DORADO,
    LASALLE_DORADO_OSCURO,
    LASALLE_TEXTO,
    LASALLE_FONDO_GRIS,
    COLOR_MALA,
)
from data_loader import fetch_dataframe

st.set_page_config(
    page_title="Pausas Activas — ErgIoT",
    page_icon="⏱️",
    layout="wide",
)

st.markdown(
    f"""
    <style>
      header[data-testid="stHeader"] {{
        background: linear-gradient(90deg, {LASALLE_AZUL_PRIMARIO} 0%, {LASALLE_AZUL_MEDIO} 100%);
      }}
      header[data-testid="stHeader"] * {{ color: #fff !important; }}
      section[data-testid="stSidebar"] {{
        background-color: {LASALLE_FONDO_GRIS};
        border-right: 4px solid {LASALLE_DORADO};
      }}
      h1, h2, h3 {{ color: {LASALLE_AZUL_PRIMARIO}; }}
      h1 {{ border-bottom: 3px solid {LASALLE_DORADO}; padding-bottom: 8px; }}
      div[data-testid="stMetric"] {{
        background: #fff;
        border-left: 4px solid {LASALLE_DORADO};
        border-radius: 6px;
        padding: 12px 16px;
        box-shadow: 0 1px 3px rgba(0,48,87,.08);
      }}
      div[data-testid="stMetricLabel"] {{ color: {LASALLE_AZUL_MEDIO}; font-weight: 600; }}
      div[data-testid="stMetricValue"] {{ color: {LASALLE_AZUL_PRIMARIO}; }}
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
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=30)
def cargar(rango: str) -> pd.DataFrame:
    return fetch_dataframe(rango)


with st.sidebar:
    st.markdown("## Pausas Activas")
    st.caption("Tiempo sentado y alertas para moverse")
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
    if st.button("Refrescar datos", use_container_width=True):
        st.cache_data.clear()


st.title("Pausas Activas")
st.caption(
    "Usa los campos `tiempo_sentado` (minutos acumulados) y `alerta_pausa` "
    "(bandera 0/1) que publica el ESP32 hacia InfluxDB."
)

df = cargar(rango)
if df.empty:
    st.warning("Sin datos en la ventana seleccionada.")
    st.stop()

k = analytics.kpis_pausa(df)


# ---------------------------------------------------------------- Banner estado
en_alerta = bool(df["alerta_pausa"].iloc[-1]) if "alerta_pausa" in df else False
tiempo_actual = float(df["tiempo_sentado"].iloc[-1]) if "tiempo_sentado" in df else 0.0

if en_alerta:
    color = COLOR_MALA
    emoji = "🚨"
    titulo = "ES MOMENTO DE UNA PAUSA ACTIVA"
    sub = f"Llevas {tiempo_actual:.1f} minutos sentado. Levántate y estírate al menos 2-3 min."
elif tiempo_actual >= k.get("umbral_alerta_min", 50) * 0.8:
    color = LASALLE_DORADO
    emoji = "⏳"
    titulo = "PAUSA RECOMENDADA PRONTO"
    sub = f"Llevas {tiempo_actual:.1f} min — cerca del umbral. Termina lo que estás haciendo y muévete."
else:
    color = LASALLE_AZUL_PRIMARIO
    emoji = "✅"
    titulo = "TIEMPO BAJO CONTROL"
    sub = f"Llevas {tiempo_actual:.1f} min sentado. El próximo aviso será a los {k.get('umbral_alerta_min', 50):.0f} min."

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, {color}15 0%, {color}30 100%);
        border-left: 8px solid {color};
        border-radius: 12px;
        padding: 24px 28px;
        margin: 6px 0 22px 0;
    ">
      <div style="font-size: 52px; line-height: 1;">{emoji}</div>
      <div style="font-size: 30px; font-weight: 700; color: {color}; margin-top: 4px;">
          {titulo}
      </div>
      <div style="font-size: 17px; color: #444; margin-top: 6px;">{sub}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Tiempo sentado actual",
    f"{k['tiempo_sentado_actual']:.1f} min",
    help="Último valor reportado por el sensor",
)
c2.metric(
    "Máximo sin pausa",
    f"{k['tiempo_sentado_max']:.0f} min",
    help="La sesión continua más larga sin levantarse",
)
c3.metric(
    "Umbral activación",
    f"{k['umbral_alerta_min']:.0f} min",
    help="Valor de tiempo_sentado donde el firmware empieza a alertar",
)
c4.metric(
    "Veces en alerta",
    f"{k['n_eventos_alerta']}",
    delta=f"{k['pct_tiempo_en_alerta']:.1f}% del tiempo",
    help="Cantidad de eventos donde se activó alerta_pausa",
)


# ---------------------------------------------------------------- Serie temporal
st.divider()
st.subheader("Tiempo sentado acumulado vs alerta de pausa")
st.caption(
    "La línea muestra el acumulado de minutos sentado. "
    "Cuando alerta_pausa = 1 se pinta una banda dorada de fondo."
)

fig = go.Figure()

# Bandas de alerta (zonas pintadas)
ev = analytics.eventos_alerta_pausa(df)
for _, e in ev.iterrows():
    fig.add_vrect(
        x0=e["inicio"], x1=e["fin"],
        fillcolor=LASALLE_DORADO, opacity=0.18,
        layer="below", line_width=0,
    )

# Línea de tiempo_sentado
fig.add_trace(go.Scatter(
    x=df["time"], y=df["tiempo_sentado"],
    mode="lines",
    line=dict(color=LASALLE_AZUL_PRIMARIO, width=2.5),
    name="Tiempo sentado (min)",
    hovertemplate="%{x|%Y-%m-%d %H:%M}<br>%{y:.1f} min<extra></extra>",
))

# Línea horizontal del umbral
if k["umbral_alerta_min"] and not pd.isna(k["umbral_alerta_min"]):
    fig.add_hline(
        y=k["umbral_alerta_min"], line_dash="dash", line_color=COLOR_MALA,
        annotation_text=f"Umbral: {k['umbral_alerta_min']:.0f} min",
        annotation_position="top left",
    )

fig.update_layout(
    height=400, margin=dict(l=0, r=0, t=10, b=0),
    xaxis_title="Tiempo", yaxis_title="Minutos sentado",
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------- Eventos detectados
st.divider()
st.subheader("Eventos de alerta de pausa")

if ev.empty:
    st.success(
        "No se han disparado alertas de pausa en esta ventana. "
        "El sensor confirma que el usuario está rotando entre sentarse y levantarse."
    )
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de eventos", len(ev))
    c2.metric("Duración promedio", f"{ev['duracion_s'].mean()/60:.1f} min")
    c3.metric("Evento más largo", f"{ev['duracion_s'].max()/60:.1f} min")

    tabla = ev.assign(
        inicio=lambda d: d["inicio"].dt.strftime("%Y-%m-%d %H:%M:%S"),
        fin=lambda d: d["fin"].dt.strftime("%H:%M:%S"),
        duracion_min=lambda d: (d["duracion_s"] / 60).round(1),
        tiempo_sentado_max=lambda d: d["tiempo_sentado_max"].round(1),
    )[["inicio", "fin", "duracion_min", "tiempo_sentado_max", "n_muestras"]]
    st.dataframe(tabla, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------- Distribución por hora
st.divider()
st.subheader("¿En qué horas se acumulan más alertas?")

if "alerta_pausa" in df:
    aux = df.copy()
    aux["hora"] = aux["time"].dt.hour
    por_hora = aux.groupby("hora")["alerta_pausa"].sum().reset_index()
    por_hora = por_hora[por_hora["alerta_pausa"] > 0]

    if por_hora.empty:
        st.info("Sin alertas por hora todavía.")
    else:
        fig = px.bar(
            por_hora, x="hora", y="alerta_pausa",
            color_discrete_sequence=[LASALLE_DORADO],
            labels={"hora": "Hora del día", "alerta_pausa": "Muestras en alerta"},
        )
        fig.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(dtick=1),
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------- Recomendaciones
st.divider()
st.subheader("Pausas activas recomendadas (2–3 min)")
st.markdown(
    """
    Cuando se dispara la alerta, intenta una de estas rutinas rápidas:

    | Ejercicio | Duración | Beneficio |
    |---|---|---|
    | **Estiramiento de cuello** (rotación lenta) | 30 s | Libera tensión cervical |
    | **Hombros arriba-abajo** (10 repeticiones) | 30 s | Activa trapecio y zona dorsal |
    | **Caminata corta + agua** | 60 s | Reactiva circulación |
    | **Estiramiento de muñecas** | 30 s | Previene síndrome del túnel carpiano |
    | **Mirar a 20 pies por 20 segundos** | 20 s | Regla 20-20-20 para fatiga visual |

    > El firmware del ESP32 activa `alerta_pausa = 1` cuando `tiempo_sentado` supera el
    > umbral configurado. El contador se reinicia cuando el sensor detecta que el
    > usuario se levantó (presión del asiento < umbral durante varias muestras).
    """
)
