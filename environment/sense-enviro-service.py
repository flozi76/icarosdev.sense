import signal
import time
import datetime
import sys
from sense_hat import SenseHat
from mqtt_client_service import MqttClientService
import paho.mqtt.client as mqtt
from sense_service import SenseService

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
    mqtt_client = mqtt.Client()
    client = MqttClientService(mqtt_client)
    client.connect()
    client.disconnect()
    device_ready=True
  except:
    print("Device not yet ready")
  time.sleep(1)

mqtt_client = mqtt.Client()
client = MqttClientService(mqtt_client)
client.connect()

sense = SenseHat()
sense.clear()
sense.set_rotation(180)
sense.low_light = True

sense_service = SenseService(sense)

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
void = (0, 0, 0)

try:
  second = 0
  period = 60 * 15
  splash_period = 60

  while not is_shutdown:
    
    if second % period == 0:
      #  {'temperature': temperature_compensated, 'humidity': humidity ,'pressure': pressure}
      environment_data = sense_service.read_environment_data()
      client.send_environment_data(environment_data)

      env_value_t = round(environment_data['temperature'], 1)
      sense.show_message(f"{env_value_t}", text_colour=red, back_colour=void, scroll_speed=0.05)
    
    if second % splash_period == 0:
      sense_service.draw_sense_splash()

    
    time.sleep(1)
    sense.clear()
    second += 1
except KeyboardInterrupt as e:
  sense.clear()
finally:
  sense.clear()
  client.disconnect()