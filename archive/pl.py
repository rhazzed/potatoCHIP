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

print("ORIG_X: %s\nORIG_Y: %s" % (data['x'],data['y']))

new=data
for i in range(0,360):
	##new['x'][i] =  math.cos(math.radians(data['x'][i]))*data['y'][i]
	##new['y'][i] =  math.sin(math.radians(data['x'][i]))*data['y'][i]

	# Convert theta to radians
	theta =  math.radians(data['x'][i])

	###new['x'][i] =  math.radians(data['x'][i])
	###new['y'][i] =  data['y'][i]

	if data['y'][i] == 9999:
		new['x'][i] = 0
		new['y'][i] = 0
	else:
		new['x'][i] = math.cos(theta)*data['y'][i]
		new['y'][i] = math.sin(theta)*data['y'][i]

print("NEW__X: %s\nNEW__Y: %s" % (new['x'],new['y']))


# THE FOLLOWING SHOULD BE RIGHT CALCULATION, just need it in an array...
##plt.scatter(math.cos(data['x'])*data['y'], math.sin(data['x']*data['y']))

##plt.scatter(data['x'],data['y'])
plt.scatter(new['x'],new['y'])

plt.show()

