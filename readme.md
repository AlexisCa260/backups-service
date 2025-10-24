# 🛎️ Backup Service API

API ligera desarrollada en **FastAPI** para ejecutar **backups automáticos y manuales** de configuraciones de equipos de red.  
Obtiene la lista de equipos desde **Zabbix**, se conecta por **SSH** para leer la configuración y almacena los resultados en la tabla `backrest`.

---

## 📁 Estructura del proyecto

- **main.py** — Configuración general de la API y del scheduler.  
- **services/**
  - `backup_service.py` — Lógica principal para creación de backups (`crear_backups_todos`).
  - `ssh_service.py` — Conexión SSH y obtención de configuraciones.
- **repositories/**
  - `zabbix_repo.py` — Consulta de hosts en Zabbix (`get_zabbix_hosts`).
  - `backrest_repo.py` — Inserción de backups en base de datos (`guardar_backrest`).
- **config.py** — Variables de entorno y configuración general.
- **db.py** — Creación del engine SQLAlchemy.
- **security.py** — Autenticación JWT (`get_current_user`).

---

## 🔐 Autenticación

Todos los endpoints requieren autenticación **JWT** mediante la dependencia `security.get_current_user`.

Puedes enviar el token de dos maneras:
- En el **header**:  
  `Authorization: Bearer <TOKEN>`
- O como parámetro en la URL:  
  `?token=<TOKEN>`

El token se valida usando `SECRET_KEY` y `JWT_ALGORITHM` definidos en `config.py`.

---

## ⚙️ Variables de entorno

Define las siguientes variables en un archivo `.env`:

| Variable | Descripción |
|-----------|--------------|
| `DB_ENGINE` | Motor de base de datos (`MYSQL` o `POSTGRES`) |
| `DB_URL_MYSQL` / `DB_URL_POSTGRES` | URL de conexión |
| `SSH_USER`, `SSH_PASS`, `SSH_TIMEOUT` | Credenciales SSH |
| `SECRET_KEY`, `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES` | Configuración de JWT |

Consulta `config.py` para ver cómo se cargan.

---

## 🚀 Endpoints principales

### 1. Crear backups para todos los equipos
- **Método:** `GET`  
- **Ruta:** `/backups/create/all`  
- **Autenticación:** requerida  
- **Acción:** ejecuta `crear_backups_todos` y devuelve un resumen con motor, total de hosts y resultados.  

### 2. Crear backup para un equipo específico
- **Método:** `GET`  
- **Ruta:** `/backups/create/{nombre}`  
- **Parámetros:** `nombre` (path)  
- **Autenticación:** requerida  
- **Acción:** obtiene la IP del último registro, ejecuta el backup SSH y guarda la nueva configuración.  
- **Respuesta:** incluye `mensaje`, `ip`, `marca`, `nueva_configuracion` (preview) y `último_registro`.

---

## ⏰ Scheduler / Cron integrado

Al iniciar la API, se configura un job automático con `configurar_cron_backup()` (ver `main.py`).

- Hora por defecto: **23:59**  
- Acción programada: ejecutar `crear_backups_todos`  
- Se registran logs de inicio y fin de la tarea

Puedes ajustar la hora fácilmente modificando el valor en `main.py`.

---

## 🗄 Base de datos

- Conexión generada por `db.get_engine()` según la URL definida en `.env`.  
- Los backups se almacenan en la tabla `backrest`.  
- Verifica que las tablas y permisos existan en tu motor (`MySQL` o `PostgreSQL`).

---

## 🧪 Instalación y uso local

1. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar `.env` con credenciales de BD y SSH.
4. Iniciar servidor:
   ```bash
   uvicorn main:app --reload --port 8094
   ```

---

## 🐳 Docker

Archivo `Dockerfile` incluido.  
Construir y ejecutar:

```bash
docker build -t backup-service .
docker run -e $(cat .env | xargs) -p 8094:8094 backup-service
```

---

## 🧩 Problemas comunes

| Problema | Posible causa / solución |
|-----------|--------------------------|
| Timeout SSH | Aumenta `SSH_TIMEOUT` en `.env`. |
| Error de algoritmos SSH | `ssh_service.py` prueba diferentes `disabled_algorithms`. |
| Cambios no visibles en BD | Verifica commits y transacciones en `backrest_repo.py`. |

---

## 📘 Referencias útiles

- `main.crear_backups`
- `services.backup_service.crear_backups_todos`
- `services.ssh_service.obtener_configuracion_ssh`
- `repositories.backrest_repo.guardar_backrest`
- `repositories.zabbix_repo.get_zabbix_hosts`

---

## 📚 Documentación automática

Disponible al ejecutar el servicio:
- **Swagger UI:** [http://localhost:8094/docs](http://localhost:8094/docs)
- **ReDoc:** [http://localhost:8094/redoc](http://localhost:8094/redoc)

---

✳️ *Backup Service API — Módulo de respaldo de configuraciones de red.*

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/jcastro03/backup-service)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

