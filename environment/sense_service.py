from random import randint
import time
import logging
from sense_hat import SenseHat

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

class SenseService:

    cpu_compensation_factor = 8.5
    pressure_compensation = 65.9
    humidity_compensation = 0
    
    red = (255, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    void = (0, 0, 0)

    def __init__(self):
        sense_client = SenseHat()
        sense_client.clear()
        sense_client.set_rotation(180)
        sense_client.low_light = True
        self.sense_client = sense_client
        self.initialize_joistick()

    def initialize_joistick(self):
        logging.info("Initializing stick ...")

    # Get the temperature of the CPU for compensation
    def get_cpu_temperature(self):
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = f.read()
            temp = int(temp) / 1000.0
        return temp

    def cmpensate_temperature(self, temperature, temperature_pressure, temperature_humidity, cpu_temp):
        mid_temp = (temperature+temperature_pressure+temperature_humidity)/3
        cpu_compensation = cpu_temp/self.cpu_compensation_factor
        compensated = mid_temp - cpu_compensation
        return compensated
        
    def read_environment_data(self):
        humidity = self.sense_client.get_humidity()
        temperature = self.sense_client.get_temperature()
        temperature_pressure = self.sense_client.get_temperature_from_pressure()
        temperature_humidity = self.sense_client.get_temperature_from_humidity()
        pressure = self.sense_client.get_pressure()
        cpu_temp = self.get_cpu_temperature()

        temperature_compensated = self.cmpensate_temperature(temperature, temperature_pressure, temperature_humidity, cpu_temp)
        pressure_compensated = pressure + self.pressure_compensation
        humidity_compensated = humidity + self.humidity_compensation

        return {'temperature': temperature_compensated, 'humidity': humidity_compensated ,'pressure': pressure_compensated, 'cpu_temperature' : cpu_temp}

    def show_red_message(self, message):
        self.sense_client.show_message(message, text_colour=self.red, back_colour=self.void, scroll_speed=0.05)

    def clear(self):
        self.sense_client.clear()
        
    # Generate a random colour
    def pick_random_colour(self):
        random_red = randint(0, 255)
        random_green = randint(0, 255)
        random_blue = randint(0, 255)
        return (random_red, random_green, random_blue)

    def draw_sense_splash(self):
        X = self.pick_random_colour()
        O = [0, 0, 0]
        speed = 0.15
        quad1 = [
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, X, X, O, O, O,
                O, O, O, X, X, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O
                ]
        X = self.pick_random_colour()
        self.sense_client.set_pixels(quad1)
        time.sleep(speed)

        quad2 = [
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O,
                O, O, X, X, X, X, O, O,
                O, O, X, O, O, X, O, O,
                O, O, X, O, O, X, O, O,
                O, O, X, X, X, X, O, O,
                O, O, O, O, O, O, O, O,
                O, O, O, O, O, O, O, O
                ]

        X = self.pick_random_colour()
        self.sense_client.set_pixels(quad2)
        time.sleep(speed)

        quad3 = [
                O, O, O, O, O, O, O, O,
                O, X, X, X, X, X, X, O,
                O, X, O, O, O, O, X, O,
                O, X, O, O, O, O, X, O,
                O, X, O, O, O, O, X, O,
                O, X, O, O, O, O, X, O,
                O, X, X, X, X, X, X, O,
                O, O, O, O, O, O, O, O
                ]

        X = self.pick_random_colour()
        self.sense_client.set_pixels(quad3)
        time.sleep(speed)

        quad4 = [
                X, X, X, X, X, X, X, X,
                X, O, O, O, O, O, O, X,
                X, O, O, O, O, O, O, X,
                X, O, O, O, O, O, O, X,
                X, O, O, O, O, O, O, X,
                X, O, O, O, O, O, O, X,
                X, O, O, O, O, O, O, X,
                X, X, X, X, X, X, X, X
                ]
        self.sense_client.set_pixels(quad4)
        time.sleep(speed)
        self.sense_client.clear()