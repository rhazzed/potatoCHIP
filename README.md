# Raspberry Pi 3B+ code development for Derpa and Nimrod
  (We originally used a C.H.I.P. single board computer, so you may see remnants of that in the codebase...)

Both are tracked robots based on the OSEPP TANK-01 (https://www.digikey.com/en/products/detail/osepp-electronics-ltd/TANK-01/11198516).

This is a (mostly) Python codebase to get various things going with -- like a 16-channel I2C PWM controller board, Ultrasonic Range Sensors, LIDAR, IR, Laser range finders and more.

REQUIREMENTS -

     sudo pip install httpserver
     sudo apt-get install python3-numpy python3-matplotlib

     cd ~/potatoCHIP

     ./fixLidarOffset

     touch /dev/shm/lidar.png
     ln -s /dev/shm/lidar.png ./lidar.png

     touch /dev/shm/lidar.csv
     ln -s /dev/shm/lidar.csv ./lidar.csv


SEE "motd" FILE FOR STARTUP INSTRUCTIONS!


TO-DOs:
1) DON'T ground motor GND-OUT to PWM power-gnd-in!
2) Add left/right/fwd/back buttons to website
3) Reload "MyPins.py" every time a "START" command is issued
4) Modify plotLidar.py to DYNAMICALLY determine sensor coverages (for now it's hard-coded)
5) Modify obstacle-avoidance logic to be "turn, sense, go -or- turn-some-more" rather than just
   blindly turning "x" degrees 

Eric's Wishes:

1. Add the pan buttons to the CAM screen. Currently, can't watch cam and control it at the same time on mobile or tablet.  
2. For the same reasons as #1,  Start/Stop buttons on cam screen makes sense too.
