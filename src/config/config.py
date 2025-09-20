import os
from dotenv import load_dotenv

load_dotenv()  # Para usar archivo .env


class Settings:
    APP_NAME: str = "Email Microservice"
    APP_VERSION: str = "1.0.0"

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