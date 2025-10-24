// ...existing code...
# 🛎️ Backup Service API

API ligera en FastAPI para ejecutar backups automáticos y manuales de configuraciones de equipos de red. La API obtiene la lista de equipos desde Zabbix, se conecta por SSH para leer la configuración y persiste los backups en la tabla `backrest`.

---

## 📁 Estructura relevante
- [main.py](main.py) — endpoints y configuración del scheduler.
- [services/backup_service.py](services/backup_service.py) — lógica principal para crear backups (`services.backup_service.crear_backups_todos`).
- [services/ssh_service.py](services/ssh_service.py) — conexión SSH y obtención de configuración (`services.ssh_service.obtener_configuracion_ssh`).
- [repositories/zabbix_repo.py](repositories/zabbix_repo.py) — consulta de hosts en Zabbix (`repositories.zabbix_repo.get_zabbix_hosts`).
- [repositories/backrest_repo.py](repositories/backrest_repo.py) — persiste backups en BD (`repositories.backrest_repo.guardar_backrest`).
- [config.py](config.py) — variables de entorno y configuración.
- [db.py](db.py) — fábrica de engine SQLAlchemy (`db.get_engine`).
- [security.py](security.py) — autenticación por Bearer JWT (`security.get_current_user`).

---

## 🔐 Autenticación
Todos los endpoints protegen el acceso con JWT mediante la dependencia [`security.get_current_user`](security.py). En las peticiones debes enviar:

- Header: Authorization: Bearer <TOKEN>
- O como query param: ?token=<TOKEN>

El token se valida con la `SECRET_KEY` y `JWT_ALGORITHM` definidos en [config.py](config.py).

---

## 📦 Variables de entorno importantes
Define en `.env` (ya hay ejemplo en tu `.env`):
- DB_ENGINE (MYSQL o POSTGRES)
- DB_URL_MYSQL / DB_URL_POSTGRES
- SSH_USER, SSH_PASS, SSH_TIMEOUT
- SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

Consulta [config.py](config.py) para ver cómo se cargan.

---

## 🚀 Endpoints principales

1) Crear backups para todos (manual)
- Método: GET
- Ruta: /backups/create/all
- Autenticación: requerida
- Acción: ejecuta [`services.backup_service.crear_backups_todos`](services/backup_service.py)
- Respuesta: resumen con motor, total de hosts y resultados por host.

2) Crear backup para un equipo (manual)
- Método: GET
- Ruta: /backups/create/{nombre}
- Parámetros: nombre (path)
- Autenticación: requerida
- Acción: busca último registro en la tabla `backrest`, obtiene IP y ejecuta `obtener_configuracion_ssh`, luego persiste con `guardar_backrest`.
- Respuesta: mensaje, ip, marca, nueva_configuracion (preview) y último_registro.

---

## ⏰ Scheduler / Cron integrado
La API configura una tarea programada al iniciar la aplicación via `configurar_cron_backup` en [main.py](main.py). Por defecto se inicia con:
- Hora configurada en startup: actualmente `configurar_cron_backup("23:59")` (ajusta si necesitas otra hora).
- El job ejecuta `services.backup_service.crear_backups_todos` y loggea inicio/fin.

---

## 🗄 Base de datos
- Conexión: generada por [`db.get_engine`](db.py) usando la URL definida en `.env`.
- Tabla objetivo: `backrest` (insertos realizados en `repositories/backrest_repo.guardar_backrest`).
- Asegúrate de tener las tablas y permisos necesarios en MySQL/Postgres según `DB_ENGINE`.

---

## 🧪 Requisitos / Instalación
1. Crear entorno virtual y activar:
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
3. Configurar `.env` con credenciales de BD y SSH (ver apartado variables de entorno).

---

## 🐳 Docker
Imagen base y comandos listos en [dockerfile](dockerfile). Para construir y ejecutar:
```bash
docker build -t backup-service .
docker run -e $(cat .env | xargs) -p 8094:8094 backup-service
```

---

## ⚙️ Problemas comunes y debugging
- Timeout SSH: ajusta `SSH_TIMEOUT` en `.env`.
- Algoritmos SSH incompatibles: `services/ssh_service.py` intenta diferentes disabled_algorithms.
- Visibilidad de inserciones en BD: si usas SQLAlchemy engine vs. conexión nativa, revisa commits y transacciones en `repositories/backrest_repo.py`.

---

## 📌 Notas finales
- Para ver el código de los puntos clave, abre:
  - [`main.crear_backups`](main.py)
  - [`services.backup_service.crear_backups_todos`](services/backup_service.py)
  - [`services.ssh_service.obtener_configuracion_ssh`](services/ssh_service.py)
  - [`repositories.backrest_repo.guardar_backrest`](repositories/backrest_repo.py)
  - [`repositories.zabbix_repo.get_zabbix_hosts`](repositories/zabbix_repo.py)

- Endpoints documentados automáticamente por FastAPI en:
  - Swagger UI: http://localhost:8094/docs
  - ReDoc: http://localhost:8094/redoc

Si quieres, actualizo la README con ejemplos de requests (curl / Postman) o añado un apartado de diseño de DB. 
```// filepath: readme.md
// ...existing code...
# 🛎️ Backup Service API

API ligera en FastAPI para ejecutar backups automáticos y manuales de configuraciones de equipos de red. La API obtiene la lista de equipos desde Zabbix, se conecta por SSH para leer la configuración y persiste los backups en la tabla `backrest`.

---

## 📁 Estructura relevante
- [main.py](main.py) — endpoints y configuración del scheduler.
- [services/backup_service.py](services/backup_service.py) — lógica principal para crear backups (`services.backup_service.crear_backups_todos`).
- [services/ssh_service.py](services/ssh_service.py) — conexión SSH y obtención de configuración (`services.ssh_service.obtener_configuracion_ssh`).
- [repositories/zabbix_repo.py](repositories/zabbix_repo.py) — consulta de hosts en Zabbix (`repositories.zabbix_repo.get_zabbix_hosts`).
- [repositories/backrest_repo.py](repositories/backrest_repo.py) — persiste backups en BD (`repositories.backrest_repo.guardar_backrest`).
- [config.py](config.py) — variables de entorno y configuración.
- [db.py](db.py) — fábrica de engine SQLAlchemy (`db.get_engine`).
- [security.py](security.py) — autenticación por Bearer JWT (`security.get_current_user`).

---

## 🔐 Autenticación
Todos los endpoints protegen el acceso con JWT mediante la dependencia [`security.get_current_user`](security.py). En las peticiones debes enviar:

- Header: Authorization: Bearer <TOKEN>
- O como query param: ?token=<TOKEN>

El token se valida con la `SECRET_KEY` y `JWT_ALGORITHM` definidos en [config.py](config.py).

---

## 📦 Variables de entorno importantes
Define en `.env` (ya hay ejemplo en tu `.env`):
- DB_ENGINE (MYSQL o POSTGRES)
- DB_URL_MYSQL / DB_URL_POSTGRES
- SSH_USER, SSH_PASS, SSH_TIMEOUT
- SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES

Consulta [config.py](config.py) para ver cómo se cargan.

---

## 🚀 Endpoints principales

1) Crear backups para todos (manual)
- Método: GET
- Ruta: /backups/create/all
- Autenticación: requerida
- Acción: ejecuta [`services.backup_service.crear_backups_todos`](services/backup_service.py)
- Respuesta: resumen con motor, total de hosts y resultados por host.

2) Crear backup para un equipo (manual)
- Método: GET
- Ruta: /backups/create/{nombre}
- Parámetros: nombre (path)
- Autenticación: requerida
- Acción: busca último registro en la tabla `backrest`, obtiene IP y ejecuta `obtener_configuracion_ssh`, luego persiste con `guardar_backrest`.
- Respuesta: mensaje, ip, marca, nueva_configuracion (preview) y último_registro.

---

## ⏰ Scheduler / Cron integrado
La API configura una tarea programada al iniciar la aplicación via `configurar_cron_backup` en [main.py](main.py). Por defecto se inicia con:
- Hora configurada en startup: actualmente `configurar_cron_backup("23:59")` (ajusta si necesitas otra hora).
- El job ejecuta `services.backup_service.crear_backups_todos` y loggea inicio/fin.

---

## 🗄 Base de datos
- Conexión: generada por [`db.get_engine`](db.py) usando la URL definida en `.env`.
- Tabla objetivo: `backrest` (insertos realizados en `repositories/backrest_repo.guardar_backrest`).
- Asegúrate de tener las tablas y permisos necesarios en MySQL/Postgres según `DB_ENGINE`.

---

## 🧪 Requisitos / Instalación
1. Crear entorno virtual y activar:
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
3. Configurar `.env` con credenciales de BD y SSH (ver apartado variables de entorno).

---

## 🐳 Docker
Imagen base y comandos listos en [dockerfile](dockerfile). Para construir y ejecutar:
```bash
docker build -t backup-service .
docker run -e $(cat .env | xargs) -p 8094:8094 backup-service
```

---

## ⚙️ Problemas comunes y debugging
- Timeout SSH: ajusta `SSH_TIMEOUT` en `.env`.
- Algoritmos SSH incompatibles: `services/ssh_service.py` intenta diferentes disabled_algorithms.
- Visibilidad de inserciones en BD: si usas SQLAlchemy engine vs. conexión nativa, revisa commits y transacciones en `repositories/backrest_repo.py`.

---

## 📌 Notas finales
- Para ver el código de los puntos clave, abre:
  - [`main.crear_backups`](main.py)
  - [`services.backup_service.crear_backups_todos`](services/backup_service.py)
  - [`services.ssh_service.obtener_configuracion_ssh`](services/ssh_service.py)
  - [`repositories.backrest_repo.guardar_backrest`](repositories/backrest_repo.py)
  - [`repositories.zabbix_repo.get_zabbix_hosts`](repositories/zabbix_repo.py)

- Endpoints documentados automáticamente por FastAPI en:
  - Swagger UI: http://localhost:8094/docs
  - ReDoc: http://localhost:8094/redoc 