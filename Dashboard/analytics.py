"""Análisis básico: KPIs, eventos de mala postura, correlaciones."""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import UMBRAL_ANGULO_DEG, ALERTA_DURACION_S


def kpis(df: pd.DataFrame) -> dict:
    """Indicadores clave para los tiles superiores del dashboard."""
    if df.empty:
        return {}

    ocupado = df[df.get("ocupado", pd.Series(dtype=float)).fillna(0) > 0]
    base = ocupado if not ocupado.empty else df

    angulo = base["angulo_grados"].dropna()
    presion = base["presion_adc"].dropna()

    pct_correcta = float((angulo <= UMBRAL_ANGULO_DEG).mean() * 100) if not angulo.empty else float("nan")
    pct_ocupacion = float((df["ocupado"].fillna(0) > 0).mean() * 100) if "ocupado" in df else float("nan")

    return {
        "n_puntos": int(len(df)),
        "rango_inicio": df["time"].min(),
        "rango_fin": df["time"].max(),
        "angulo_medio": float(angulo.mean()) if not angulo.empty else float("nan"),
        "angulo_p95": float(angulo.quantile(0.95)) if not angulo.empty else float("nan"),
        "angulo_max": float(angulo.max()) if not angulo.empty else float("nan"),
        "presion_media": float(presion.mean()) if not presion.empty else float("nan"),
        "pct_postura_correcta": pct_correcta,
        "pct_ocupacion": pct_ocupacion,
        "indice_riesgo_medio": (
            float(base["indice_riesgo"].mean())
            if "indice_riesgo" in base and base["indice_riesgo"].notna().any()
            else float("nan")
        ),
    }


def detectar_eventos_mala_postura(
    df: pd.DataFrame,
    umbral_grados: float = UMBRAL_ANGULO_DEG,
    duracion_min_s: float = ALERTA_DURACION_S,
) -> pd.DataFrame:
    """Agrupa muestras consecutivas con ángulo > umbral en eventos.

    Solo cuenta el evento si dura más de `duracion_min_s` segundos
    y el usuario está presente (ocupado > 0 cuando exista la columna).
    """
    if df.empty or "angulo_grados" not in df:
        return pd.DataFrame(
            columns=["inicio", "fin", "duracion_s", "angulo_max", "angulo_medio"]
        )

    base = df.copy()
    if "ocupado" in base:
        base = base[base["ocupado"].fillna(0) > 0]

    base = base.sort_values("time").reset_index(drop=True)
    mala = base["angulo_grados"] > umbral_grados
    grupo = (mala != mala.shift()).cumsum()

    eventos = []
    for _, sub in base[mala].groupby(grupo):
        if len(sub) < 2:
            continue
        dur = (sub["time"].iloc[-1] - sub["time"].iloc[0]).total_seconds()
        if dur < duracion_min_s:
            continue
        eventos.append(
            {
                "inicio": sub["time"].iloc[0],
                "fin": sub["time"].iloc[-1],
                "duracion_s": dur,
                "angulo_max": float(sub["angulo_grados"].max()),
                "angulo_medio": float(sub["angulo_grados"].mean()),
            }
        )

    return pd.DataFrame(eventos)


def matriz_correlacion(df: pd.DataFrame) -> pd.DataFrame:
    """Correlación entre ángulo, presión, índice de riesgo, tiempo sentado."""
    cols = [c for c in ["angulo_grados", "presion_adc", "indice_riesgo", "tiempo_sentado"] if c in df]
    if len(cols) < 2:
        return pd.DataFrame()
    return df[cols].corr(numeric_only=True)


def heatmap_horario(df: pd.DataFrame) -> pd.DataFrame:
    """Promedio de ángulo por hora del día y día de la semana."""
    if df.empty or "angulo_grados" not in df:
        return pd.DataFrame()
    base = df.copy()
    base["hora"] = base["time"].dt.hour
    base["dia"] = base["time"].dt.day_name()
    pivot = base.pivot_table(
        index="dia", columns="hora", values="angulo_grados", aggfunc="mean"
    )
    orden = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in orden if d in pivot.index])
    return pivot


def distribucion_riesgo(df: pd.DataFrame) -> pd.Series:
    """Conteo de cada clasificación de riesgo."""
    if "clasificacion_riesgo" not in df:
        return pd.Series(dtype=int)
    return df["clasificacion_riesgo"].dropna().astype(str).value_counts()


# ============================ Buena postura ============================

def _segmentos_buena_postura(
    df: pd.DataFrame, umbral_grados: float = UMBRAL_ANGULO_DEG
) -> pd.DataFrame:
    """Devuelve segmentos consecutivos con ángulo ≤ umbral mientras hay ocupación.

    Columnas: inicio, fin, duracion_s, angulo_medio, n_muestras
    """
    if df.empty or "angulo_grados" not in df:
        return pd.DataFrame(
            columns=["inicio", "fin", "duracion_s", "angulo_medio", "n_muestras"]
        )

    base = df.copy()
    if "ocupado" in base:
        base = base[base["ocupado"].fillna(0) > 0]
    base = base.sort_values("time").reset_index(drop=True)

    buena = base["angulo_grados"] <= umbral_grados
    grupo = (buena != buena.shift()).cumsum()

    segs = []
    for _, sub in base[buena].groupby(grupo):
        if len(sub) < 2:
            continue
        dur = (sub["time"].iloc[-1] - sub["time"].iloc[0]).total_seconds()
        segs.append(
            {
                "inicio": sub["time"].iloc[0],
                "fin": sub["time"].iloc[-1],
                "duracion_s": dur,
                "angulo_medio": float(sub["angulo_grados"].mean()),
                "n_muestras": len(sub),
            }
        )
    return pd.DataFrame(segs).sort_values("duracion_s", ascending=False).reset_index(drop=True)


def estado_actual(df: pd.DataFrame, umbral_grados: float = UMBRAL_ANGULO_DEG) -> dict:
    """Estado del último registro disponible: flag, ángulo, presencia."""
    if df.empty:
        return {"flag": "SIN_DATOS"}
    ult = df.iloc[-1]
    angulo = float(ult.get("angulo_grados", float("nan")))
    ocupado = int(ult.get("ocupado", 0)) if not pd.isna(ult.get("ocupado", 0)) else 0
    clasif = str(ult.get("clasificacion_riesgo", ""))
    ts = ult["time"]

    if ocupado == 0:
        flag = "AUSENTE"
    elif angulo <= umbral_grados * 0.7:
        flag = "EXCELENTE"
    elif angulo <= umbral_grados:
        flag = "BUENA"
    elif angulo <= umbral_grados * 1.2:
        flag = "LIMITE"
    else:
        flag = "MALA"

    return {
        "flag": flag,
        "angulo": angulo,
        "ocupado": ocupado,
        "clasificacion": clasif,
        "timestamp": ts,
    }


def racha_actual(df: pd.DataFrame, umbral_grados: float = UMBRAL_ANGULO_DEG) -> dict:
    """Racha actual de buena postura desde el final hacia atrás.

    Cuenta muestras consecutivas con ángulo ≤ umbral al final de la serie.
    """
    if df.empty or "angulo_grados" not in df:
        return {"duracion_s": 0, "n_muestras": 0, "inicio": None}

    base = df.copy()
    if "ocupado" in base:
        base = base[base["ocupado"].fillna(0) > 0]
    base = base.sort_values("time").reset_index(drop=True)

    buena = base["angulo_grados"] <= umbral_grados
    # encuentra hasta dónde se mantiene True desde el final
    n = 0
    for v in buena.values[::-1]:
        if v:
            n += 1
        else:
            break
    if n == 0:
        return {"duracion_s": 0, "n_muestras": 0, "inicio": None}

    inicio = base["time"].iloc[-n]
    fin = base["time"].iloc[-1]
    return {
        "duracion_s": (fin - inicio).total_seconds(),
        "n_muestras": n,
        "inicio": inicio,
        "fin": fin,
    }


def mejor_racha(
    df: pd.DataFrame, umbral_grados: float = UMBRAL_ANGULO_DEG
) -> dict:
    """La sesión dorada más larga registrada en la ventana."""
    segs = _segmentos_buena_postura(df, umbral_grados)
    if segs.empty:
        return {"duracion_s": 0, "inicio": None, "fin": None, "angulo_medio": float("nan")}
    top = segs.iloc[0]
    return {
        "duracion_s": float(top["duracion_s"]),
        "inicio": top["inicio"],
        "fin": top["fin"],
        "angulo_medio": float(top["angulo_medio"]),
    }


def sesiones_doradas(
    df: pd.DataFrame,
    duracion_min_s: float = 60,
    umbral_grados: float = UMBRAL_ANGULO_DEG,
) -> pd.DataFrame:
    """Segmentos de buena postura más largos que `duracion_min_s` segundos."""
    segs = _segmentos_buena_postura(df, umbral_grados)
    if segs.empty:
        return segs
    return segs[segs["duracion_s"] >= duracion_min_s].reset_index(drop=True)


def pct_buena_por_dia(
    df: pd.DataFrame, umbral_grados: float = UMBRAL_ANGULO_DEG
) -> pd.DataFrame:
    """% de muestras con buena postura por día (solo cuando hay ocupación)."""
    if df.empty or "angulo_grados" not in df:
        return pd.DataFrame(columns=["dia", "pct_buena", "n"])
    base = df.copy()
    if "ocupado" in base:
        base = base[base["ocupado"].fillna(0) > 0]
    base["dia"] = base["time"].dt.date
    agg = base.groupby("dia").agg(
        n=("angulo_grados", "size"),
        buenas=("angulo_grados", lambda s: int((s <= umbral_grados).sum())),
    )
    agg["pct_buena"] = (agg["buenas"] / agg["n"] * 100).round(1)
    return agg.reset_index()[["dia", "pct_buena", "n"]]


def asignar_flag(angulo: float, ocupado: int | float | None,
                 umbral: float = UMBRAL_ANGULO_DEG) -> str:
    """Categoriza una muestra individual en EXCELENTE/BUENA/LIMITE/MALA/AUSENTE."""
    if ocupado is None or (isinstance(ocupado, float) and pd.isna(ocupado)) or int(ocupado) == 0:
        return "AUSENTE"
    if pd.isna(angulo):
        return "AUSENTE"
    if angulo <= umbral * 0.7:
        return "EXCELENTE"
    if angulo <= umbral:
        return "BUENA"
    if angulo <= umbral * 1.2:
        return "LIMITE"
    return "MALA"


def df_con_flags(df: pd.DataFrame, umbral: float = UMBRAL_ANGULO_DEG) -> pd.DataFrame:
    """Devuelve el DataFrame con una columna `flag` añadida por muestra."""
    if df.empty:
        return df.assign(flag=[])
    out = df.copy()
    out["flag"] = [
        asignar_flag(a, o, umbral)
        for a, o in zip(out.get("angulo_grados", []), out.get("ocupado", [0]*len(out)))
    ]
    return out


def tiempo_por_flag(df: pd.DataFrame, umbral: float = UMBRAL_ANGULO_DEG) -> pd.DataFrame:
    """Tiempo acumulado en cada flag.

    Calculado como el delta temporal entre muestras consecutivas asignado
    al flag de la muestra inicial del intervalo.
    """
    if df.empty or "angulo_grados" not in df:
        return pd.DataFrame(columns=["flag", "segundos", "minutos"])
    base = df_con_flags(df, umbral).sort_values("time").reset_index(drop=True)
    if len(base) < 2:
        return pd.DataFrame(columns=["flag", "segundos", "minutos"])
    deltas = base["time"].diff().shift(-1).dt.total_seconds()
    # rellenar la última muestra con la mediana del delta para no perderla
    if not deltas.dropna().empty:
        deltas = deltas.fillna(deltas.median())
    base["delta_s"] = deltas
    agg = base.groupby("flag", as_index=False)["delta_s"].sum()
    agg = agg.rename(columns={"delta_s": "segundos"})
    agg["minutos"] = (agg["segundos"] / 60).round(2)
    orden = ["EXCELENTE", "BUENA", "LIMITE", "MALA", "AUSENTE"]
    agg["flag"] = pd.Categorical(agg["flag"], categories=orden, ordered=True)
    return agg.sort_values("flag").reset_index(drop=True)


def kpis_pausa(df: pd.DataFrame) -> dict:
    """Indicadores sobre tiempo sentado y alertas de pausa activa."""
    if df.empty or "tiempo_sentado" not in df:
        return {}

    ts = df["tiempo_sentado"].dropna()
    ap = df.get("alerta_pausa", pd.Series(dtype=int)).fillna(0).astype(int)

    # Umbral implícito del firmware: el primer instante con alerta=1
    alertas = df[df["alerta_pausa"] == 1] if "alerta_pausa" in df else pd.DataFrame()
    umbral_alerta = (
        float(alertas["tiempo_sentado"].min()) if not alertas.empty else float("nan")
    )

    # Sesiones de tiempo sentado: cada vez que tiempo_sentado se resetea a un valor menor
    # consideramos que empezó una nueva sesión.
    sesiones = []
    if not ts.empty:
        base = df.dropna(subset=["tiempo_sentado"]).copy()
        base["reset"] = base["tiempo_sentado"].diff().fillna(0) < 0
        base["sesion"] = base["reset"].cumsum()
        for _, sub in base.groupby("sesion"):
            sesiones.append(
                {
                    "inicio": sub["time"].iloc[0],
                    "fin": sub["time"].iloc[-1],
                    "duracion_min": float(sub["tiempo_sentado"].max()),
                }
            )

    n_eventos_alerta = int((ap.diff().fillna(ap.iloc[0]) == 1).sum()) if not ap.empty else 0

    return {
        "tiempo_sentado_actual": float(df["tiempo_sentado"].iloc[-1]) if not ts.empty else 0.0,
        "tiempo_sentado_max": float(ts.max()) if not ts.empty else 0.0,
        "tiempo_sentado_medio": float(ts.mean()) if not ts.empty else 0.0,
        "umbral_alerta_min": umbral_alerta,
        "n_eventos_alerta": n_eventos_alerta,
        "n_muestras_en_alerta": int(ap.sum()) if not ap.empty else 0,
        "pct_tiempo_en_alerta": float(ap.mean() * 100) if not ap.empty else 0.0,
        "sesiones_largas": [s for s in sesiones if s["duracion_min"] >= 30],
        "total_sesiones": len(sesiones),
    }


def eventos_alerta_pausa(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa muestras consecutivas con alerta_pausa=1 en eventos.

    Columnas: inicio, fin, duracion_s, tiempo_sentado_max
    """
    if df.empty or "alerta_pausa" not in df:
        return pd.DataFrame(
            columns=["inicio", "fin", "duracion_s", "tiempo_sentado_max"]
        )
    base = df.sort_values("time").reset_index(drop=True)
    en_alerta = base["alerta_pausa"].fillna(0).astype(int) == 1
    grupo = (en_alerta != en_alerta.shift()).cumsum()
    eventos = []
    for _, sub in base[en_alerta].groupby(grupo):
        if len(sub) < 1:
            continue
        dur = (sub["time"].iloc[-1] - sub["time"].iloc[0]).total_seconds()
        eventos.append(
            {
                "inicio": sub["time"].iloc[0],
                "fin": sub["time"].iloc[-1],
                "duracion_s": dur,
                "tiempo_sentado_max": float(sub["tiempo_sentado"].max())
                if "tiempo_sentado" in sub else float("nan"),
                "n_muestras": len(sub),
            }
        )
    return pd.DataFrame(eventos).reset_index(drop=True)


def achievements(
    df: pd.DataFrame, umbral_grados: float = UMBRAL_ANGULO_DEG
) -> list[dict]:
    """Lista de logros desbloqueados según el historial.

    Cada logro: {'id', 'titulo', 'descripcion', 'desbloqueado'}.
    """
    segs = _segmentos_buena_postura(df, umbral_grados)
    pct_dia = pct_buena_por_dia(df, umbral_grados)
    racha_max_s = float(segs["duracion_s"].max()) if not segs.empty else 0.0
    dias_perfectos = int((pct_dia["pct_buena"] >= 90).sum()) if not pct_dia.empty else 0
    dias_buenos = int((pct_dia["pct_buena"] >= 75).sum()) if not pct_dia.empty else 0
    total_buena_min = float(segs["duracion_s"].sum() / 60) if not segs.empty else 0.0

    return [
        {
            "id": "racha_5",
            "titulo": "Calienta motores",
            "descripcion": "Mantén buena postura durante 5 minutos seguidos.",
            "desbloqueado": racha_max_s >= 5 * 60,
            "progreso": min(1.0, racha_max_s / (5 * 60)),
        },
        {
            "id": "racha_15",
            "titulo": "Concentrado",
            "descripcion": "15 minutos consecutivos con la espalda recta.",
            "desbloqueado": racha_max_s >= 15 * 60,
            "progreso": min(1.0, racha_max_s / (15 * 60)),
        },
        {
            "id": "racha_30",
            "titulo": "Maratón ergonómico",
            "descripcion": "Media hora seguida en postura correcta.",
            "desbloqueado": racha_max_s >= 30 * 60,
            "progreso": min(1.0, racha_max_s / (30 * 60)),
        },
        {
            "id": "dia_perfecto",
            "titulo": "Día perfecto",
            "descripcion": "≥ 90% del día en buena postura.",
            "desbloqueado": dias_perfectos >= 1,
            "progreso": float(min(1.0, dias_perfectos)),
        },
        {
            "id": "habito",
            "titulo": "Hábito formado",
            "descripcion": "3 días seguidos con ≥ 75% de buena postura.",
            "desbloqueado": dias_buenos >= 3,
            "progreso": min(1.0, dias_buenos / 3),
        },
        {
            "id": "60_min_total",
            "titulo": "Una hora bien sentado",
            "descripcion": "Acumula 60 minutos de buena postura en la ventana.",
            "desbloqueado": total_buena_min >= 60,
            "progreso": min(1.0, total_buena_min / 60),
        },
    ]
