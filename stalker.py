import pygame
import pygame.camera
import RPi.GPIO as GPIO
from flask import Flask, render_template, make_response
from functools import wraps, update_wrapper
from datetime import datetime
import os
import time
import dht11

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
app = Flask(__name__)
app.debug = True

temp = 0
humidity = 0
moveFile = ""
timeVal = 0

def movementCamera(channel):
  global timeVal
  global moveFile
  newTime = time.time()
  if newTime - timeVal > 5:
    mf = str(int(time.time()))
    pygame.camera.init()
    cam = pygame.camera.Camera("/dev/video0",(1280,720))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,"static/{}move.jpg".format(mf))
    cam.stop()
    moveFile = "{}move.jpg".format(mf)
    timeVal = newTime

GPIO.add_event_detect(17,GPIO.RISING, callback=movementCamera,bouncetime=300)

@app.route("/")
def index():
  fname = take_picture()
  lights = get_lights_on()
  th = get_temp()
  lstr = "off"
  if lights:
    lstr = "on"
  return render_template("index.html",lights=lstr,fname=fname,move=moveFile,temp=th[0],humidity=th[1])

def get_temp():
  global temp
  global humidity
  instance = dht11.DHT11(pin = 14)
  result = instance.read()
  if result.is_valid():
    temp = result.temperature
    humidity = result.humidity
  return ("Temperature {}\N{DEGREE SIGN}C, {}\N{DEGREE SIGN}F".format(temp,temp * 9/5 + 32),"Humidity {}%".format(humidity))

def take_picture():
  fname = str(int(time.time()))
  pygame.camera.init()
  cam = pygame.camera.Camera("/dev/video0",(1280,720))
  cam.start()
  img = cam.get_image()
  cam.stop()
  pygame.image.save(img,"static/{}.jpg".format(fname))
  return "{}.jpg".format(fname)

def get_lights_on():
  return GPIO.input(23)

if __name__ == "__main__":
  app.run(host="0.0.0.0")

GPIO.cleanup()
cam.stop()
