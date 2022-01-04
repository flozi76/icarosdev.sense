import signal
from sense_hat import SenseHat
from random import randint
import time
import datetime
import sys
from mqtt_client import MqttClient

is_shutdown = False

client = MqttClient()
client.say_hello()

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

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

try:
  second = 0
  period = 1*60

  env_value_h = 0
  env_value_t = 0
  env_value_ta = 0
  env_value_p = 0
  cpu_temp = 0

  while not is_shutdown:
    
    if second % period == 0:
      env_value_h = sense.get_humidity()
      env_value_t = sense.get_temperature()
      env_value_ta = sense.get_temperature_from_pressure()
      env_value_p = sense.get_pressure()
      cpu_temp = get_cpu_temperature()
      
      env_value_h = round(env_value_h, 2)
      env_value_t = round(env_value_t, 2)
      env_value_ta = round(env_value_ta, 2)
      env_value_p = round(env_value_p, 2)
      cpu_temp = round(cpu_temp, 2)

      if second % 10 == 0:
        sense.show_message(f"{env_value_ta}", text_colour=red, back_colour=void, scroll_speed=0.05)
    
    if second % 3 == 0:
      sense.set_pixel(randint(1,6),randint(1,6),pick_random_colour())
    
    sys.stdout.write(f"Sec: {second} Temp: {env_value_t} Temp acc: {env_value_ta} CPU Temp: {cpu_temp}  Hum: {env_value_h} Press: {env_value_p} \r")
    sys.stdout.flush()

    time.sleep(1)
    sense.clear()
    second += 1
except KeyboardInterrupt as e:
  sense.clear()
except:
  sense.clear()
  print("Unexpected error:", sys.exc_info()[0])