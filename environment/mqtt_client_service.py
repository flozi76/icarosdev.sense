import sys
import paho.mqtt.client as mqtt
import json
import pytz
from datetime import datetime, timezone

class MqttClientService:

    mqtt_broker = "raspberrypi.local"
    mqtt_broker_port = 1883
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def connect(self):
        self.mqtt_client.connect(self.mqtt_broker,self.mqtt_broker_port,60)

        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.loop_start()
    
    def disconnect(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def on_connect(self, client, userdata, rc, tc):
        if rc != 0:
            print(f"MQTT Client Connected Broker: {self.mqtt_broker}:{self.mqtt_broker_port}")

    def send_environment_data(self, environment_data):

        ZRH = pytz.timezone('Europe/Zurich')
        utc_dt = datetime.now(timezone.utc)

        date_time = utc_dt.astimezone(ZRH)
        

        json_env_data = {
            "date_time" : f"{date_time}",
            "humidity" : environment_data['humidity'],
            "temperature" : environment_data['temperature'],
            "pressure" : environment_data['pressure'],
        }

        env_data_str = json.dumps(json_env_data)

        
        self.mqtt_client.publish("topic/environment/data", env_data_str)


        humidity = round(environment_data['humidity'], 1)
        temperature = round(environment_data['temperature'], 1)
        pressure = round(environment_data['pressure'], 1)
        cpu_temperature = round(environment_data['cpu_temperature'], 2)

        sys.stdout.write(f"Temp: {temperature} CPU Temp: {cpu_temperature}  Hum: {humidity} Press: {pressure} \r")
        sys.stdout.flush()
    