"""Vista de Buena Postura — flags positivos, rachas y sesiones doradas.

Refuerzo positivo: en lugar de solo mostrar alertas de mala postura,
celebra los momentos en los que la persona se mantiene bien sentada.
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
    COLOR_EXCELENTE,
    COLOR_BUENA,
    COLOR_LIMITE,
    COLOR_MALA,
    COLOR_AUSENTE,
)
from data_loader import fetch_dataframe

st.set_page_config(
    page_title="Buena Postura — ErgIoT",
    page_icon="🌿",
    layout="wide",
)

# ---------- Estilos institucionales La Salle (mismos que app.py) ----------
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


# ---------------------------------------------------------------- Sidebar
with st.sidebar:
    st.markdown("## Buena Postura")
    st.caption("Indicadores de refuerzo positivo")
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


# ---------------------------------------------------------------- Header
st.title("Vista de Buena Postura")
st.caption("Celebra lo que estás haciendo bien — refuerzo positivo basado en datos en vivo.")

df = cargar(rango)
if df.empty:
    st.warning("Sin datos en la ventana seleccionada.")
    st.stop()


# ---------------------------------------------------------------- Flag actual
estado = analytics.estado_actual(df)

FLAG_STYLES = {
    "EXCELENTE":  {"emoji": "🌟", "color": COLOR_EXCELENTE, "msg": "EXCELENTE POSTURA",
                    "sub": "Tu espalda está perfectamente alineada. ¡Sigue así!"},
    "BUENA":      {"emoji": "🌿", "color": COLOR_BUENA, "msg": "BUENA POSTURA",
                    "sub": "Estás dentro del rango ergonómico recomendado."},
    "LIMITE":     {"emoji": "⚠️", "color": COLOR_LIMITE, "msg": "EN EL LÍMITE",
                    "sub": "Estás cerca del umbral. Ajusta ligeramente la espalda."},
    "MALA":       {"emoji": "🔴", "color": COLOR_MALA, "msg": "CORRIGE LA POSTURA",
                    "sub": "Endereza la espalda. Pequeños ajustes evitan dolor a largo plazo."},
    "AUSENTE":    {"emoji": "💤", "color": COLOR_AUSENTE, "msg": "USUARIO AUSENTE",
                    "sub": "No se detecta presencia en el asiento."},
    "SIN_DATOS":  {"emoji": "❓", "color": COLOR_AUSENTE, "msg": "SIN DATOS",
                    "sub": "Esperando lecturas del sensor."},
}
s = FLAG_STYLES[estado["flag"]]

st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, {s['color']}22 0%, {s['color']}44 100%);
        border-left: 8px solid {s['color']};
        border-radius: 12px;
        padding: 28px 32px;
        margin: 8px 0 24px 0;
    ">
      <div style="font-size: 64px; line-height: 1; margin-bottom: 4px;">{s['emoji']}</div>
      <div style="font-size: 36px; font-weight: 700; color: {s['color']}; letter-spacing: 0.5px;">
          {s['msg']}
      </div>
      <div style="font-size: 18px; color: #444; margin-top: 6px;">{s['sub']}</div>
      <div style="font-size: 13px; color: #777; margin-top: 14px;">
          Último registro: <b>{estado.get('timestamp')}</b> ·
          Ángulo: <b>{estado.get('angulo', 0):.1f}°</b> ·
          Ocupación: <b>{'Sí' if estado.get('ocupado') else 'No'}</b>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- Impacto visual de los flags
st.divider()
st.subheader("Impacto de los flags a lo largo del tiempo")
st.caption(
    "Cada punto del sensor se etiqueta con un flag según el ángulo y la presencia. "
    "Aquí ves directamente cuánto tiempo estuviste en cada estado."
)

FLAG_COLOR = {
    "EXCELENTE": COLOR_EXCELENTE,
    "BUENA":     COLOR_BUENA,
    "LIMITE":    COLOR_LIMITE,
    "MALA":      COLOR_MALA,
    "AUSENTE":   COLOR_AUSENTE,
}

df_flag = analytics.df_con_flags(df)

col_serie, col_donut = st.columns([2, 1])

with col_serie:
    fig = go.Figure()
    # Línea fina de fondo para dar continuidad
    fig.add_trace(go.Scatter(
        x=df_flag["time"], y=df_flag["angulo_grados"],
        mode="lines", line=dict(color="#cccccc", width=1),
        name="Trazo", showlegend=False, hoverinfo="skip",
    ))
    # Puntos coloreados por flag
    for flag, color in FLAG_COLOR.items():
        sub = df_flag[df_flag["flag"] == flag]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["time"], y=sub["angulo_grados"],
            mode="markers",
            name=flag,
            marker=dict(color=color, size=7, line=dict(width=0)),
            hovertemplate=(
                f"<b>{flag}</b><br>%{{x|%Y-%m-%d %H:%M:%S}}<br>"
                "Ángulo: %{y:.1f}°<extra></extra>"
            ),
        ))
    fig.add_hline(
        y=UMBRAL_ANGULO_DEG, line_dash="dash", line_color=COLOR_MALA,
        annotation_text=f"Umbral {UMBRAL_ANGULO_DEG}°",
        annotation_position="top left",
    )
    fig.add_hline(
        y=UMBRAL_ANGULO_DEG * 0.7, line_dash="dot",
        line_color=COLOR_EXCELENTE,
        annotation_text=f"Excelente ≤ {UMBRAL_ANGULO_DEG*0.7:.0f}°",
        annotation_position="bottom left",
    )
    fig.update_layout(
        height=380, margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="Tiempo", yaxis_title="Ángulo (°)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig, use_container_width=True)

with col_donut:
    tpf = analytics.tiempo_por_flag(df)
    if tpf.empty or tpf["segundos"].sum() == 0:
        st.info("Sin datos para distribución de flags.")
    else:
        tpf["etiqueta"] = tpf.apply(
            lambda r: f"{r['flag']}<br>{r['minutos']:.1f} min", axis=1,
        )
        fig = go.Figure(data=[go.Pie(
            labels=tpf["flag"].astype(str),
            values=tpf["segundos"],
            hole=0.55,
            marker=dict(colors=[FLAG_COLOR[f] for f in tpf["flag"].astype(str)]),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value:.0f} s<br>(%{percent})<extra></extra>",
        )])
        total_min = tpf["segundos"].sum() / 60
        fig.update_layout(
            height=380, margin=dict(l=0, r=0, t=20, b=0),
            showlegend=False,
            annotations=[dict(
                text=f"<b>{total_min:.0f}</b><br>min totales",
                x=0.5, y=0.5, font_size=18, showarrow=False,
            )],
        )
        st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------- Métricas de buena postura
racha = analytics.racha_actual(df)
mejor = analytics.mejor_racha(df)
pct_buena_total = float((df[df.get("ocupado", 0) > 0]["angulo_grados"] <= UMBRAL_ANGULO_DEG).mean() * 100)

c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Racha actual",
    f"{racha['duracion_s']/60:.1f} min" if racha['duracion_s'] > 0 else "0 min",
    help="Tiempo continuo con ángulo ≤ umbral al final de la serie.",
)
c2.metric(
    "Mejor sesión",
    f"{mejor['duracion_s']/60:.1f} min",
    help="Sesión dorada más larga registrada en la ventana.",
)
c3.metric(
    "% Buena postura",
    f"{pct_buena_total:.1f}%",
    help="Porcentaje de muestras con buena postura estando sentado.",
)
c4.metric(
    "Umbral activo",
    f"{UMBRAL_ANGULO_DEG}°",
)


# ---------------------------------------------------------------- Achievements
st.divider()
st.subheader("Logros de ergonomía")

logros = analytics.achievements(df)
cols = st.columns(3)
for i, logro in enumerate(logros):
    with cols[i % 3]:
        marca = "🏆" if logro["desbloqueado"] else "🔒"
        color = LASALLE_DORADO if logro["desbloqueado"] else "#999"
        st.markdown(
            f"""
            <div style="
                border: 2px solid {color};
                border-radius: 10px;
                padding: 14px;
                margin-bottom: 10px;
                opacity: {'1' if logro['desbloqueado'] else '0.55'};
            ">
              <div style="font-size: 22px;">{marca} <b>{logro['titulo']}</b></div>
              <div style="font-size: 13px; color: #555; margin: 6px 0 8px 0;">
                  {logro['descripcion']}
              </div>
              <div style="
                  background: #eee; border-radius: 6px; height: 8px; overflow: hidden;
              ">
                <div style="
                    width: {logro['progreso']*100:.0f}%;
                    background: {color}; height: 100%;
                "></div>
              </div>
              <div style="font-size: 11px; color: #888; margin-top: 4px;">
                  Progreso: {logro['progreso']*100:.0f}%
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------- Sesiones doradas
st.divider()
st.subheader("Sesiones doradas")
st.caption(
    "Períodos largos de postura correcta. Cada barra representa una sesión continua "
    "con ángulo por debajo del umbral."
)

doradas = analytics.sesiones_doradas(df, duracion_min_s=30)
if doradas.empty:
    st.info(
        "Todavía no hay sesiones doradas de 30 s o más. Concéntrate en mantener "
        "la espalda recta de forma sostenida para empezar a desbloquear logros."
    )
else:
    top = doradas.head(15).copy()
    top["min"] = top["duracion_s"] / 60
    top["etiqueta"] = top["inicio"].dt.strftime("%Y-%m-%d %H:%M")
    fig = px.bar(
        top.iloc[::-1],
        x="min", y="etiqueta", orientation="h",
        color="angulo_medio",
        color_continuous_scale=[[0, LASALLE_AZUL_PRIMARIO], [1, LASALLE_DORADO]],
        labels={"min": "Duración (min)", "etiqueta": "Inicio", "angulo_medio": "Ángulo medio (°)"},
        hover_data={"duracion_s": ":.0f", "n_muestras": True, "min": ":.1f"},
    )
    fig.update_layout(
        height=max(280, 32 * len(top) + 80),
        margin=dict(l=0, r=0, t=10, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------- Tendencia diaria
st.divider()
st.subheader("Tendencia diaria de buena postura")
pct_dia = analytics.pct_buena_por_dia(df)
if pct_dia.empty:
    st.info("Sin datos diarios suficientes.")
else:
    pct_dia["dia"] = pd.to_datetime(pct_dia["dia"])
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=pct_dia["dia"], y=pct_dia["pct_buena"],
            marker_color=[
                LASALLE_AZUL_PRIMARIO if v >= 90 else LASALLE_AZUL_MEDIO if v >= 75 else
                LASALLE_DORADO if v >= 50 else COLOR_MALA
                for v in pct_dia["pct_buena"]
            ],
            text=[f"{v:.0f}%" for v in pct_dia["pct_buena"]],
            textposition="outside",
        )
    )
    fig.add_hline(
        y=75, line_dash="dot", line_color="#888",
        annotation_text="Objetivo: 75%", annotation_position="right",
    )
    fig.update_layout(
        height=320, margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Día",
        yaxis_title="% buena postura",
        yaxis_range=[0, 110],
    )
    st.plotly_chart(fig, use_container_width=True)


# ---------------------------------------------------------------- Tips
st.divider()
st.subheader("Tips para mantener una buena postura")
st.markdown(
    """
    - **Apoya la zona lumbar** contra el respaldo; usa un cojín si es necesario.
    - **Pies planos en el suelo** o sobre un reposapiés; rodillas a 90°.
    - **Pantalla a la altura de los ojos**, a ~50–70 cm de distancia.
    - **Codos a 90°** al teclear; muñecas neutras.
    - **Pausas activas cada 30–45 minutos**: levántate, estira, mira lejos por 20 s.
    - **Hidrátate**: te obliga a levantarte y romper la inercia de la silla.
    """
)
