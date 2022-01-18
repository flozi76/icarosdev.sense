import sys
import json
import pytz
from datetime import datetime, timezone
import logging

from bme280 import BME280
from enviroplus import gas

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class EnviroService:

    temperature_compensation = 2.5
    pressure_compensation = 63
    humidity_compensation = 14

    def __init__(self):
        bus = SMBus(1)
        self.bme280 = BME280(i2c_dev=bus)

    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp

    def read_environment_data(self):
            temperature = self.bme280.get_temperature()
            pressure = self.bme280.get_pressure()
            humidity = self.bme280.get_humidity()
            cpu_temp = self.get_cpu_temperature()
            readings = gas.read_all()
            reducing = readings.reducing
            oxidising = readings.oxidising
            nh3 = readings.nh3
            lux = ltr559.get_lux()

            temperature_compensated = temperature - self.temperature_compensation
            pressure_compensated = pressure + self.pressure_compensation
            humidity_compensated = humidity + self.humidity_compensation


            return {'temperature': temperature_compensated, 'humidity': humidity_compensated ,'pressure': pressure_compensated, 
            'cpu_temperature' : cpu_temp, 'reducing' : reducing, 'oxidising' : oxidising, 'nh3' : nh3, 'lux' : lux}

    def run_test(self):
        temperature = self.bme280.get_temperature()
        pressure = self.bme280.get_pressure()
        humidity = self.bme280.get_humidity()
        logging.info("""Temperature: {:05.2f} *C
Pressure: {:05.2f} hPa
Relative humidity: {:05.2f} %
""".format(temperature, pressure, humidity))

        readings = gas.read_all()
        logging.info(readings)

        lux = ltr559.get_lux()
        prox = ltr559.get_proximity()
        logging.info("""Light: {:05.02f} Lux
Proximity: {:05.02f}
""".format(lux, prox))