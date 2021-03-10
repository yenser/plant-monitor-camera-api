from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from io import BytesIO
from time import sleep
import picamera
import subprocess

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/healthcheck')
def healthcheck():
    result = subprocess.run('cat /sys/class/thermal/thermal_zone0/temp', stdout=subprocess.PIPE,  shell=True)
    fileTemp = result.stdout
    temp = float(fileTemp)/1000
    return {'status': 'OK', 'temperature': temp}


@app.get('/capture')
def captureImage():
    print("Taking picture")
    with picamera.PiCamera() as camera:
        image_stream = BytesIO()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(1)
        camera.capture(image_stream, 'jpeg')

        buff_size = str(image_stream.getbuffer().nbytes)
        image_stream.seek(0) # move to start position

        return StreamingResponse(image_stream, media_type="image/jpeg", headers={'Content-Length': buff_size})
