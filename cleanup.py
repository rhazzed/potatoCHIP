#
import time
# Import the PCA9685 16-channel I2C PWM module.
import Adafruit_PCA9685 as PWM
# Import the GPIO library
import CHIP_IO.GPIO as GPIO

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *

# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=2)

#set GPIO pin directions (IN / OUT) for Ultrasonic Range Detector
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#set GPIO pin directions (IN / OUT) for Tracks
GPIO.setup(GPIO_RFRONT, GPIO.OUT)
GPIO.setup(GPIO_RREAR, GPIO.OUT)
GPIO.setup(GPIO_LFRONT, GPIO.OUT)
GPIO.setup(GPIO_LREAR, GPIO.OUT)


# Center the servo
pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round( servo_min + ((servo_max - servo_min)/2) )))
time.sleep(1)

# Stop the left track
pwm.set_pwm(PWM_CH_LEFT, 0, TRACK_STOP)
GPIO.output(GPIO_LFRONT, GPIO.LOW)
GPIO.output(GPIO_LREAR, GPIO.LOW)

# Stop the right track
pwm.set_pwm(PWM_CH_RIGHT, 0, TRACK_STOP)
GPIO.output(GPIO_RFRONT, GPIO.LOW)
GPIO.output(GPIO_RREAR, GPIO.LOW)

GPIO.cleanup()
