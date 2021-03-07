from fastapi import FastAPI

app = FastAPI()

@app.get('/capture')
def captureImage():
  from io import BytesIO
  from time import sleep
  from picamera import PiCamera
  import requests

  my_stream = BytesIO()
  camera = PiCamera()
  camera.start_preview()
  # Camera warm-up time
  sleep(1)
  camera.capture(my_stream, 'jpeg')

  r = requests.post('http://192.168.50.156:8080/images/name.jpg', data=my_stream.getbuffer() ,headers={'Content-Type': 'image/jpeg', 'Content-Length': str(my_stream.getbuffer().nbytes)})
  return r.json()
