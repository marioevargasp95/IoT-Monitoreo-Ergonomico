"""Carga datos del bucket InfluxDB y los pivota a un DataFrame ancho."""
from __future__ import annotations

import pandas as pd
from influxdb_client import InfluxDBClient

from config import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET,
    MEASUREMENT,
)


def fetch_dataframe(rango: str = "-7d") -> pd.DataFrame:
    """Consulta InfluxDB y devuelve un DataFrame con columnas por field.

    Returns columnas: time, angulo_grados, presion_adc, ocupado,
    clasificacion_riesgo, indice_riesgo, tiempo_sentado, alerta_pausa
    """
    flux = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: {rango})
      |> filter(fn: (r) => r._measurement == "{MEASUREMENT}")
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> sort(columns: ["_time"])
    '''

    with InfluxDBClient(
        url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG, timeout=60_000
    ) as client:
        df = client.query_api().query_data_frame(flux)

    if isinstance(df, list):
        df = pd.concat(df, ignore_index=True) if df else pd.DataFrame()

    if df.empty:
        return df

    df = df.rename(columns={"_time": "time"})
    keep = [
        "time",
        "angulo_grados",
        "presion_adc",
        "ocupado",
        "clasificacion_riesgo",
        "indice_riesgo",
        "tiempo_sentado",
        "alerta_pausa",
    ]
    present = [c for c in keep if c in df.columns]
    df = df[present].copy()
    df["time"] = pd.to_datetime(df["time"]).dt.tz_convert("America/Bogota")
    df = df.sort_values("time").reset_index(drop=True)
    return df
