"""Módulo de registro (logs) del sistema Software FJ."""

import logging  # Librería estándar de Python para registrar mensajes
import os       # Permite crear carpetas del sistema

# Crea la carpeta "logs" si no existe (exist_ok evita error si ya existe)
os.makedirs("logs", exist_ok=True)

# Configura el archivo donde se guardarán todos los mensajes
logging.basicConfig(
    filename="logs/software_fj.log",                  # Ruta del archivo de logs
    level=logging.INFO,                               # Registra desde nivel INFO hacia arriba
    format="%(asctime)s | %(levelname)s | %(message)s",  # Fecha | nivel | mensaje
    encoding="utf-8",                                 # Permite tildes y ñ
)

# Objeto logger propio del sistema
log = logging.getLogger("software_fj")


def registrar_evento(mensaje):
    """Registra un evento normal (operación exitosa)."""
    log.info(mensaje)


def registrar_error(mensaje):
    """Registra un error controlado."""
    log.error(mensaje)
