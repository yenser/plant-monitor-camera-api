from fastapi import FastAPI
from io import BytesIO
from time import sleep
import picamera
import requests

app = FastAPI()

@app.get('/capture')
def captureImage():
  with picamera.PiCamera() as camera:
    image_stream = BytesIO()
    camera.start_preview()
    # Camera warm-up time
    sleep(1)
    camera.capture(image_stream, 'jpeg')

    r = requests.post('http://192.168.50.156:8080/images/name.jpg',
      data=image_stream.getbuffer(),
      headers={'Content-Type': 'image/jpeg', 'Content-Length': str(image_stream.getbuffer().nbytes)})
    return r.json()
