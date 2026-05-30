"""Configuración del dashboard ErgIoT.

Las credenciales de InfluxDB se leen de variables de entorno o de un
archivo `.env` colocado al lado de este módulo. **Nunca** se hardcodean
en el código fuente para no exponerlas en GitHub.

Si falta cualquier variable, la app falla rápido con un mensaje claro.
"""
from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv() -> None:
    """Carga variables de un .env adyacente al archivo, sin requerir python-dotenv."""
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv()


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Falta la variable de entorno {name}. "
            f"Define INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG e INFLUX_BUCKET "
            f"en un archivo .env (ver .env.example) o como variables de entorno."
        )
    return value


# ---- Credenciales InfluxDB Cloud (cargadas desde entorno) ----
INFLUX_URL    = _require("INFLUX_URL")
INFLUX_TOKEN  = _require("INFLUX_TOKEN")
INFLUX_ORG    = _require("INFLUX_ORG")
INFLUX_BUCKET = _require("INFLUX_BUCKET")
MEASUREMENT   = os.environ.get("INFLUX_MEASUREMENT", "telemetria_ergonomica")


# ---- Umbrales del sistema ergonómico ----
UMBRAL_ANGULO_DEG       = float(os.environ.get("UMBRAL_ANGULO_DEG", 30.0))
UMBRAL_PRESION_OCUPADO  = int(os.environ.get("UMBRAL_PRESION_OCUPADO", 100))
ALERTA_DURACION_S       = float(os.environ.get("ALERTA_DURACION_S", 10))


# ---- Paleta institucional Universidad de La Salle (Bogotá) ----
# Extraída de https://lasalle.edu.co/es
LASALLE_AZUL_PRIMARIO   = "#003057"
LASALLE_AZUL_OSCURO     = "#033259"
LASALLE_AZUL_MEDIO      = "#02416c"
LASALLE_AZUL_CLARO      = "#a2c9fd"
LASALLE_DORADO          = "#f2a900"
LASALLE_DORADO_OSCURO   = "#d4a017"
LASALLE_TEXTO           = "#001e38"
LASALLE_FONDO           = "#ffffff"
LASALLE_FONDO_GRIS      = "#f5f7fa"

# ---- Semáforo derivado de la identidad institucional ----
COLOR_EXCELENTE = LASALLE_AZUL_PRIMARIO
COLOR_BUENA     = LASALLE_AZUL_MEDIO
COLOR_LIMITE    = LASALLE_DORADO
COLOR_MALA      = "#C73E1D"
COLOR_AUSENTE   = "#888888"

# Escala secuencial para mapas de calor (azul → dorado → rojo)
ESCALA_RIESGO = [
    [0.0, LASALLE_AZUL_PRIMARIO],
    [0.5, LASALLE_DORADO],
    [1.0, COLOR_MALA],
]
