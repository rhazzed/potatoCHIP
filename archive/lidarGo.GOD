#!/bin/sh
##########################################
# lidarGo - A quick shell script to see if the robot should go straight, turn left or turn right.
#           Nothing more than a P.O.C. to test the usefulness of the LIDAR as an obstacle-avoidance
#           tool.
#
#  NOTE: This program *requires* that you have the "ultra_simple" program running in the background!
#
# HISTORICAL INFORMATION -
#
#  2021-01-22  msipin  Created
#  2021-01-23  msipin  Changed LIDAR threshold from 200 to 350 to give robot more time to react to obstacles.
##########################################

# Where to look for range values (*MUST* MATCH the directory used in "ultra_simple"!!!)
RANGE_DIR=/dev/shm

# Where to put the "adjusted" compass files (*MUST* MATCH the dierctory used in fixLidarOffset!!!)
ADJUSTED_DIR=/home/pi/potatoCHIP/RANGE

# IF YOU ARE USING ADJUSTED COMPASS FILES, UNCOMMENT THE FOLLOWING LINE ---
RANGE_DIR=$ADJUSTED_DIR		# Use "adjusted" compass points, not the "actual" Lidar compass points


########################################
# Robot-specific values START here
########################################
########################################

FWD_OFF_ANGLE=30   # 0 +/- this is considered "forward-looking"
FWD_THRESHOLD=350  # If there is nothing in front of the LIDAR closer than this value, it is safe to move forward

MAX_OFF_ANGLE=45   # Beyond FWD_OFF_ANGLE and up to (this) is considered "right-" or "left-looking"
SIDE_THRESHOLD=350 # If there is something to the side of the LIDAR that is closer than this value, a turn is necessary!

########################################
########################################
# Robot-specific values END here
########################################

# Number of files to examine between FRONT and LEFT/RIGHT
NUM_FILES=`expr $MAX_OFF_ANGLE - $FWD_OFF_ANGLE`
echo
#echo
#echo "DEBUG: NUM_FILES=$NUM_FILES"
##exit 2
echo



# Constants that could be returned upon exit
EXIT_DIR_UNKNOWN=0
EXIT_DIR_ERROR=1
EXIT_DIR_LEFT=2
EXIT_DIR_FWD=3
EXIT_DIR_RIGHT=4
EXIT_DIR_BACKUP_AND_TURN=100
EXIT_DIR_STUCK=124

# Default to throwing an error
DIRECTION=$EXIT_DIR_ERROR


# Function to compute average range from a selection of files
get_avg() {

grep -v "\-1" $* | awk 'BEGIN { count=0; val=0; }{
   split($1,arr,":")
   #printf("\tDEBUG: File: %s  Val: %s\n",arr[1],arr[2]);
   count++;
   val+=int(arr[2]);
} END {
   printf("%0d",int(val/count));
}'

}

# Function to find minimum range from a selection of files
get_min() {

grep -v "\-1" $* | awk 'BEGIN { min=999999; }{
   split($1,arr,":")
   #printf("\tDEBUG: File: %s  Val: %s\n",arr[1],arr[2]);
   if ((arr[2] >= 0) && (arr[2] < min)) {
      min = arr[2];
   }
} END {
   printf("%0d",min);
}'

}

# 1) Average out the valid (-MAX_OFF_ANGLE --to-- -FWD_OF_ANGLE) valid LIDAR distance-sensor readings and call this the "left value"
files=`ls ${RANGE_DIR}/[0-9][0-9][0-9] | tail -${FWD_OFF_ANGLE} | head -$NUM_FILES`
left_val=`get_min $files`

echo "DEBUG: left_val  = $left_val"
##exit 2



# 2) Average out the valid (-FWD_OFF_ANGLE --to-- +FWD_OFF_ANGLE) valid LIDAR distance-sensor readings, and call this the "forward value"
files1=`ls ${RANGE_DIR}/[0-9][0-9][0-9] | head -${FWD_OFF_ANGLE}`
files2=`ls ${RANGE_DIR}/[0-9][0-9][0-9] | tail -${FWD_OFF_ANGLE}`
files=`echo $files1 $files2`
fwd_val=`get_min $files`

echo "DEBUG: fwd_val   = $fwd_val"
##exit 2



# 3) Average out the valid (+FWD_OFF_ANGLE --to-- +MAX_OF_ANGLE) valid LIDAR distance-sensor readings and call this the "right value"
files=`ls ${RANGE_DIR}/[0-9][0-9][0-9] | head -${MAX_OFF_ANGLE} | tail -$NUM_FILES`
right_val=`get_min $files`

echo "DEBUG: right_val = $right_val"
##exit 2
echo



# 4) If either "left value" or "right value" is closer than SIDE_THRESHOLD...
if [ ""$left_val"" -le $SIDE_THRESHOLD -o ""$right_val"" -le $SIDE_THRESHOLD ]
then
	echo "SOMETHING ON LEFT or RIGHT "


#    5a) If "left value" *AND* "right value" are closer than SIDE_THRESHOLD...
	if [ ""$left_val"" -le $SIDE_THRESHOLD -a ""$right_val"" -le $SIDE_THRESHOLD ]
	then
		echo "SOMETHING ON *BOTH* LEFT *AND* RIGHT "
#       6a) Backup a bit and turn (randomly left or right)
		echo "Need to BACK OUT"
		DIRECTION=$EXIT_DIR_BACKUP_AND_TURN
	else

#    5b) If "left value" is lower than (or equal-to) "right value"...
		if [ ""$left_val"" -le ""$right_val"" ]
		then
#       6b) Turn right
			echo "Need to turn RIGHT"
			DIRECTION=$EXIT_DIR_RIGHT
		else

#    5c) If "right value" is lower than (only!) "left value"...
			if [ ""$right_val"" -lt ""$left_val"" ]
			then
#       6c) Turn left
				echo "Need to turn LEFT"
				DIRECTION=$EXIT_DIR_LEFT
			else
				echo "STUCK 1"
				DIRECTION=$EXIT_DIR_STUCK
			fi
		fi
	fi
else
# 7) If "forward value" is greater than FWD_THRESHOLD...
	if [ ""$fwd_val"" -gt $FWD_THRESHOLD ]
	then
# 8a) It is safe to move forward
		echo "Can MOVE FORWARD"
		DIRECTION=$EXIT_DIR_FWD
	else
# 8b) Make a turn...
		if [ ""$right_val"" -le ""$left_val"" ]
		then
			echo "Turn LEFT"
			DIRECTION=$EXIT_DIR_LEFT
		else
			echo "Turn RIGHT"
			DIRECTION=$EXIT_DIR_RIGHT
		fi
	fi
fi

exit $DIRECTION


#######################################
TEST RESULTS -

DEBUG: fwd_val = 193	# CAN NOT GO FWD
DEBUG: NUM_FILES=15
DEBUG: right_val = 563  # can go LEFT
DEBUG: left_val = 220   # can go RIGHT
			## SHOULD go LEFT
STUCK 2

