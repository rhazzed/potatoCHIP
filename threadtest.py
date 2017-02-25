#!/usr/bin/python
##################################
from __future__ import division
from threading import Thread
import time
# Import the PCA9685 16-channel I2C PWM module.
import Adafruit_PCA9685 as PWM
# Import the GPIO library
import CHIP_IO.GPIO as GPIO

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *



#set GPIO pin directions (IN / OUT) for Ultrasonic Range Detector
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#set GPIO pin directions (IN / OUT) for Tracks
GPIO.setup(GPIO_RFRONT, GPIO.OUT)
GPIO.setup(GPIO_RREAR, GPIO.OUT)
GPIO.setup(GPIO_LFRONT, GPIO.OUT)
GPIO.setup(GPIO_LREAR, GPIO.OUT)

range = 999	# Global variable that holds the ultrasonic range
		# detector's latest distance measurement
run=1		# Global "keep going" variable. Set to "0" to stop
		# all threads (e.g. to shut down the program)



# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=2)

# Configure servo pulse lengths given (externall-defined) min and max
servo_step = ((servo_max - servo_min)/5)

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
    GPIO.output(GPIO_RFRONT, GPIO.HIGH)
    GPIO.output(GPIO_RREAR, GPIO.LOW)
    pwm.set_pwm(PWM_CH_RIGHT, 0, TRACK_FULL)

def right_backwards():
    # Make right track go BACKWARDS
    GPIO.output(GPIO_RFRONT, GPIO.LOW)
    GPIO.output(GPIO_RREAR, GPIO.HIGH)
    pwm.set_pwm(PWM_CH_RIGHT, 0, TRACK_FULL)

def left_forward():
    # Make left track go FORWARD
    GPIO.output(GPIO_LFRONT, GPIO.HIGH)
    GPIO.output(GPIO_LREAR, GPIO.LOW)
    pwm.set_pwm(PWM_CH_LEFT, 0, TRACK_FULL)

def left_backwards():
    # Make left track go BACKWARDS
    GPIO.output(GPIO_LFRONT, GPIO.LOW)
    GPIO.output(GPIO_LREAR, GPIO.HIGH)
    pwm.set_pwm(PWM_CH_LEFT, 0, TRACK_FULL)

def go_forward():
    right_forward()
    left_forward()

def go_backwards():
    right_backwards()
    left_backwards()

def stop_tracks():
    # Stop the left track
    pwm.set_pwm(PWM_CH_LEFT, 0, TRACK_STOP)
    GPIO.output(GPIO_LFRONT, GPIO.LOW)
    GPIO.output(GPIO_LREAR, GPIO.LOW)

    # Stop the right track
    pwm.set_pwm(PWM_CH_RIGHT, 0, TRACK_STOP)
    GPIO.output(GPIO_RFRONT, GPIO.LOW)
    GPIO.output(GPIO_RREAR, GPIO.LOW)




def thread1(threadname):

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    #global run
    while run:
        # display variable "range" modify by thread 2
        print range
        time.sleep(1)

def lookout(threadname):
    global range

    # Uncomment the following line if THIS THREAD
    # will need to modify the "run" variable. DO NOT
    # need to uncomment it to just READ it...
    #global run

    print('ULTRASONIC RANGE SENSOR SERVO MIN...')
    servo_pos = servo_min
    pwm.set_pwm(PWM_CH_SERVO, 0, servo_pos)


    # Make left track go BACKWARDS
    left_backwards()

    # Make right track go FORWARD
    right_forward()

    while run:

	# Settle the trigger to zero
	GPIO.output(GPIO_TRIGGER, GPIO.LOW)

	# Wait for trigger to settle
	time.sleep(0.25)

	# Send trigger pulse
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, GPIO.HIGH)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, GPIO.LOW)

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

	# Calculate new servo position
	servo_pos += servo_step
	if (servo_pos > servo_max):
		servo_pos = servo_min
	pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round(servo_pos)))

thread1 = Thread( target=thread1, args=("Thread-1", ) )
lookout = Thread( target=lookout, args=("Thread-2", ) )

thread1.start()
lookout.start()

try:
    raw_input('\n\t******** Press Enter to stop ********\n\n')
except KeyboardInterrupt:
    print("\n\n\t******** CAUTION: Next time press <Enter>! ********\n")

print("Stopping all threads...")
run=0

thread1.join()
lookout.join()

print("All threads stopped")

# Center the servo
pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round( servo_min + ((servo_max - servo_min)/2) )))
time.sleep(1)

stop_tracks()

print("Cleaning up GPIO...")
GPIO.cleanup()
print("Done")
