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


#new = data
##print("ORIG_X: %s\nORIG_Y: %s" % (data['x'],data['y']))

data = np.genfromtxt("lidar.csv", delimiter=",", names=["x", "y"])

new=data
for i in range(0,360):
	new['x'][i] =  math.cos(math.radians(data['x'][i]))*data['y'][i]
	new['y'][i] =  math.sin(math.radians(data['x'][i]))*data['y'][i]

##print("NEW__X: %s\nNEW__Y: %s" % (new['x'],new['y']))

#plt.scatter(np.sin(data['x']), 9999-data['y'])
#plt.scatter(np.sin(data['x']), math.hypot(data['x'], data['y']))

#plt.plot(np.sin(data['x']), (9999-data['y']*np.sin(data['x'])))
#plt.plot(np.sin(data['x']), data['y']*np.sin(data['x']), linestyle='None', markersize = 10.0)

#plt.scatter(data['x'], 9999-data['y'])

ax = plt.subplot(111, projection='polar')
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

# ax.scatter(data['x'], 9999-data['y'])
#plt.scatter(new['x'], 9999-new['y'])
#ax.scatter(data['x'],new['y'])

#plt.scatter(new['x'],new['y'])
ax.scatter(data['x'],data['y'])

# THE FOLLOWING SHOULD BE RIGHT CALCULATION, just need to put it into array somehow...
### ax.scatter(math.cos(math.radians(data['x']))*data['y'], math.sin(math.radians(data['x'])*data['y']))

plt.show()

