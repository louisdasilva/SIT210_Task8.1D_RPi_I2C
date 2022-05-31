# Code modified and adapted from
# https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
# https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bh1750.py

import smbus
import time

bus = smbus.SMBus(1) 
DEVICE = 0x23 # Default device I2C address, confirm: type <sudo i2cdetect -y 1> into terminal

# https://mouser.com/datasheet/2/348/bh1750fvi-e-186247.pdf
# page 5 Instruction set architecture
ONE_TIME_HIGHRES = 32

def readLight():
  # Read data from I2C interface
  data = bus.read_i2c_block_data(DEVICE, ONE_TIME_HIGHRES)

  # https://mouser.com/datasheet/2/348/bh1750fvi-e-186247.pdf
  # first byte high, second byte low so high byte starts at 256
  # divide by 1.2 to convert count to lux as per datasheet pg 11
  data = (data[1] + (256 * data[0])) / 1.2 
  
  if(data > 900):
      return "too bright"
  if(data > 600):
      return "bright"
  if(data > 200):
      return "medium"
  if(data > 100):
      return "dark"
  if(data <= 100):
      return "too dark"
  
def main():

  while True:
    lightLevel=readLight()
    print("Light Level: " + lightLevel)
    time.sleep(1)

if __name__=="__main__":
   main()