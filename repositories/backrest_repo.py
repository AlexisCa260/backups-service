from datetime import datetime

import pytz
from sqlalchemy import text

from config import SSH_USER
from db import get_engine

zona_colombia = pytz.timezone("America/Bogota")


def guardar_backrest(host: str, ip: str, marca: str, configuracion: str):
    engine = get_engine()
    fecha = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S")

    query = text("""
        INSERT INTO backrest (date, backrestnew, tipo, usuario, ip, nombre, marca, modelo)
        VALUES (:date, :conf, :tipo, :usuario, :ip, :nombre, :marca, :modelo)
    """)

    data = {
        "date": fecha,
        "conf": configuracion,
        "tipo": "Automatica",
        "usuario": SSH_USER,
        "ip": ip,
        "nombre": host,
        "marca": marca,
        "modelo": "Desconocido",
    }

    with engine.begin() as conn:
        conn.execute(query, data)
