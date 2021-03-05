from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from camera import Camera
from database import Database
from images import toByteArray
from starlette.responses import StreamingResponse
import cv2
import io
import datetime

db = Database()
db.connect()

camera = Camera()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/capture/{name}')
def capturePicture(name):

  x = datetime.datetime.now()
  name += x.strftime("-%y-%m-%d-%H-%M-%S")

  image = camera.capture()
  is_success, image_buff = toByteArray(image)

  if(is_success):
    id = db.saveImage(name, image_buff)
    return {"id": id }

  raise HTTPException(status_code=500, detail="Failed to capture an image")

@app.get('/images/{id}')
def getImage(id):
  image = db.getImageById(id)

  if(image is None):
    raise HTTPException(status_code=404)

  return StreamingResponse(io.BytesIO(image), media_type="image/jpg")


@app.get('/version')
def version():
  return {"version": 'v0.1.0'}

@app.get('/version/db')
def dbVersion():
  db_version = db.getVersion()

  return db_version

@app.get('/dbsize')
def dbSize():
  size = db.getDatabaseSize()
  return {"size": size}