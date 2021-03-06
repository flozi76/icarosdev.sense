import sys
import json
import pytz
from datetime import datetime, timezone
import logging
from enviroplus.noise import Noise
import ST7735
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont

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

    temperature_compensation = 0.8
    temperature_cpu_factor = 9.11
    pressure_compensation = 63.5
    humidity_compensation = 14

    def __init__(self):
        bus = SMBus(1)
        self.bme280 = BME280(i2c_dev=bus)
        self.noise = Noise()
        self.disp = ST7735.ST7735(
            port=0,
            cs=ST7735.BG_SPI_CS_FRONT,
            dc=9,
            backlight=12,
            rotation=270)
        # self.disp.set_backlight(0)
        self.disp.begin()
        self.img = Image.new('RGB', (self.disp.width, self.disp.height), color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.img)
        

    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp

    def compensate_temperature(self, temperature, cpu_temp):
        compensation = (cpu_temp/self.temperature_cpu_factor) + self.temperature_compensation
        compensated = temperature - compensation
        return compensated

    def display_values(self, temperature, humidity, pressure, light):
        WIDTH = self.disp.width
        HEIGHT = self.disp.height
        rect_colour = (0, 60, 60)
        self.draw.rectangle((0, 0, 160, 80), rect_colour)
        

        font_size = 15
        font = ImageFont.truetype(UserFont, font_size)

        colour = (255, 255, 255)
        temperature = "Temp:\t\t{:.2f} ??C\nHum:\t\t\t\t{:.2f}%\nPress:\t\t{:.2f}hPa\nLight:\t\t\t{:.2f}lux".format(temperature, humidity,pressure,light)

        x = 0
        y = 0
        self.draw.text((x, y), temperature, font=font, fill=colour)
        self.disp.display(self.img)

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
            
            low, mid, high, amp = self.noise.get_noise_profile()
            
            low *= 128
            mid *= 128
            high *= 128
            amp *= 64

            temperature_compensated = self.compensate_temperature(temperature, cpu_temp)
            pressure_compensated = pressure + self.pressure_compensation
            humidity_compensated = humidity + self.humidity_compensation

            self.display_values(temperature_compensated, humidity_compensated, pressure_compensated, lux)

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