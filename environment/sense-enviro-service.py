import signal
from sense_hat import SenseHat
from random import randint
import time
import datetime
import sys

is_shutdown = False

def stop(sig, frame):
  print(f"SIGTERM at {datetime.datetime.now()}")
  global is_shutdown
  is_shutdown = True

def ignore(sig, frsma):
  print(f"SIGHUP at {datetime.datetime.now()}")

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGHUP, ignore)

print(f"START at {datetime.datetime.now()}")

device_ready=False
while not device_ready:
  try:
    sense_t = SenseHat()
    device_ready=True
  except:
    print("Device not yet ready")
  time.sleep(1)

sense = SenseHat()
sense.clear()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
void = (0, 0, 0)


# Generate a random colour
def pick_random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)

try:
  counter = 0
  while not is_shutdown:
    counter += 1
    env_value_h = sense.get_humidity()
    env_value_t = sense.get_temperature()
    env_value_ta = sense.get_temperature_from_pressure()
    env_value_p = sense.get_pressure()
    
    env_value_h = round(env_value_h, 2)
    env_value_t = round(env_value_t, 2)
    env_value_ta = round(env_value_ta, 2)
    env_value_p = round(env_value_p, 2)
    # print(f"Temp: {env_value_t}")
    # print(f"Hum: {env_value_h}")
    # print(f"Press: {env_value_p}")
    
    sys.stdout.write(f"Temp: {env_value_t} Temp acc: {env_value_ta}  Hum: {env_value_h} Press: {env_value_p} \r")
    sys.stdout.flush()

    if counter == 10:
      sense.show_message(f"{env_value_ta}", text_colour=red, back_colour=void, scroll_speed=0.05)
      counter = 0
    #sense.show_letter("2",  pick_random_colour())
    time.sleep(1)
except KeyboardInterrupt as e:
  sense.clear()
except:
  sense.clear()
  print("Unexpected error:", sys.exc_info()[0])