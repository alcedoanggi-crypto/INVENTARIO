"""
Configuracion central de la aplicacion.
"""
import os
import urllib.parse
from datetime import timedelta

# Forzar a la libreria de PostgreSQL a comunicarse siempre en UTF-8
os.environ["PGCLIENTENCODING"] = "utf-8"

basedir = os.path.abspath(os.path.dirname(__file__))


def _database_uri() -> str:
    """
    Obtiene la URL de conexion a la base de datos.
    1. Busca la variable de entorno DATABASE_URL.
    2. Si no existe, se conecta a PostgreSQL local (inventario_db).
    """
    url = os.environ.get("DATABASE_URL")

    if not url:
        db_user = os.environ.get("DB_USER", "postgres")
        # Contraseña configurada a 'admin123'
        db_pass = os.environ.get("DB_PASSWORD", "admin123")

        # Codifica la contraseña para evitar errores con caracteres especiales o tildes
        db_pass_encoded = urllib.parse.quote_plus(db_pass)

        db_host = os.environ.get("DB_HOST", "localhost")
        db_port = os.environ.get("DB_PORT", "5432")
        db_name = os.environ.get("DB_NAME", "inventario_db")

        url = f"postgresql://{db_user}:{db_pass_encoded}@{db_host}:{db_port}/{db_name}"

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-desarrollo-inventario")

    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Forzar codificación UTF-8 a nivel de motor SQLAlchemy
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"options": "-c client_encoding=utf8"}
    }

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    UPLOAD_FOLDER = os.path.join(basedir, "app", "static", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    DEFAULT_MIN_STOCK = 5

    PRODUCTS_PER_PAGE = 10
    MOVEMENTS_PER_PAGE = 15


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
    WTF_CSRF_ENABLED = False
    # Puedes usar una carpeta temporal de pruebas si lo prefieres
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "tests", "test_uploads")

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}