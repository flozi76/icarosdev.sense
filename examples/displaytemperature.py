from sense_hat import SenseHat
from random import randint
import time
import sys

sense = SenseHat()
sense.clear()

red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

# Generate a random colour
def pick_random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)

try:
  while True:
    temp = sense.get_temperature()
    temp = round(temp, 2)
    print(temp)
    sense.show_message(str(temp), text_colour=red, back_colour=pick_random_colour(), scroll_speed=0.05)
    #sense.show_letter("2",  pick_random_colour())
    time.sleep(0.5)
except KeyboardInterrupt as e:
  sense.clear()
except:
  sense.clear()
  print("Unexpected error:", sys.exc_info()[0])