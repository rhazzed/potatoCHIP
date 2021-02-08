##############
# Python include file for Nimrod
##############

#set GPIO pins for Ultrasonic Range Detector
#    FRONT
GPIO_TRIGGER_F=6
GPIO_ECHO_F=7
#    LEFT
GPIO_TRIGGER_L=13
GPIO_ECHO_L=26
#    RIGHT
GPIO_TRIGGER_R=23
GPIO_ECHO_R=24

#set GPIO for Tracks
GPIO_RFRONT=12
GPIO_RREAR=19
GPIO_LFRONT=20
GPIO_LREAR=21

#set PWM Controller channels
PWM_CH_RIGHT=0
PWM_CH_LEFT=2
PWM_CH_SERVO=15

# REAL VALUES BELOW -
TRACK_FULL=4095	# Full-power (100% "on") PWM to track motors
TRACK_HALF=2200	# (Roughly) Half-power PWM to track motors
TRACK_SLOW=1400	# (Roughly) lower-power PWM to track motors
TRACK_STOP=0		# Power OFF (0% "on") PWM to track motors

# Configure min and max servo pulse lengths
#servo_min=150  # Min pulse length out of 4096
servo_min=270  # Min pulse length out of 4096
servo_max=500  # Max pulse length out of 4096 (600 torqued one servo too much)

# Variable that approximates turning rate (seconds-per-degree)
SECONDS_PER_DEGREE=0.010000	# 4166 FULL SPEED (Nimrod needs this for half-speed!?)
#SECONDS_PER_DEGREE=0.0055833	# HALF SPEED
#SECONDS_PER_DEGREE=0.0065833	# HALF SPEED

### LEFT
ULTRASONIC_MIN_DIST_L=15
#ULTRASONIC_MIN_DIST_L=14 # Nimrod got within 1/2" of wall (aka not sensitive enough)

### FRONT
ULTRASONIC_MIN_DIST_F=17
#ULTRASONIC_MIN_DIST_F=15

### RIGHT (default to using same as RIGHT)
ULTRASONIC_MIN_DIST_R=15

### LIDAR ANGLES
FWD_OFF_ANGLE=30   # 0 +/- this is considered "forward-looking"
MAX_OFF_ANGLE=45   # Beyond FWD_OFF_ANGLE and up to (this) is considered "right-" or "left-looking"

### LIDAR DISTANCES
### FYI -  LIDAR sensor max seems to be *AT* *LEAST* 16,000 mm / 52 feet (at night, outside, reflecting off cars)
FWD_THRESHOLD=450  # If there is nothing in front of the LIDAR closer than this value, it is safe to move forward
SIDE_THRESHOLD=400 # If there is something to the side of the LIDAR that is closer than this value, a turn is necessary!

# The "lidar compass-point" that aligns with the platform's (robot's) zero-degree-point
RH=0  # Set this to indicate your LIDAR's zero-degrees offset to your robot's zero-degrees point (aka its front)

# Exit codes used as direction-indicators from shell scripts
EXIT_DIR_UNKNOWN=0
EXIT_DIR_ERROR=1
EXIT_DIR_LEFT=2
EXIT_DIR_FWD=3
EXIT_DIR_RIGHT=4
EXIT_DIR_BACKUP_AND_TURN=100
EXIT_DIR_STUCK=124

# COMMAND-PASSING FILE -
# File to use to pass commands to the robot
CMD_FILE="/dev/shm/IN"
# File to use to retrieve responses from the robot
RSP_FILE="/dev/shm/OUT"

# Where to look for lidar-range values (*MUST* MATCH the directory used in "ultra_simple"!!!)
RANGE_DIR="/dev/shm"

# Where to look for sensor readings
SENSOR_OUTPUT_DIR="/dev/shm"

# Ultrasonic sensor suffixes
US_L="US_L"
US_F="US_F"
US_R="US_R"

# Lidar sensor suffixes
LI_L="LI_L"
LI_F="LI_F"
LI_R="LI_R"

# Where to put the "adjusted" compass files (*MUST* MATCH the dierctory used in fixLidarOffset!!!)
ADJUSTED_DIR="/home/pi/potatoCHIP/RANGE"

# INDIVIDUAL COMMANDS -
CMD_START="START"
CMD_STOP="STOP"
