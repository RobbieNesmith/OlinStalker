IMPORT rPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

def printFunction(channel):
  print("function")

GPIO.add_event_detect(17,GPIO.RISING,callback=printFunction,bouncetime=300)
while True:
  pass
GPIO.cleanup()()
