from flask import Flask, request, jsonify, send_file
import cv2
import requests
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

api_key = os.getenv('GOOGLE_API_KEY')
email_password = os.getenv('EMAIL_PASSWORD')

def capture_photo():
    # Acceso a la webcam
    cam = cv2.VideoCapture(0)
    result, image = cam.read()
    if result:
        photo_path = "photo.jpg"
        cv2.imwrite(photo_path, image)
    else:
        photo_path = None
    cam.release()
    return photo_path

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
    
    if photo_path:
        attachment = open(photo_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(photo_path)}")
        msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "ftbq cknu iztg adyu ")  # Cambia aquí con la contraseña de aplicación
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

@app.route('/run', methods=['GET'])
def run_script():
    api_key = "AIzaSyDBoTuvRrlDEq3I-_ZTP5vKfEIITIBQGYY"  # Reemplaza con tu clave de API de Google
    
    photo_path = capture_photo()
    location, address, maps_url = get_location(api_key)
    if location:
        send_email(photo_path, location, address, maps_url)
        
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
        return jsonify(status="success", message="Email sent successfully.")
    else:
        return jsonify(status="error", message="Failed to obtain location.")

if __name__ == '__main__':
    app.run(debug=True)
