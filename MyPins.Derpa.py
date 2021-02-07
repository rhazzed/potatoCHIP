#############
# Python include file for Derpa
#############

#set GPIO pins for Ultrasonic Range Detector
#    FRONT
GPIO_TRIGGER_F = 6
GPIO_ECHO_F = 5
#    LEFT
GPIO_TRIGGER_L = 13
GPIO_ECHO_L = 26
#    RIGHT
GPIO_TRIGGER_R = 23
GPIO_ECHO_R = 24

#set GPIO for Tracks
GPIO_RFRONT = 12
GPIO_RREAR = 19
GPIO_LFRONT = 20
GPIO_LREAR = 21

#set PWM Controller channels
PWM_CH_RIGHT = 0
PWM_CH_LEFT = 2
PWM_CH_SERVO = 15

# REAL VALUES BELOW -
TRACK_FULL = 4095	# Full-power (100% "on") PWM to track motors
TRACK_HALF = 1900	# (Roughly) Half-power PWM to track motors
TRACK_SLOW = 1400	# Minimum-power PWM to track motors
TRACK_STOP = 0		# Power OFF (0% "on") PWM to track motors

# Configure min and max servo pulse lengths
servo_min = 250  # Min pulse length out of 4096 (Max CW/Right)
#servo_max = 520  # Max pulse length out of 4096 (600 torqued one servo too much)
servo_max = 520  # Max pulse length out of 4096 (Max CCW/Left) (600 torqued one servo too much)

# Variable that approximates turning rate (seconds-per-degree)
#SECONDS_PER_DEGREE = 0.004166	# FULL SPEED
#SECONDS_PER_DEGREE = 0.0055833	# HALF SPEED - On A/C mains power
SECONDS_PER_DEGREE = 0.0070000	# HALF SPEED - Derpa, with fresh 6xAA batts
#SECONDS_PER_DEGREE = 0.0100000	# HALF SPEED - Derpa, when 6xAA are weak
#SECONDS_PER_DEGREE = 0.01674990# HALF SPEED - Seemed to work on 6xAAs before "ground problem"
#SECONDS_PER_DEGREE = 0.0240     # HALF SPEED - Derpa with 6xAA NiHM Amazon Basics 2000mah batteries


# COMMAND-PASSING FILE -
# File to use to pass commands to the robot
CMD_FILE="/dev/shm/IN"
# File to use to retrieve responses from the robot
RSP_FILE="/dev/shm/OUT"

# INDIVIDUAL COMMANDS -
CMD_START="START"
CMD_STOP="STOP"
