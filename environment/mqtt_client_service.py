import sys
import paho.mqtt.client as mqtt
import json
import pytz
from datetime import datetime, timezone

class MqttClientService:

    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def send_environment_data(self, humidity, temperature, temperature_humidity, temperature_pressure, pressure, cpu_temperature):

        ZRH = pytz.timezone('Europe/Zurich')
        utc_dt = datetime.now(timezone.utc)

        date_time = utc_dt.astimezone(ZRH)
        

        json_env_data = {
            "date_time" : f"{date_time}",
            "humidity" : humidity,
            "temperature" : temperature,
            "temperature_humidity" : temperature_humidity,
            "temperature_pressure" : temperature_pressure,
            "pressure" : pressure,
            "cpu_temperature" : cpu_temperature
        }

        env_data_str = json.dumps(json_env_data)

        self.mqtt_client.connect("raspberrypi.local",1883,60)
        self.mqtt_client.publish("topic/environment/data", env_data_str)
        self.mqtt_client.disconnect()

        humidity = round(humidity, 2)
        temperature = round(temperature, 4)
        temperature_humidity = round(temperature_humidity, 4)
        temperature_pressure = round(temperature_pressure, 4)
        pressure = round(pressure, 2)
        cpu_temperature = round(cpu_temperature, 2)

        sys.stdout.write(f"Temp: {temperature} Temp humidity: {temperature_humidity} Temp pressure: {temperature_pressure} CPU Temp: {cpu_temperature}  Hum: {humidity} Press: {pressure} \r")
        sys.stdout.flush()
    