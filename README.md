# Raspberry Pi 3B+ code development for Derpa and Nimrod
  (We originally used a C.H.I.P. single board computer, so you may see remnants of that in the codebase...)

Both are tracked robots based on the OSEPP TANK-01 (https://www.digikey.com/en/products/detail/osepp-electronics-ltd/TANK-01/11198516).

This is a (mostly) Python codebase to get various things going with -- like a 16-channel I2C PWM controller board, Ultrasonic Range Sensors, LIDAR, IR, Laser range finders and more.

REQUIREMENTS -

     pip install httpserver

SEE "motd" FILE FOR STARTUP INSTRUCTIONS!


TO-DOs:
1) DON'T ground motor GND-OUT to PWM power-gnd-in!
2) Add left/right/fwd/back buttons to website
3) Add camera pan controls to website
4) After reading CMD_FILE/RSP_FILE, clear it out
5) Modify website to show current sensor readings
6) Reload "MyPins.py" every time a "START" command is issued
7) Modify obstacle-avoidance logic to be "turn, sense, go -or- turn-some-more" rather than just
   blindly turning "x" degrees 
