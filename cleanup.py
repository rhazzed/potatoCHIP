#
import time
# Import the PCA9685 16-channel I2C PWM module.
import Adafruit_PCA9685 as PWM
# Import the GPIO library
###import CHIP_IO.GPIO as GPIO
import Adafruit_GPIO as gpio
GPIO = gpio.get_platform_gpio()

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *

# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 1, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=1)

#set GPIO pin directions (IN / OUT) for Ultrasonic Range Detector
GPIO.setup(GPIO_TRIGGER, gpio.OUT)
GPIO.setup(GPIO_ECHO, gpio.IN)

#set GPIO pin directions (IN / OUT) for Tracks
GPIO.setup(GPIO_RFRONT, gpio.OUT)
GPIO.setup(GPIO_RREAR, gpio.OUT)
GPIO.setup(GPIO_LFRONT, gpio.OUT)
GPIO.setup(GPIO_LREAR, gpio.OUT)


# Center the servo
pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round( servo_min + ((servo_max - servo_min)/2) )))
time.sleep(1)

# Stop the left track
pwm.set_pwm(PWM_CH_LEFT, 0, TRACK_STOP)
GPIO.output(GPIO_LFRONT, gpio.LOW)
GPIO.output(GPIO_LREAR, gpio.LOW)

# Stop the right track
pwm.set_pwm(PWM_CH_RIGHT, 0, TRACK_STOP)
GPIO.output(GPIO_RFRONT, gpio.LOW)
GPIO.output(GPIO_RREAR, gpio.LOW)

GPIO.cleanup()
