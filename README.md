# 📧 Notification Service - FastAPI + SMTP + O365

Servicio backend para el envío de notificaciones por correo electrónico utilizando **SMTP** y **Microsoft O365**, desarrollado con **FastAPI** y diseñado para ser escalable, modular y fácil de mantener.

## 🚀 Características

- Envío de correos vía **SMTP** y **O365 Graph API**.
- Soporte para:
  - Archivos adjuntos
  - Imágenes embebidas en HTML
  - Mensajes en texto plano y HTML
- Arquitectura modular con separación de controladores, servicios y modelos.
- Validación de datos con **Pydantic**.
- Configuración centralizada mediante variables de entorno.
- Preparado para pruebas unitarias con **pytest** y **httpx**.
- Documentación automática con **Swagger UI** y **ReDoc**.

---

## 📂 Estructura del proyecto

├── src/
│ ├── config/
│ │ └── config.py
│ ├── controllers/
│ │ └── email_controller.py
│ ├── interfaces/
│ │ └── email_service.py
│ ├── models/
│ │ └── smtp_model.py
│ ├── routes/
│ │ └── send_routes.py  
│ └── services/
│ └── send_services.py
├── tests/
│ ├── test_smtp.py
│ ├── test_o365.py
│ └── test_routes.py
├── main.py
├── requirements.txt
├── .env
└── README.md

---

## ⚙️ Requisitos previos

- **Python 3.10+**
- Cuenta SMTP válida (Gmail, Outlook, etc.) o credenciales de **Microsoft O365**.
- Variables de entorno configuradas (`.env`).

---

## 📦 Instalación

bash

# 1. Clonar el repositorio

git clone https://github.com/devanthony92/notification_service
cd notification-service

# 2. Crear y activar entorno virtual

python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate # Windows

# 3. Instalar dependencias

pip install -r requirements.txt

---

## 🔑 Configuracion

# Configuración SMTP

SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=usuario@example.com
SMTP_PASSWORD=contraseña

# Configuración O365

O365_CLIENT_ID=tu_client_id
O365_CLIENT_SECRET=tu_client_secret
O365_TENANT_ID=tu_tenant_id
O365_USERNAME=usuario@dominio.com
O365_PASSWORD=contraseña

---

## ▶️ Ejecucion

uvicorn main:app --reload

La API estará disponible en:

- Swagger UI → http://localhost:8000/docs#/
- ReDoc → http://localhost:8000/redoc#/

---

## 🧪 Pruebas

pytest --maxfail=1 --disable-warnings -q
