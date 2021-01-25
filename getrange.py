#!/usr/bin/python
##################################
# getrange.py - Get distance reading from ultrasonic range detector
#               on GPIO pins GPIO_TRIGGER_F and GPIO_ECHO_F
#
# HISTORICAL INFORMATION -
#
#  2016-xx-xx  Eric/Mike  Created for Raspberry pi
#  2017-02-04  msipin  Adapted to C.H.I.P. by replacing GPIO library,
#                      editing pins and adding "settling time" before
#                      the ultrasonic sensor is triggered.
#  2021-01-24  msipin  Changed definition for "main" ultrasonic sensor pins.
#  2021-01-25  msipin  Added left and right ultrasonic sensors and parameterized "distance" function
##################################

#Libraries
#import CHIP_IO.GPIO as GPIO
import Adafruit_GPIO as gpio
GPIO = gpio.get_platform_gpio()
import time
import sys


# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *


#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_L, gpio.OUT)
GPIO.setup(GPIO_ECHO_L, gpio.IN)
#
GPIO.setup(GPIO_TRIGGER_F, gpio.OUT)
GPIO.setup(GPIO_ECHO_F, gpio.IN)
#
GPIO.setup(GPIO_TRIGGER_R, gpio.OUT)
GPIO.setup(GPIO_ECHO_R, gpio.IN)


def distance(trigger_gpio,echo_gpio):

	# Settle the trigger to zero
	GPIO.output(trigger_gpio, False)

	# Wait for trigger to settle
	time.sleep(0.25)

	# Send trigger pulse
	# set Trigger to HIGH
	GPIO.output(trigger_gpio, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(trigger_gpio, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(echo_gpio) == 0:
		StartTime = time.time()

	# save time of arrival
	while GPIO.input(echo_gpio) == 1:
		StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	dist = ((TimeElapsed * 34300) / 2 / 2.54)

	# If distance is beyond the range of this device,
	# consider it "invalid", and set it to "max. distance" (999)
	if (dist > 40):
		dist = 999

	return dist


def main():
	continuous=False
	for arg in sys.argv[1:]:
		#print arg
		if (arg == "-c"):
			continuous=True

	while (True):

		try:
			print
			for NAME,TRIG,ECHO in [ ["LEFT",GPIO_TRIGGER_L, GPIO_ECHO_L],\
				["FWD",GPIO_TRIGGER_F, GPIO_ECHO_F],\
				["RIGHT",GPIO_TRIGGER_R, GPIO_ECHO_R] ]:

				dist = distance(TRIG,ECHO)
				print ("%s - %d in" % (NAME,dist))

		# Reset by pressing CTRL + C
		except KeyboardInterrupt:
			print("\n\nMeasurement stopped by User")
			break

		if (not continuous):
			break


if __name__ == "__main__":
    main()
    GPIO.cleanup()
    print

