#!/usr/bin/python3
####################################################
# plotLidar.py - An attempt in Python3 to plot what the LIDAR sensor "sees"
#
# NOTE: YOU HAVE TO EXECUTE THIS COMMAND BEFORE THIS SCRIPT WILL WORK -
#
#    sudo apt-get install python3-numpy python3-matplotlib
#
# NOTE: YOU MUST use "ssh -X pi@192.168.x.y" to allow X-Forwarding through your ssh session
# NOTE: YOU MUST also be running an X-windows capable operating system (or use Xming for Winblows)
#
####################################################

import numpy as np
import matplotlib.pyplot as plt
import math

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *

data = np.genfromtxt("lidar.csv", delimiter=",", names=["x", "y"])

##print("ORIG_X: %s\nORIG_Y: %s" % (data['x'],data['y']))

new=data
for i in range(0,360):
	##new['x'][i] =  math.cos(math.radians(data['x'][i]))*data['y'][i]
	##new['y'][i] =  math.sin(math.radians(data['x'][i]))*data['y'][i]

	# Convert theta to radians
	new['x'][i] =  math.radians(data['x'][i])
	new['y'][i] =  data['y'][i]

##print("NEW__X: %s\nNEW__Y: %s" % (new['x'],new['y']))

ax = plt.subplot(111, projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)


# Establish max collision-avoidance value
max=FWD_THRESHOLD
if (SIDE_THRESHOLD > FWD_THRESHOLD):
	max=SIDE_THRESHOLD

# Show only what we are in danger of running into
#ax.set_ylim(0,(max*1.1))  # This seems to be a good "potential-collision", only view

# Give some reference beyond "danger close"
##ax.set_ylim(0,(max*11)) ##### THIS ONE SEEMS PERFECT for checking close-in
##ax.set_ylim(0,(max*5))
ax.set_ylim(0,(max*3))

# Playing around -
#ax.set_ylim(0,1000)
#ax.set_ylim(0,5000)

# Sensible "inside house" value for "long-range view" -
#ax.set_ylim(0,9000)

# LIDAR sensor max seems to be *AT* *LEAST* 16,000 mm (at night, outside, reflecting off cars)


# THE FOLLOWING SHOULD BE RIGHT CALCULATION, just need it in an array...
### (math.cos(math.radians(data['x']))*data['y'], math.sin(math.radians(data['x'])*data['y']))

##ax.scatter(data['x'],data['y'])
ax.scatter(new['x'],new['y'])

# Identify min thresholds being used
plt.title("Thresholds:\nSide: " + str(SIDE_THRESHOLD) + "\nFwd : " + str(FWD_THRESHOLD), pad=0.0, loc="left")

# Save to JPEG
plt.savefig(SENSOR_OUTPUT_DIR + "/lidar.png", bbox_inches="tight")

#plt.show()

