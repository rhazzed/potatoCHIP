#!/usr/bin/python
##################################
# getrange.py - Get distance reading from ultrasonic range detector
#               on GPIO pins GPIO_TRIGGER and GPIO_ECHO
#
# HISTORICAL INFORMATION -
#
#  2016-xx-xx  Eric/Mike  Created for Raspberry pi
#  2017-02-04  msipin  Adapted to C.H.I.P. by replacing GPIO library,
#                      editing pins and adding "settling time" before
#                      the ultrasonic sensor is triggered.
##################################

#Libraries
import CHIP_IO.GPIO as GPIO
import time
import sys


#set GPIO Pins
GPIO_TRIGGER = "CSID0"
GPIO_ECHO = "CSID1"

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():

	# Settle the trigger to zero
	GPIO.output(GPIO_TRIGGER, False)

	# Wait for trigger to settle
	time.sleep(0.25)

	# Send trigger pulse
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()

	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = ((TimeElapsed * 34300) / 2 / 2.54)

	# If distance is beyond the range of this device,
	# consider it "invalid", and set it to "max. distance" (999)
	if (distance > 40):
		distance = 999

	return distance


def main():
	try:
		continuous=False
		for arg in sys.argv[1:]:
			#print arg
			if (arg == "-c"):
				continuous=True

		while continuous:
			dist = distance()
			print ("%d in" % dist)
			#time.sleep(1)

		dist = distance()
		print ("%d in" % dist)
		#time.sleep(1)
		GPIO.cleanup()

		# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		GPIO.cleanup()


if __name__ == "__main__":
    main()
