from typing import Any, Dict

from fastapi import Depends, FastAPI
from sqlalchemy import text

from db import get_engine
from repositories.backrest_repo import guardar_backrest
from security import get_current_user
from services.backup_service import crear_backups_todos
from services.ssh_service import obtener_configuracion_ssh

app = FastAPI()


@app.get("/backups/create/all")
def crear_backups(current_user: dict = Depends(get_current_user)) -> Dict[str, Any]:
    return crear_backups_todos()


@app.get("/backups/create/{nombre}")
def crear_backup(nombre: str, current_user: dict = Depends(get_current_user)):
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
