#!/bin/sh
############################################################
# robot - A shell script to launch the executable(s) that it takes to run the Nimrod/Derpa robot
#
# HISTORICAL INFORMATION -
#
#  2021-01-29  msipin  Created
############################################################

CONTINUOUS=1    # Uncomment this to keep restarting the robot-logic exe if it ever crashes
#CONTINUOUS=0    # Uncomment this to only run the robot-logic exe *ONCE*


# File to use to pass commands to the robot (NOTE: *MUST* MATCH the file used in MyPins.py, threadtest.py, etc!)
CMD_FILE="/dev/shm/IN"

EXE_DIR=/home/pi/potatoCHIP

cd ${EXE_DIR}

while [ 1 ]
do
	sudo rm -f ${CMD_FILE}
	python ${EXE_DIR}/threadtest.py

	if [ ""$CONTINUOUS"" -ne 1 ]
	then
		break;
	fi
done


#    # Watch you robot's livestream video (OPTIONAL) -
#    *) start web browser
#    *) go to http://192.168.x.y:8000 (put your IP in x.y)
#        (NOTE: This only works if you've already started the livestream video webserver (above))

#    # Control your robot over the web interface -
#    *) start web browser
#    *) go to http://192.168.x.y:8080 (put your IP in x.y)
#    *) click on the start robot link
#    *) Enjoy robot!
#    *) click on the stop robot link
#    *) Once you click the stop link, you'll have to restart the robot-control executable (above)

exit 0

