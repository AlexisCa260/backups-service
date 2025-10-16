import os

from dotenv import load_dotenv

load_dotenv()

# =======================================
# 🔧 CONFIGURACIÓN GENERAL
# =======================================
DB_ENGINE = os.getenv("DB_ENGINE", "").upper()
DB_URL = os.getenv("DB_URL")

if DB_ENGINE == "MYSQL":
    DB_URL = os.getenv("DB_URL_MYSQL")
elif DB_ENGINE == "POSTGRES":
    DB_URL = os.getenv("DB_URL_POSTGRES")
else:
    if not DB_URL:
        raise ValueError(
            f"Motor de base de datos no soportado o DB_URL no configurada: {DB_ENGINE}"
        )

# =======================================
# 🔐 CONFIGURACIÓN DE SEGURIDAD
# =======================================
SECRET_KEY = os.getenv("SECRET_KEY", "super_secret")
JWT_ALGORITHM = "HS256"

# =======================================
# ⚙️ CONFIGURACIÓN SSH
# =======================================
SSH_USER = os.getenv("SSH_USER")
SSH_PASS = os.getenv("SSH_PASS")
SSH_TIMEOUT = int(os.getenv("SSH_TIMEOUT", "10"))
