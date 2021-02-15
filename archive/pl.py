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
from PIL import Image, ImageDraw, ImageFont


# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *

filename = SENSOR_OUTPUT_DIR + "/lidar.png"
image = Image.new(mode="RGB", size=(500,500),color="white")
draw = ImageDraw.Draw(image)
fnt = ImageFont.truetype('Vera.ttf',12)


data = np.genfromtxt("lidar.csv", delimiter=",", names=["x", "y"])

# Degrees,sin,cos
maths = np.genfromtxt("angleToSinCos.csv", delimiter=",", names=["deg","sin","cos"])

##print("ORIG_X: %s\nORIG_Y: %s" % (data['x'],data['y']))

draw.text((250,250),"*",font=fnt,fill=(255,0,0))

new=data
for i in range(0,360):
	# Fake/draw a ring at max-distance for now...
	if data['y'][i] > 0 and data['y'][i] < 1300:

        	# Make 90 degrees "up"
		new['x'][i] = maths['cos'][90-i]*data['y'][i]
		new['y'][i] = maths['sin'][90-i]*data['y'][i]

		# Make a blue dot on the image at (x,y)
		draw.text(((new['x'][i]/7.42)+250, (new['y'][i]/-7.42)+250),"*",font=fnt,fill=(0,0,255))

#print("NEW__X: %s\nNEW__Y: %s" % (new['x'],new['y']))

image.save(filename)

##plt.scatter(new['x'],new['y'])

# Save to JPEG
##plt.savefig(SENSOR_OUTPUT_DIR + "/lidar.png", bbox_inches="tight")


