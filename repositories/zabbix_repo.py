from sqlalchemy import text

from db import get_engine


def get_zabbix_hosts():
    engine = get_engine()
    query = text("""
        SELECT 
            h.hostid,
            h.name AS host,
            i.ip,
            m.value AS marca
        FROM hosts h
        JOIN interface i ON i.hostid = h.hostid
        JOIN host_tag b ON b.hostid = h.hostid
        LEFT JOIN host_tag m ON m.hostid = h.hostid AND m.tag = 'Marca'
        WHERE h.status = 0 AND b.tag = 'backups' AND b.value = 'SI';
    """)

    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
        return [dict(row) for row in rows]
