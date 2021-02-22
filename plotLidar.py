#!/usr/bin/python3
####################################################
# plotLidar.py - An attempt in Python3 to plot what the LIDAR sensor "sees"
#
# NOTE: YOU HAVE TO EXECUTE THIS COMMAND BEFORE THIS SCRIPT WILL WORK -
#
#    sudo apt-get install python3-numpy python3-matplotlib
#
# NOTE: If you want to use the "plt.show()" command at the end of this file,
#       YOU MUST use "ssh -X pi@192.168.x.y" to allow X-Forwarding through your ssh session
#       YOU MUST also be running an X-windows capable operating system (or use Xming for Winblows)
#
#  2021-02-14  msipin  Sped things up a bit by only processing datapoints that will be shown on final plot
#  2021-02-22  msipin  Completely refactored. TOTALLY RELIANT on pre-computed "lidar.blank.png", and all
#                      current values for the LIDAR minimum thresholds (450/400mm, fron and sides,
#                      respectively). If ANY of those values changes, so must the "lidar.blank.png" file!
####################################################
from PIL import Image
import math
import numpy as np

# Import the pin definition (a symbolic link to MyPins.<RobotName>.py)
# for your particular robot -
from MyPins import *



def putpoint(arr,x,y,val):
    for i in range(-3,4):
        for ii in range(-3,4):
            arr[midx+x+i,midy+y+ii] = val
            arr[midx+x-i,midy+y+ii] = val

def plotAt(deg,dist,color):
    rad=math.radians(90-deg)
    xOffset = int(math.cos(rad)*dist*pixels_per_mm)
    yOffset = int(math.sin(rad)*dist*pixels_per_mm)
    #print("xOffset=%d  yOffset=%d" %(xOffset,yOffset))
    putpoint(pixelsNew,xOffset,-yOffset,color)



#print()

im1 = Image.open('lidar.blank.png')
#print("Image1 Mode: %s" % im1.mode)
#print("im1.size[0]: %d  im1.size[1]: %d" %(im1.size[0],im1.size[1]))
pixelMap1 = im1.load()

midx=int(im1.size[0]/2)+3
midy=int(im1.size[1]/2)+10
pixels_per_mm=137.4/1000

#print("midx=%d  midy=%d" % (midx,midy))

im3 = Image.new(im1.mode, im1.size)
pixelsNew = im3.load()
for i in range(im1.size[0]):
    for j in range(im1.size[1]):
        pixelsNew[i,j] = pixelMap1[i,j]



black = (0,0,0,255)
red = (255,0,0,255)
green = (0,255,0,255)
blue = (0,0,255,255)


# Put red cross on 0,0
plotAt(0,0,red)

# Put blue cross on 135 degrees, 1200mm
##plotAt(135,1200,blue)
# Put blue cross on 180 degrees, 1200mm
##plotAt(180,1200,blue)
# Try red cross at 45 deg, 600mm
##plotAt(45,600,red)


data = np.genfromtxt("lidar.csv", delimiter=",", names=["d", "r"])
# For each point in lidar.csv...
for i in range(0,360):
    if data['r'][i] > 0 and data['r'][i] < 1300:
        #print("DEG: %s  RANGE: %s" % (data['d'],data['r']))
        plotAt(data['d'][i],data['r'][i],blue)



#print("im3.size[0]: %d  im3.size[1]: %d" %(im3.size[0],im3.size[1]))
#im3.show()
im3.save(SENSOR_OUTPUT_DIR + "/lidar.png", bbox_inches="tight")
#print()
