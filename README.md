# 💳 Integración de API de Pagos Khipu

Este repositorio contiene una prueba técnica solicitada por el equipo de Khipu, cuyo objetivo es simular la integración real de su API de pagos utilizando el entorno de pruebas (DemoBank).

## 🧾 Descripción

La integración permite generar un cobro por un monto de $5.000 CLP de forma automática utilizando el endpoint `POST /v3/payments` de Khipu. El pago se realiza a través de un enlace entregado por la API, el cual redirige al entorno de pruebas de DemoBank.

## 🔧 Requisitos

- Python 3.10 o superior
- Cuenta de desarrollador en [https://khipu.com](https://khipu.com)
- Clave API de Khipu (modo desarrollador)

## 📦 Instalación

Clona el repositorio y crea un entorno virtual:

```bash
git clone https://github.com/progexe/khipu-payment.git
cd khipu-payment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
