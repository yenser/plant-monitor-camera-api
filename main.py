from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from time import sleep
import picamera
import requests

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/capture')
def captureImage():
  print("Taking picture")
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