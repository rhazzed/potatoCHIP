#!/usr/bin/python
#############
# Python include file for Derpa
#############

#set GPIO pins for Ultrasonic Range Detector
GPIO_TRIGGER = 06
GPIO_ECHO = 05

#set GPIO for Tracks
GPIO_RFRONT = 19
GPIO_RREAR = 12
GPIO_LFRONT = 21
GPIO_LREAR = 20

#set PWM Controller channels
PWM_CH_RIGHT = 0
PWM_CH_LEFT = 2
PWM_CH_SERVO = 15

# REAL VALUES BELOW -
TRACK_FULL = 4095	# Full-power (100% "on") PWM to track motors
TRACK_HALF = 1900	# (Roughly) Half-power PWM to track motors
TRACK_SLOW = 1400	# (Roughly) Half-power PWM to track motors
TRACK_STOP = 0		# Power OFF (0% "on") PWM to track motors

# Configure min and max servo pulse lengths
#servo_min = 150  # Min pulse length out of 4096
servo_min = 250  # Min pulse length out of 4096
servo_max = 580  # Max pulse length out of 4096 (600 torqued one servo too much)

# Variable that approximates turning rate (seconds-per-degree)
#SECONDS_PER_DEGREE = 0.004166	# FULL SPEED
SECONDS_PER_DEGREE = 0.0055833	# HALF SPEED
