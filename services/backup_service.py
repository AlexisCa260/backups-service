from config import DB_ENGINE
from repositories.backrest_repo import guardar_backrest
from repositories.zabbix_repo import get_zabbix_hosts
from services.ssh_service import obtener_configuracion_ssh


def crear_backups_todos():
    hosts = get_zabbix_hosts()
    resultados = []

    if not hosts:
        return {
            "mensaje": f"No se encontraron hosts en {DB_ENGINE} con tag backups=SI."
        }

    for h in hosts:
        conf = obtener_configuracion_ssh(h["ip"])
        guardar_backrest(h["host"], h["ip"], h.get("marca", "Desconocida"), conf)
        resultados.append(
            {
                "host": h["host"],
                "ip": h["ip"],
                "marca": h.get("marca", "Desconocida"),
                "configuracion": conf,
            }
        )

    return {
        "motor": DB_ENGINE,
        "total_hosts": len(resultados),
        "resultados": resultados,
    }
