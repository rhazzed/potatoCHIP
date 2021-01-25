# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will repeatedly move various channels from min to max
# position in sequence until the user presses Ctrl-C
######################################
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685 as PWM

## import CHIP_IO.GPIO as GPIO

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=1)


# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

try:
  # Move servos between extremes in a loop.
  print('Moving servos, press Ctrl-C to quit...')
  while True:
    print('FNB MIN...')
    pwm.set_pwm(PWM_CH_RIGHT, 0, servo_min)
    time.sleep(1)

    print('FNA MIN...')
    pwm.set_pwm(PWM_CH_LEFT, 0, servo_min)
    time.sleep(1)

    print('ULTRASONIC RANGE SENSOR SERVO MIN...')
    pwm.set_pwm(PWM_CH_SERVO, 0, servo_min)
    time.sleep(1)

    print('FNB MAX...')
    pwm.set_pwm(PWM_CH_RIGHT, 0, servo_max)
    time.sleep(1)

    print('FNA MAX...')
    pwm.set_pwm(PWM_CH_LEFT, 0, servo_max)
    time.sleep(1)

    print('ULTRASONIC RANGE SENSOR SERVO MAX...')
    pwm.set_pwm(PWM_CH_SERVO, 0, servo_max)
    time.sleep(1)

except KeyboardInterrupt:
  print("Stopped by User")
##  print("Cleaning up GPIO")
##  GPIO.cleanup()

