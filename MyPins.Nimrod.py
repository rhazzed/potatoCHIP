#!/usr/bin/python
#############
# Python include file for Derpa
#############

#set GPIO pins for Ultrasonic Range Detector
GPIO_TRIGGER = "CSID0"
GPIO_ECHO = "CSID1"

#set GPIO for Tracks
GPIO_RFRONT = "XIO-P3"
GPIO_RREAR = "XIO-P2"
GPIO_LFRONT = "XIO-P1"
GPIO_LREAR = "XIO-P0"

#set PWM Controller channels
PWM_CH_RIGHT = 2
PWM_CH_LEFT = 0
PWM_CH_SERVO = 15

# REAL VALUES BELOW -
TRACK_FULL = 4095	# Full-power (100% "on") PWM to track motors
TRACK_STOP = 0		# Power OFF (0% "on") PWM to track motors

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 580  # Max pulse length out of 4096 (600 torqued one servo too much)

