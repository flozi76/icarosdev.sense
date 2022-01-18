import signal
import time
import datetime
import sys

from mqtt_client_service import MqttClientService
from sense_service import SenseService
import logging

try:
  from enviro_service import EnviroService
except:
  logging.warning("EnviroService not ready...")


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""weather.py - Print readings from the BME280 weather sensor.

Press Ctrl+C to exit!

""")

is_shutdown = False

def stop(sig, frame):
  logging.info(f"SIGTERM at {datetime.datetime.now()}")
  global is_shutdown
  is_shutdown = True

def ignore(sig, frsma):
  logging.info(f"SIGHUP at {datetime.datetime.now()}")

signal.signal(signal.SIGTERM, stop)
signal.signal(signal.SIGHUP, ignore)

logging.info(f"START at {datetime.datetime.now()}")

client = MqttClientService()

# Try connect Mqtt
device_ready=False
client=None
while not device_ready:
  try:
    client = MqttClientService()
    client.connect()
    device_ready=True
  except:
    logging.warning("Device not yet ready")
  time.sleep(1)

def warm_up_service(service):
  logging.info(f"Performing warmup for service {service}")
  for i in range(10):
    service.read_environment_data()
    time.sleep(0.2)


# Try crate Sense Service for SenseHat

sense_service = None

try:
  sense_service = SenseService()
except:
  logging.warning("SenseHat not available ...")

# Try crate Sense Service for SenseHat
enviro_service = None
try:
  enviro_service = EnviroService()
except:
  logging.warning("EnviroHat not available ...")

try:
  second = 0
  period = 60 * 10
  splash_period = 60

  while not is_shutdown:
    if second % period == 0:
    # Sense Service
      if sense_service is not None:
        warm_up_service(sense_service)
        environment_data = sense_service.read_environment_data()
        client.send_environment_data(environment_data)

        env_value_t = round(environment_data['temperature'], 1)
        sense_service.show_red_message(f"{env_value_t}")
        
        if second % splash_period == 0:
          sense_service.draw_sense_splash()
        
      if enviro_service is not None:
        warm_up_service(enviro_service)
        environment_data = enviro_service.read_environment_data()
        client.send_environment_data(environment_data)
    
    time.sleep(1)
    second += 1
except KeyboardInterrupt as e:
  logging.info("Terminating sense service")
  if sense_service is not None:
    sense_service.clear()
finally:
  if sense_service is not None:
    sense_service.clear()
  client.disconnect()