#!/usr/bin/python
##################################
# threadtest.py - A script to try to merge all robot sensors into movement using multithreading under Python
#
# HISTORICAL INFORMATION -
#
#  2021-01-22  msipin  Added this header. Added another thread to process LIDAR data
#  2021-01-24  msipin  Changed definition for "main" ultrasonic sensor pins.
#  2021-01-25  msipin  Fixed missing lidar-backup case
#  2021-01-27  msipin  Added website integration (to pickup commands)
#  2021-01-29  msipin  Moved ultrasonic sensor readings to their own thread and spaced them out to avoid
#                      hearing eachother's "distant responses"
#  2021-02-04  msipin  Added a pause after making any turn to give sensors time to re-check their surroundings
#                      Improved debugging in ultrasonic sensor distance function. Truncated RSP_FILE on startup
#  2021-02-06  msipin  Increased allowable range of sensors (one spec says up to 500cm!). Also returned
#                      "max" when sensor doesn't pickup anything, to allow failover on bad reading
#  2021-02-06  msipin  Let each ultrasonic sensor have its own setting, and moved them to MyPins.*.py.
#                      Changed turns from 65 degrees to 15, per Nimrod "live testing"
#  2021-02-07  msipin  Hid the ultrasonic "direction indication" from other threads until final determination
#                      Made the ultrasonic and lidar range detector loops run faster
#  2021-02-09  msipin  Replaced robot's CMD_FILE with socket-based communications (had to adapt Python3 -vs- Python2
#                      object-serialization!!!)
##################################

from __future__ import division
from threading import Thread
import time
import subprocess
import os
from random import randrange
import sys, select
from multiprocessing.connection import Listener


# Import the PCA9685 16-channel I2C PWM module.
import Adafruit_PCA9685 as PWM

# Import the GPIO library
## import CHIP_IO.GPIO as GPIO

import Adafruit_GPIO as gpio
GPIO = gpio.get_platform_gpio()


# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *


#set GPIO pin directions (IN / OUT) for Ultrasonic Range Detectors
# LEFT -
GPIO.setup(GPIO_TRIGGER_L, gpio.OUT)
GPIO.setup(GPIO_ECHO_L, gpio.IN)
# FWD -
GPIO.setup(GPIO_TRIGGER_F, gpio.OUT)
GPIO.setup(GPIO_ECHO_F, gpio.IN)
# RIGHT -
GPIO.setup(GPIO_TRIGGER_R, gpio.OUT)
GPIO.setup(GPIO_ECHO_R, gpio.IN)

# Settle each trigger to zero
GPIO.output(GPIO_TRIGGER_L, False)
GPIO.output(GPIO_TRIGGER_F, False)
GPIO.output(GPIO_TRIGGER_R, False)


#set GPIO pin directions (IN / OUT) for Tracks
GPIO.setup(GPIO_RFRONT, gpio.OUT)
GPIO.setup(GPIO_RREAR, gpio.OUT)
GPIO.setup(GPIO_LFRONT, gpio.OUT)
GPIO.setup(GPIO_LREAR, gpio.OUT)



run=1		# Global "keep going" variable. Set to "0" to stop
		# all threads (e.g. to shut down the program)

lidar_dir = EXIT_DIR_FWD
ultrasonic_dir = EXIT_DIR_FWD

track_speed=TRACK_HALF	# Global variable to control how fast the tracks
#track_speed=TRACK_FULL  # Global variable to control how fast the tracks
#track_speed=TRACK_SLOW	# Global variable to control how fast the tracks
			# will spin when activated

#NUM_STEPS = 3	# Number of servo steps to move Ultrasonic Range Detector in


# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=1)

# Configure servo pulse lengths given (externall-defined) min and max
#servo_step = ((servo_max - servo_min)/NUM_STEPS)

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
    go_backwards()
    time.sleep(0.75)
    degrees = randrange(10,39)
    print("Turning right %d degrees\n" % degrees)
    left_forward()
    right_backwards()
    duration = (degrees*SECONDS_PER_DEGREE)
    print('Sleeping for {0} seconds'.format(duration))
    time.sleep(duration)
    stop_tracks()

def distance(trigger_gpio,echo_gpio):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run

    # Send trigger pulse
    # set Trigger to HIGH
    GPIO.output(trigger_gpio, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger_gpio, False)

    now = time.time()
    StartTime = now

    # save StartTime
    while run and GPIO.input(echo_gpio) == 0 and ((now - StartTime) < 0.1):
        now = time.time()
    #print("\t\tE.T. %02d StartTime: %0.4f" %  (trigger_gpio, (now - StartTime)))
    StartTime = now

    StopTime = now
    # save time of arrival
    while run and GPIO.input(echo_gpio) == 1 and ((now - StopTime) < 0.1):
        now = time.time()
    #print("\t\tE.T. %02d StopTime: %0.4f" %  (trigger_gpio, (now - StopTime)))
    StopTime = now

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    dist = ((TimeElapsed * 34300) / 2 / 2.54)

    # If distance is beyond the range of this device,
    # consider it "invalid", and set it to "max. distance" (999)
    if (dist > 120):
        dist = 999

    if (dist <= 0):
        dist = 999

    return dist



def lidar(threadname):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run
    global lidar_dir

    while run:
        # Run LIDAR reader command and display its output
        p = subprocess.Popen(["./lidarGo"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out = p.stdout.read()
        print out

        # Get return code from call
        # Wait until process terminates
        while p.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.05)

        lidar_dir = p.returncode
        print("LIDAR exit value: %d\n" % lidar_dir)

        time.sleep(0.1)

    run=0
    print("\n\t\t***Thread %s exiting." % threadname)


def _set_servo_position(servo_pos):
    pwm.set_pwm(PWM_CH_SERVO, 0, (int)(servo_pos))


def servo_left():
    print('SERVO LEFT...')
    servo_pos = int(servo_max)
    _set_servo_position(servo_pos)


def servo_forward():
    print('SERVO FWD...')
    servo_pos = int((servo_max - servo_min)/2)+servo_min
    _set_servo_position(servo_pos)


def servo_right():
    print('SERVO RIGHT...')
    servo_pos = int(servo_min)
    _set_servo_position(servo_pos)


def ultrasonic(threadname):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run
    global ultrasonic_dir

    # Local (aka "internal") direction-decision variable
    ultrasonic_decision = ultrasonic_dir

    # set ALL triggers to LOW
    GPIO.output(GPIO_TRIGGER_L, False)
    GPIO.output(GPIO_TRIGGER_F, False)
    GPIO.output(GPIO_TRIGGER_R, False)


    while run:

	# Ensure ultrasonic trigger has time to settle
	time.sleep(0.20)
	rangeF = distance(GPIO_TRIGGER_F, GPIO_ECHO_F)
	with open(SENSOR_OUTPUT_DIR + "/" + US_F, "w") as f2:
		f2.write(format(int(rangeF)))
		f2.write("\n")
		f2.close()

	# Ensure ultrasonic trigger has time to settle
	time.sleep(0.20)
	rangeL = distance(GPIO_TRIGGER_L, GPIO_ECHO_L)
	with open(SENSOR_OUTPUT_DIR + "/" + US_L, "w") as f2:
		f2.write(format(int(rangeL)))
		f2.write("\n")
		f2.close()

	# Ensure ultrasonic trigger has time to settle
	time.sleep(0.20)
	rangeR = distance(GPIO_TRIGGER_R, GPIO_ECHO_R)
	with open(SENSOR_OUTPUT_DIR + "/" + US_R, "w") as f2:
		f2.write(format(int(rangeR)))
		f2.write("\n")
		f2.close()

        # display ultrasonic "range"
        print("Left ultrasonic : %d" % rangeL)
        print("Front ultrasonic: %d" % rangeF)
        print("Right ultrasonic: %d" % rangeR)

        ultrasonic_decision = EXIT_DIR_FWD

	# If ultrasonic distance is "danger close", stop moving!
	if (rangeL <= ULTRASONIC_MIN_DIST_L or rangeF <= ULTRASONIC_MIN_DIST_F or rangeR <= ULTRASONIC_MIN_DIST_R):
		print("\nUltrasonic sensors see something in our path!\n")
		ultrasonic_decision = EXIT_DIR_UNKNOWN

        # If the ultrasonic sensor stopped us...
        if (ultrasonic_decision == EXIT_DIR_UNKNOWN):
		# If front sensor triggered, default to turning right (NOTE: Might get
		# overruled, below)
		if (rangeF <= ULTRASONIC_MIN_DIST_F):
			ultrasonic_decision = EXIT_DIR_RIGHT # RIGHT

		if (rangeL <= ULTRASONIC_MIN_DIST_L) and (rangeR > ULTRASONIC_MIN_DIST_R):
			ultrasonic_decision = EXIT_DIR_RIGHT # RIGHT

		if (rangeR <= ULTRASONIC_MIN_DIST_R) and (rangeL > ULTRASONIC_MIN_DIST_L):
			ultrasonic_decision = EXIT_DIR_LEFT # LEFT

		if (rangeL <= ULTRASONIC_MIN_DIST_L and rangeR <= ULTRASONIC_MIN_DIST_R):
			ultrasonic_decision = EXIT_DIR_BACKUP_AND_TURN # BACKUP AND TURN

        # Let the "outside world" know what our decision is
        ultrasonic_dir = ultrasonic_decision

	# Calculate new servo position
	#servo_pos += servo_step
	#servo_stop += 1
	#if (servo_pos > servo_max):
	#	servo_pos = servo_min
	#	servo_stop = 1
	#pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round(servo_pos)))

    run=0
    print("\n\t\t***Thread %s exiting." % threadname)





def tracks(threadname):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run
    global ultrasonic_dir
    global lidar_dir


    # WAIT for the run variable to be set to 2
    print("Thread %s waiting for signal to run..." % threadname)
    while run == 1:
        time.sleep(0.5)
    print("Thread %s done waiting..." % threadname)

    # Go FORWARD
    ##go_forward()

    while run:

	# If lidar doesn't think we should keep going forward, stop moving!
	if (lidar_dir != EXIT_DIR_FWD):
		print("\nLidar sees something in our path! (%d)\n" % lidar_dir)
		stop_tracks()

	# if ultrasonic RIGHT and (lidar FWD or lidar RIGHT)...
        if (ultrasonic_dir == EXIT_DIR_RIGHT and (lidar_dir == EXIT_DIR_FWD or lidar_dir == EXIT_DIR_RIGHT)):
		print("\t----- Turning RIGHT >>>>>>>>")
		turn_right(15)
		time.sleep(0.50) # Give sensors time to re-check their environment

	# if ultrasonic LEFT and (lidar FWD or lidar LEFT)...
        if (ultrasonic_dir == EXIT_DIR_LEFT and (lidar_dir == EXIT_DIR_FWD or lidar_dir == EXIT_DIR_LEFT)):
		print("\t<<<<<<<< Turning LEFT  -----")
		turn_left(15)
                time.sleep(0.50) # Give sensors time to re-check their environment

	# if ((ultrasonic RIGHT and lidar LEFT) or (ultrasonic LEFT and lidar RIGHT) or (ultrasonic BACKUP) or (lidar BACKUP))...
	if ((ultrasonic_dir == EXIT_DIR_LEFT and lidar_dir == EXIT_DIR_RIGHT) or (ultrasonic_dir == EXIT_DIR_RIGHT and lidar_dir == EXIT_DIR_LEFT) or (ultrasonic_dir == EXIT_DIR_BACKUP_AND_TURN) or (lidar_dir == EXIT_DIR_BACKUP_AND_TURN)):
		print("\t----- B/U Random Turn ------")
		backup_turn_random()
		time.sleep(0.50) # Give sensors time to re-check their environment

	# If ultrasonic FWD
	if (ultrasonic_dir == EXIT_DIR_FWD):
		# if lidar RIGHT
		if (lidar_dir == EXIT_DIR_RIGHT):
			print("\t----- Turning RIGHT >>>>>>>>")
			turn_right(15)
		        time.sleep(0.50) # Give sensors time to re-check their environment
		# else if lidar LEFT
		if (lidar_dir == EXIT_DIR_LEFT):
			print("\t<<<<<<<< Turning LEFT  -----")
			turn_left(15)
		        time.sleep(0.50) # Give sensors time to re-check their environment


	print("Done! Proceeding Forward!")
	go_forward()

    run=0
    print("\n\t\t***Thread %s exiting." % threadname)


def cmds(threadname):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run

    # Start the command-listener (socket on localhost)
    address = ('127.0.0.1', ROBOT_CMD_PORT)
    listener = Listener(address, authkey=ROBOT_SECRET_KEY)

    while run:
        try:
            conn = listener.accept()
            #print "RECEIVER accepted connection!"
            while conn is not None:
                try:
                    temp = conn.recv()
                    print("RECEIVED: %s" % temp)
                    for cmd in temp:

                        # Write cmd back to response-file
                        with open(RSP_FILE, "a") as f2:
                            f2.write(cmd)
                            f2.write("\n")
                            f2.close()

                        print("DEBUG: cmd = [%s]" % cmd)

                        if CMD_START in cmd and run == 1:
                            # Tell robot to go!
                            run = 2

                        if CMD_STOP in cmd:
                            # Tell all threads to stop!
                            run = 0
                            # Close the connection from the current user
                            conn.close()
                            conn = None

                        if CMD_CAMERA_LEFT in cmd:
                            # Turn camera servo LEFT
                            servo_left()


                        if CMD_CAMERA_FORWARD in cmd:
                            # Turn camera servo FORWARD
                            servo_forward()


                        if CMD_CAMERA_RIGHT in cmd:
                            # Turn camera servo RIGHT
                            servo_right()

                except EOFError:
                    # Close the connection from the (now-non-existent!) user
                    conn.close()
                    conn = None

                time.sleep(0.25)

        except IOError:
            # File doesn't exist
            True

        except IOError:
            # No instructions in file
            True

    run=0

    # Close this thread's socket/listener
    listener.close()
    print("\n\t\t***Thread %s exiting." % threadname)


def kybd(threadname):
    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    global run

    if not sys.stdin.isatty():
        print("\n\t\t***Thread %s thinks no kybd is present! Self-looping" % threadname)
        while (run):
            time.sleep(1)
    else:
        print('\n\t******** Press Enter to stop ********\n\n')
        while run:
            i, o, e = select.select( [sys.stdin], [], [], 1)
            if (len(i)>0):
                # User typed something!
                run=0
            else:
                # Nothing typed
                True

    run=0
    print("Stopping all threads...")

    print("\n\t\t***Thread %s exiting." % threadname)



# Initialize the "robot response file"
open(RSP_FILE, "w").close()


# Point the servo forward (WAS: ultrasonic sensor. NOW IS: Camera)
servo_forward()
time.sleep(1)


lidar = Thread( target=lidar, args=("lidar_thread", ) )
ultrasonic = Thread( target=ultrasonic, args=("ultrasonic_thread", ) )
cmds = Thread( target=cmds, args=("cmds_thread", ) )
# Mark cmds thread as a "daemon", so it won't stop us from exiting
cmds.daemon = True
kybd = Thread( target=kybd, args=("kybd_thread", ) )
tracks = Thread( target=tracks, args=("tracks_thread", ) )

lidar.start()
ultrasonic.start()
cmds.start()
kybd.start()
tracks.start()

while run:
    time.sleep(1)

print("Stopping all threads...")
run=0

lidar.join()
ultrasonic.join()
# Since cmds is a daemon, try to stop it "nicely", but give up if it's stuck on an accept() call to "no one"
cmds.join(2)
if cmds.is_alive():
    print("\n\t\t***Thread (cmds) is stuck/blocking. Exiting anyway!")
# At this point, if we try to exit, cmds will get killed anyway...
kybd.join()
tracks.join()

print("All threads stopped")

# Center the servo
servo_forward()
time.sleep(1)

stop_tracks()

print("Cleaning up GPIO...")
GPIO.cleanup()
print("\n\t\t***Main thread done!\nProgram exiting!")

