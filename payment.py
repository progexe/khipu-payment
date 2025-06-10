from flask import Flask, render_template_string, redirect
import requests # type: ignore

app = Flask(__name__)


API_KEY = "21505680-02e4-46f4-8dcf-8121c66fb1d4"

HTML_INDEX = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Pagar con Khipu</title>
</head>
<body>
    <h2>Prueba de integración Khipu</h2>
    <form action="/pagar" method="get">
        <button type="submit">
            <img src="https://s3.amazonaws.com/static.khipu.com/buttons/chile/2024/banks-163x127.svg" alt="110x50-tu-banco" alt="Pagar con Khipu">
        </button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_INDEX)

@app.route('/pagar')
def pagar():
    
    url = "https://payment-api.khipu.com/v3/payments"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": "21505680-02e4-46f4-8dcf-8121c66fb1d4"
    }

    payload = {
        "amount": 5000,
        "currency": "CLP",
        "subject": "Cobro de prueba desde Flask",
        "transaction_id": "pago-flask-khipu-001",
        "return_url": "https://tusitio.com/retorno",
        "cancel_url": "https://tusitio.com/cancelado"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return redirect(data.get("payment_url"))
    except Exception as e:
        return f"<h3>Error al generar el cobro: {e}</h3>"

if __name__ == '__main__':
    app.run(debug=True)