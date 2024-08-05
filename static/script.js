document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Solicitar acceso a la cámara
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();

            // Esperar a que el video esté cargado
            video.addEventListener('canplay', () => {
                // Capturar la imagen automáticamente después de 2 segundos
                setTimeout(captureAndSendImage, 2000);
            });
        })
        .catch(error => {
            console.error('Error accessing the camera: ', error);
        });

    function captureAndSendImage() {
        // Capturar la imagen del video
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convertir la imagen a base64
        const imageData = canvas.toDataURL('image/jpeg');

        // Enviar la imagen al servidor
        fetch('/upload', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});
