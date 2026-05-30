"""Imprime KPIs actualizados para usar en el guion del video."""
from data_loader import fetch_dataframe
import analytics

df = fetch_dataframe("-30d")
k = analytics.kpis(df)
kp = analytics.kpis_pausa(df)
tpf = analytics.tiempo_por_flag(df)

print("==KPIs principales==")
print(f"n_puntos: {k['n_puntos']}")
print(f"rango: {k['rango_inicio']} -> {k['rango_fin']}")
print(f"angulo_medio: {k['angulo_medio']:.1f}")
print(f"angulo_p95: {k['angulo_p95']:.1f}")
print(f"angulo_max: {k['angulo_max']:.1f}")
print(f"pct_postura_correcta: {k['pct_postura_correcta']:.1f}%")
print(f"pct_ocupacion: {k['pct_ocupacion']:.1f}%")

print("\n==Tiempo por flag==")
print(tpf.to_string())

print("\n==Pausa activa==")
print(f"umbral firmware: {kp['umbral_alerta_min']} min")
print(f"eventos alerta: {kp['n_eventos_alerta']}")
print(f"pct_alerta: {kp['pct_tiempo_en_alerta']:.1f}%")
print(f"max_sin_pausa: {kp['tiempo_sentado_max']} min")

ev = analytics.detectar_eventos_mala_postura(df)
print("\n==Eventos mala postura==")
print(f"cantidad: {len(ev)}")
if not ev.empty:
    print(f"tiempo total en mala postura (min): {ev['duracion_s'].sum()/60:.1f}")
    print(f"evento mas largo (s): {ev['duracion_s'].max()}")

sd = analytics.sesiones_doradas(df, 30)
mr = analytics.mejor_racha(df)
print("\n==Sesiones doradas==")
print(f"sesiones (>=30s): {len(sd)}")
print(f"mejor racha (min): {mr['duracion_s']/60:.1f}")

cm = analytics.matriz_correlacion(df)
print("\n==Correlacion==")
print(cm.round(2))

pct = analytics.pct_buena_por_dia(df)
print("\n==% buena postura por dia==")
print(pct.to_string())
