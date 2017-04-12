# Use the PCA9685 PWM servo/LED controller library to set one
# servo to the position specified on the command line.
######################################
from __future__ import division
import time
import sys

# Import the PCA9685 module.
import Adafruit_PCA9685 as PWM

import CHIP_IO.GPIO as GPIO

#set PWM Controller channels
PWM_CH_SERVO = 7


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_mid = 353
servo_max = 580  # Max pulse length out of 4096 (600 torqued one servo too much)

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

try:
  # Move servos to the value the user supplied
  for arg in sys.argv[1:]:
    val = int(arg)

  print('Moving servo to %d\n' % val)
  pwm.set_pwm(PWM_CH_SERVO, 0, val)


except KeyboardInterrupt:
  print("Stopped by User")
  print("Cleaning up GPIO")
  GPIO.cleanup()

