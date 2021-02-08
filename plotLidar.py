#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import math


'''
r =  np.genfromtxt('lidar.csv',delimiter=',')
#data is a list of 360 data points taken at each 1 degree increment
theta = np.linspace(0, 2 * np.pi, 360)

ax = plt.subplot(111, projection='polar')
ax.plot(theta, r)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
#ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
ax.grid(True)

ax.set_title("Polar", va='bottom')
'''

data = np.genfromtxt("lidar.csv", delimiter=",", names=["x", "y"])

#new = data
print("ORIG_X: %s\nORIG_Y: %s" % (data['x'],data['y']))

new=data
for i in range(0,360):
	new['x'][i] =  math.cos(math.radians(data['x'][i]))*data['y'][i]
	new['y'][i] =  math.sin(math.radians(data['x'][i]))*data['y'][i]

print("NEW__X: %s\nNEW__Y: %s" % (new['x'],new['y']))

#plt.scatter(np.sin(data['x']), 9999-data['y'])
#plt.scatter(np.sin(data['x']), math.hypot(data['x'], data['y']))

#plt.plot(np.sin(data['x']), (9999-data['y']*np.sin(data['x'])))
#plt.plot(np.sin(data['x']), data['y']*np.sin(data['x']), linestyle='None', markersize = 10.0)

#plt.scatter(data['x'], 9999-data['y'])

ax = plt.subplot(111, projection='polar')
ax.set_theta_zero_location('W')
ax.set_theta_direction(-1)

# ax.scatter(data['x'], 9999-data['y'])
#plt.scatter(new['x'], 9999-new['y'])
#ax.scatter(data['x'],new['y'])

#plt.scatter(new['x'],new['y'])
ax.scatter(data['x'],data['y'])

# THE FOLLOWING SHOULD BE RIGHT CALCULATION, just need to put it into array somehow...
### ax.scatter(math.cos(math.radians(data['x']))*data['y'], math.sin(math.radians(data['x'])*data['y']))




plt.show()
