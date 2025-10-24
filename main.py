import threading
import time
from typing import Any, Dict

import schedule
from fastapi import Depends, FastAPI
from sqlalchemy import text

from db import get_engine
from repositories.backrest_repo import guardar_backrest
from security import get_current_user
from services.backup_service import crear_backups_todos
from services.ssh_service import obtener_configuracion_ssh

app = FastAPI()


# ====================== ENDPOINTS ======================


@app.get("/backups/create/all")
def crear_backups(current_user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    """Ejecuta manualmente la creación de backups para todos."""
    return crear_backups_todos()


@app.get("/backups/create/{nombre}")
def crear_backup(nombre: str, current_user: dict = Depends(get_current_user)):
    """Ejecuta manualmente la creación de backup para un solo equipo."""
    engine = get_engine()
    query_select = text("""
        SELECT id, date, backrestnew, tipo, usuario, ip, nombre, marca, modelo
        FROM backrest
        WHERE nombre = :nombre
        ORDER BY date DESC
        LIMIT 1
    """)

    with engine.connect() as conn:
        result = conn.execute(query_select, {"nombre": nombre}).mappings().first()

    if not result:
        return {
            "error": f"No se encontró un registro con nombre '{nombre}' en la tabla backrest."
        }

    ip = result["ip"]
    marca = result["marca"]
    configuracion = obtener_configuracion_ssh(ip)
    guardar_backrest(nombre, ip, marca, configuracion)

    return {
        "mensaje": f"Backup creado correctamente para '{nombre}'.",
        "ip": ip,
        "marca": marca,
        "nueva_configuracion": configuracion[:500] + "..."
        if len(configuracion) > 500
        else configuracion,
        "ultimo_registro": dict(result),
    }


# ====================== TAREA PROGRAMADA ======================


def tarea_programada_backups():
    """Envuelve la tarea para imprimir cuándo inicia y cuándo termina."""
    print("🔹 [CRON] Iniciando tarea automática de backups...")
    try:
        crear_backups_todos()
        print("✅ [CRON] Tarea de backups completada correctamente.")
    except Exception as e:
        print(f"❌ [CRON] Error al ejecutar la tarea de backups: {e}")


def run_scheduler():
    """Ejecuta el planificador de tareas en segundo plano."""
    while True:
        schedule.run_pending()
        time.sleep(1)


def configurar_cron_backup(hora: str = "02:00"):
    """
    Configura el cron para ejecutar crear_backups_todos() todos los días a una hora específica.
    Ejemplo: "02:00" = 2:00 AM
    """
    schedule.every().day.at(hora).do(tarea_programada_backups)
    thread = threading.Thread(target=run_scheduler, daemon=True)
    thread.start()


# ====================== INICIO DE LA APP ======================


@app.on_event("startup")
def startup_event():
    configurar_cron_backup("23:59")  # Cambia la hora aquí (formato HH:MM, 24h)
    print("⏰ Tarea programada: backups automáticos diarios a las 17:25")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8094, reload=True)
