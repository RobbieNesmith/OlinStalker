import pygame
import pygame.camera
import RPi.GPIO as GPIO
from flask import Flask, render_template, make_response
from functools import wraps, update_wrapper
from datetime import datetime
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
  fname = take_picture()
  lights = get_lights_on()
  lstr = "off"
  if lights:
    lstr = "on"
  return render_template("index.html",lights=lstr,fname=fname)


def take_picture():
  fname = str(int(time.time()))
  pygame.camera.init()
  cam = pygame.camera.Camera("/dev/video0",(1280,720))
  cam.start()
  img = cam.get_image()
  pygame.image.save(img,"static/{}.jpg".format(fname))
  cam.stop()
  return "{}.jpg".format(fname)

def get_lights_on():
  return GPIO.input(23)

if __name__ == "__main__":
  app.run(host="0.0.0.0")

GPIO.cleanup()
