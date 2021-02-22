#!/usr/bin/python3
####################################################
# plotBlank.py - Generate a "blank" LIDAR plot
#
#  2021-02-22  msipin  Derived from current "plotLidar.py"
####################################################

import numpy as np
import matplotlib.pyplot as plt
import math

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *


# Establish max collision-avoidance value
max=FWD_THRESHOLD
if (SIDE_THRESHOLD > FWD_THRESHOLD):
	max=SIDE_THRESHOLD


# LIDAR sensor max seems to be *AT* *LEAST* 16,000 mm (at night, outside, reflecting off cars)
#ylim=max*1.1  # This seems to be a good "potential-collision", only view
#ylim=max*11 ##### THIS ONE SEEMS PERFECT for checking close-in
#ylim=max*5
#ylim=max*2
# Playing around -
#ylim=1000
#ylim=5000
# Sensible "inside house" value for "long-range view" -
#ylim=9000
# Good context, not too much processing -
ylim=max*3

ax = plt.subplot(111, projection='polar')
ax.set_ylim(0,ylim)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
#data = np.genfromtxt("lidar.csv", delimiter=",", names=["x", "y"])
data = np.genfromtxt("lidar.blank.csv", delimiter=",", names=["x", "y"])

num=0
for i in range(0,360):
	if data['y'][i] < ylim:
		# Convert theta to radians
		data['x'][num] =  math.radians(data['x'][i])
		data['y'][num] =  data['y'][i]
		num=num+1

data=data[:num]
ax.scatter(data['x'],data['y'])

# Identify min thresholds being used
plt.title("Thresholds:\nFwd : " + str(FWD_THRESHOLD) + "\nSide: " + str(SIDE_THRESHOLD), pad=0.0, loc="left")

# Added collision ring(s) to plot
## START ANGLE, RADIUS

##     FWD_OFF_ANGLE=15   # 0 +/- this is considered "forward-looking"
##     MAX_OFF_ANGLE=45   # Beyond FWD_OFF_ANGLE and up to (this) is considered "right-" or "left-looking"


ax.plot(np.linspace(0                                  , 2*np.pi*(FWD_OFF_ANGLE/360)                , 100), np.ones(100)*FWD_THRESHOLD, color='r', linestyle='-')

ax.plot(np.linspace(0+2*np.pi*(FWD_OFF_ANGLE/360)      , 2*np.pi*(MAX_OFF_ANGLE/360)                , 100), np.ones(100)*SIDE_THRESHOLD, color='r', linestyle='-')
ax.plot(np.linspace(0+2*np.pi*((300+FWD_OFF_ANGLE)/360) , 2*np.pi*((300+MAX_OFF_ANGLE)/360)         , 100), np.ones(100)*SIDE_THRESHOLD, color='r', linestyle='-')

ax.plot(np.linspace(0+2*np.pi*((315+MAX_OFF_ANGLE)/360) , 2*np.pi*( 345               /360)         , 100), np.ones(100)*FWD_THRESHOLD, color='r', linestyle='-')


# Save to JPEG
#plt.savefig(SENSOR_OUTPUT_DIR + "/lidar.png", bbox_inches="tight")
plt.savefig("./lidar.blank.png", bbox_inches="tight")

#plt.show()

