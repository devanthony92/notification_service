import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # Para usar archivo .env

# CONFIGURACION PARA LA DATABASE
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")

# URL DATABASE 
DATABASE_URL = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Crear engine y sesion
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base =  declarative_base()


class Settings:
    APP_NAME: str = os.getenv("APP_NAME")
    APP_VERSION: str = os.getenv("APP_VERSION")

    # SMTP
    SMTP_URL : str = "http://smtp_service:8000/send/"
    SMTP_SERVER: str = os.getenv("SMTP_SERVER")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT"))
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASS: str = os.getenv("SMTP_PASS")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM")

    # O365
    O365_URL : str = "http://o365_service:8000/send/"
    O365_CLIENT_ID: str = os.getenv("O365_CLIENT_ID")
    O365_CLIENT_SECRET: str = os.getenv("O365_CLIENT_SECRET")
    O365_TENANT_ID: str = os.getenv("O365_TENANT_ID")
    O365_USERNAME: str = os.getenv("O365_USERNAME")
settings = Settings()

# mantener la conexion a la BD siempre abierta
def get_session():
    db = SessionLocal()
    try:
        yield db   
    finally:
        db.close()