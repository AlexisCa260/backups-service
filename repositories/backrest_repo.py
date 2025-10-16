from datetime import datetime

from sqlalchemy import text

from config import SSH_USER
from db import get_engine


def guardar_backrest(host: str, ip: str, marca: str, configuracion: str):
    engine = get_engine()
    fecha = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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
