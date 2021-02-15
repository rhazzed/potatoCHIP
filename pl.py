#!/usr/bin/python3
####################################################
# pl.py - An EXPERIMENTAL version of plotLidar.py
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

# Degrees,sin,cos
maths = np.genfromtxt("angleToSinCos.csv", delimiter=",", names=["deg","sin","cos"])

#                               print("ORIG_X: %s\nORIG_Y: %s" % (data['x'],data['y']))

new=data
for i in range(0,360):
	# Fake/draw a ring at max-distance for now...
	if data['y'][i] > 4500:
		data['y'][i] = 4500

        # Make 90 degrees "up"
	new['x'][i] = maths['cos'][90-i]*data['y'][i]
	new['y'][i] = maths['sin'][90-i]*data['y'][i]

#                               print("NEW__X: %s\nNEW__Y: %s" % (new['x'],new['y']))


plt.scatter(new['x'],new['y'])

# Save to JPEG
plt.savefig(SENSOR_OUTPUT_DIR + "/lidar.png", bbox_inches="tight")

##plt.show()

