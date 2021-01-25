#!/bin/sh
############################
# moveclaw.sh - Move the 3D printed claw open and shut repeatedly.
############################

# Settings for original claw I printed (uses Micro SG90 servo) -
#MAX_OPEN=370
#HOLD_OPEN=360
#MAX_CLOSE=110
#HOLD_CLOSE=125

# Settings for second claw I printed (uses "regular" Futaba servo) -
MAX_OPEN=185
HOLD_OPEN=190
MAX_CLOSE=335
HOLD_CLOSE=330

while [ 1 ]
do
	# Open
	echo "OPENING -"
	python makex.py ${MAX_OPEN};python makex.py ${HOLD_OPEN}
	echo "NOW IN OPEN POSITION"
	sleep 1
	# Close
	echo
	echo "Closing -"
	python makex.py ${MAX_CLOSE};python makex.py ${HOLD_CLOSE}
	echo "NOW IN CLOSED POSITION"
	sleep 1
done

exit 0
