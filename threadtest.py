#!/usr/bin/python
##################################
# threadtest.py - A script to try to merge all robot sensors into movement using multithreading under Python
#
# HISTORICAL INFORMATION -
#
#  2021-01-22  msipin  Added this header. Added another thread to process LIDAR data
##################################

from __future__ import division
from threading import Thread
import time
import subprocess
import os
from random import randrange

# Import the PCA9685 16-channel I2C PWM module.
import Adafruit_PCA9685 as PWM

# Import the GPIO library
## import CHIP_IO.GPIO as GPIO

import Adafruit_GPIO as gpio
GPIO = gpio.get_platform_gpio()


# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *



#set GPIO pin directions (IN / OUT) for Ultrasonic Range Detector
GPIO.setup(GPIO_TRIGGER, gpio.OUT)
GPIO.setup(GPIO_ECHO, gpio.IN)

#set GPIO pin directions (IN / OUT) for Tracks
GPIO.setup(GPIO_RFRONT, gpio.OUT)
GPIO.setup(GPIO_RREAR, gpio.OUT)
GPIO.setup(GPIO_LFRONT, gpio.OUT)
GPIO.setup(GPIO_LREAR, gpio.OUT)

range = 999	# Global variable that holds the ultrasonic range
		# detector's latest distance measurement

run=1		# Global "keep going" variable. Set to "0" to stop
		# all threads (e.g. to shut down the program)

# Return codes for the "lidarGo" program (script, actually) -
#    EXIT_DIR_UNKNOWN=0
#    EXIT_DIR_ERROR=1
#    EXIT_DIR_LEFT=2
#    EXIT_DIR_FWD=3
#    EXIT_DIR_RIGHT=4
#    EXIT_DIR_BACKUP_AND_TURN=100
#    EXIT_DIR_STUCK=124
lidar_dir=3

track_speed=TRACK_HALF	# Global variable to control how fast the tracks
#track_speed=TRACK_FULL  # Global variable to control how fast the tracks
#track_speed=TRACK_SLOW	# Global variable to control how fast the tracks
			# will spin when activated

NUM_STEPS = 5	# Number of servo steps to move Ultrasonic Range Detector in


# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=1)

# Configure servo pulse lengths given (externall-defined) min and max
servo_step = ((servo_max - servo_min)/NUM_STEPS)

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


######################
# UTILITY FUNCTIONS -
######################

def right_forward():
    # Make right track go FORWARD
    GPIO.output(GPIO_RFRONT, gpio.HIGH)
    GPIO.output(GPIO_RREAR, gpio.LOW)
    pwm.set_pwm(PWM_CH_RIGHT, 0, track_speed)

def right_backwards():
    # Make right track go BACKWARDS
    GPIO.output(GPIO_RFRONT, gpio.LOW)
    GPIO.output(GPIO_RREAR, gpio.HIGH)
    pwm.set_pwm(PWM_CH_RIGHT, 0, track_speed)

def left_forward():
    # Make left track go FORWARD
    GPIO.output(GPIO_LFRONT, gpio.HIGH)
    GPIO.output(GPIO_LREAR, gpio.LOW)
    pwm.set_pwm(PWM_CH_LEFT, 0, track_speed)

def left_backwards():
    # Make left track go BACKWARDS
    GPIO.output(GPIO_LFRONT, gpio.LOW)
    GPIO.output(GPIO_LREAR, gpio.HIGH)
    pwm.set_pwm(PWM_CH_LEFT, 0, track_speed)

def go_forward():
    right_forward()
    left_forward()

def go_backwards():
    right_backwards()
    left_backwards()

def stop_tracks():
    # Stop the left track
    pwm.set_pwm(PWM_CH_LEFT, 0, track_speed)
    GPIO.output(GPIO_LFRONT, gpio.LOW)
    GPIO.output(GPIO_LREAR, gpio.LOW)

    # Stop the right track
    pwm.set_pwm(PWM_CH_RIGHT, 0, track_speed)
    GPIO.output(GPIO_RFRONT, gpio.LOW)
    GPIO.output(GPIO_RREAR, gpio.LOW)

def turn_right(degrees):
    print("Turning right %d degrees\n" % degrees)
    left_forward()
    right_backwards()
    duration = (degrees*SECONDS_PER_DEGREE)
    print('Sleeping for {0} seconds'.format(duration))
    time.sleep(duration)
    stop_tracks()

def turn_left(degrees):
    print("Turning left %d degrees\n" % degrees)
    left_backwards()
    right_forward()
    duration = (degrees*SECONDS_PER_DEGREE)
    print('Sleeping for {0} seconds'.format(duration))
    time.sleep(duration)
    stop_tracks()

def backup_turn_random():
    degrees = randrange(10,39)
    print("Turning right %d degrees\n" % degrees)
    left_forward()
    right_backwards()
    duration = (degrees*SECONDS_PER_DEGREE)
    print('Sleeping for {0} seconds'.format(duration))
    time.sleep(duration)
    stop_tracks()




def lidar(threadname):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    #global run
    global lidar_dir
    while run:
        # Run LIDAR reader command and display its output
        p = subprocess.Popen(["lidarGo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = p.stdout.read()
        print out

        # Get return code from call
        # Wait until process terminates (without using p.wait())
        while p.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.25)

        lidar_dir = p.returncode
        print("LIDAR exit value: %d\n" % lidar_dir)

        # Just execute the command
        #os.system("lidarGo");

        time.sleep(1)


def ultrasonic(threadname):
    global range

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run
    #global lidar_dir

    print('ULTRASONIC RANGE SENSOR SERVO MIN...')
    servo_pos = servo_min
    servo_stop = 1
    pwm.set_pwm(PWM_CH_SERVO, 0, servo_pos)


    # Go FORWARD
    go_forward()

    while run:

	# Settle the trigger to zero
	GPIO.output(GPIO_TRIGGER, gpio.LOW)

	# Wait for trigger to settle
	time.sleep(0.25)

	# Send trigger pulse
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, gpio.HIGH)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, gpio.LOW)

	StartTime = time.time()
	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()

	StopTime = time.time()
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

	range = distance

        # display ultrasonic "range"
        print("ultrasonic: %d" % range)

        # Return codes for the "lidarGo" program (script, actually) -
        #    EXIT_DIR_UNKNOWN=0
        #    EXIT_DIR_ERROR=1
        #    EXIT_DIR_LEFT=2
        #    EXIT_DIR_FWD=3
        #    EXIT_DIR_RIGHT=4
        #    EXIT_DIR_BACKUP_AND_TURN=100
        #    EXIT_DIR_STUCK=124
        ultrasonic_dir = 3

	# If ultrasonic distance is "danger close", stop moving!
	if (range <= 15):
		print("\nUltrasonic sensor sees something in our path!\n")
		stop_tracks()
		ultrasonic_dir = 0

	# If lidar doesn't think we should keep going forward, stop moving!
	if (lidar_dir != 3):
		print("\nLidar sees something in our path! (%d)\n" % lidar_dir)
		stop_tracks()

        # If the ultrasonic sensor stopped us...
        if (range <= 15):
		# Use the current servo position to decide
		# whether to turn right or left
		if (servo_stop <= ((NUM_STEPS+1)/2)):
			ultrasonic_dir = 2
		else:
			ultrasonic_dir = 4

	# if ultrasonic RIGHT and (lidar FWD or lidar RIGHT)...
        if (ultrasonic_dir == 2 and (lidar_dir == 3 or lidar_dir == 2)):
		print("\t<<<<<<<< Turning LEFT  -----")
		turn_left(65)

	# if ultrasonic LEFT and (lidar FWD or lidar LEFT)...
        if (ultrasonic_dir == 4 and (lidar_dir == 3 or lidar_dir == 4)):
		print("\t----- Turning RIGHT >>>>>>>>")
		turn_right(65)

	# if ((ultrasonic RIGHT and lidar LEFT) or (ultrasonic LEFT and lidar RIGHT) or \
	#     (ultrasonic LEFT and lidar RIGHT) or (ultrasonic RIGHT and lidar LEFT))...
	if ((ultrasonic_dir == 4 and lidar_dir == 2) or (ultrasonic_dir == 2 and lidar_dir == 4) or (ultrasonic_dir == 2 and lidar_dir == 4) or (ultrasonic_dir == 4 and lidar_dir == 2)):
		print("\t----- B/U Random Turn ------")
		backup_turn_random()

	# If ultrasonic FWD
	if (ultrasonic_dir == 3):
		# if lidar RIGHT
		if (lidar_dir == 4):
			print("\t----- Turning RIGHT >>>>>>>>")
			turn_right(65)
		# else if lidar LEFT
		if (lidar_dir == 2):
			print("\t<<<<<<<< Turning LEFT  -----")
			turn_left(65)

	print("Done. Proceeding Forward!")
	go_forward()

	# Calculate new servo position
	servo_pos += servo_step
	servo_stop += 1
	if (servo_pos > servo_max):
		servo_pos = servo_min
		servo_stop = 1
	pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round(servo_pos)))

lidar = Thread( target=lidar, args=("Thread-1", ) )
ultrasonic = Thread( target=ultrasonic, args=("Thread-2", ) )

lidar.start()
ultrasonic.start()

try:
    raw_input('\n\t******** Press Enter to stop ********\n\n')
except KeyboardInterrupt:
    print("\n\n\t******** CAUTION: Next time press <Enter>! ********\n")

print("Stopping all threads...")
run=0

lidar.join()
ultrasonic.join()

print("All threads stopped")

# Center the servo
pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round( servo_min + ((servo_max - servo_min)/2) )))
time.sleep(1)

stop_tracks()

print("Cleaning up GPIO...")
GPIO.cleanup()
print("Done")
