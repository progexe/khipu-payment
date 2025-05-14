
import requests # type: ignore

url = "https://payment-api.khipu.com/v3/payments"

payload = {
  "amount": 5000,
  "currency": "CLP",
  "subject": "Cobro de prueba"
}

headers = {
  "Content-Type": "application/json",
  "x-api-key": "f3b2a14b-f221-4cf8-bfc8-3b7c24b0a972"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)