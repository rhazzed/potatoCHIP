#!/usr/bin/python
##################################
from __future__ import division
from threading import Thread
import time
# Import the PCA9685 16-channel I2C PWM module.
import Adafruit_PCA9685 as PWM
# Import the GPIO library
import CHIP_IO.GPIO as GPIO



#set GPIO pins for Ultrasonic Range Detector
GPIO_TRIGGER = "CSID0"
GPIO_ECHO = "CSID1"

#set GPIO for Tracks
GPIO_IN1 = "XIO-P2"
GPIO_IN2 = "XIO-P3"

#set GPIO pin directions (IN / OUT) for Ultrasonic Range Detector
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#set GPIO pin directions (IN / OUT) for Tracks
GPIO.setup(GPIO_IN1, GPIO.OUT)
GPIO.setup(GPIO_IN2, GPIO.OUT)

#set PWM Controller channels
PWM_CH_FNB = 0
PWM_CH_FNA = 2
PWM_CH_SERVO = 15


range = 999	# Global variable that holds the ultrasonic range
		# detector's latest distance measurement
run=1		# Global "keep going" variable. Set to "0" to stop
		# all threads (e.g. to shut down the program)



# Initialise the PCA9685 at the appropriate address and
# bus (0x40 and 2, respectively)
pwm = PWM.PCA9685(address=0x40, busnum=2)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 580  # Max pulse length out of 4096 (600 torqued one servo too much)
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


    # Make left track go FORWARD
    direction = GPIO.HIGH
    GPIO.output(GPIO_IN1, GPIO.HIGH)
    GPIO.output(GPIO_IN2, GPIO.LOW)

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
  time.sleep(100)
except KeyboardInterrupt:
  print("Stopping all threads...")
  run=0

thread1.join()
lookout.join()

print("All threads stopped")

# Center the servo
pwm.set_pwm(PWM_CH_SERVO, 0, (int)(round( servo_min + ((servo_max - servo_min)/2) )))
time.sleep(1)

# Stop the left track
GPIO.output(GPIO_IN1, GPIO.LOW)
GPIO.output(GPIO_IN2, GPIO.LOW)

print("Cleaning up GPIO...")
GPIO.cleanup()
print("Done")
