import sys
import paho.mqtt.client as mqtt
import json
import pytz
from datetime import datetime, timezone
import logging
import paho.mqtt.client as mqtt
import socket

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class MqttClientService:

    topic = "topic/environment/data"
    mqtt_broker = "raspberrypi.local"
    mqtt_broker_port = 1883
    def __init__(self):
        mqtt_client = mqtt.Client()
        self.mqtt_client = mqtt_client
        self.raspi_name = socket.gethostname()

    def connect(self):
        print(self.raspi_name)
        logging.info(f"Starting connection on raspberry {self.raspi_name}")
        self.mqtt_client.connect(self.mqtt_broker,self.mqtt_broker_port,60)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.loop_start()
    
    def disconnect(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.info("Unexpected MQTT disconnection. Will auto-reconnect")

    def on_connect(self, client, userdata, rc, tc):
        if rc != 0:
            logging.info(f"MQTT Client Connected Broker: {self.mqtt_broker}:{self.mqtt_broker_port}")

    def send_environment_data(self, environment_data):

        ZRH = pytz.timezone('Europe/Zurich')
        utc_dt = datetime.now(timezone.utc)

        date_time = utc_dt.astimezone(ZRH)
        

        json_env_data = {
            "date_time" : f"{date_time}",
            "raspi_name" : self.raspi_name,

            "env_data" : environment_data,
        }

        env_data_str = json.dumps(json_env_data)
        
        self.mqtt_client.publish(self.topic, env_data_str, qos=1)

        logging.info(json_env_data)
    