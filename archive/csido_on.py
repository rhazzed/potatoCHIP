#
import CHIP_IO.GPIO as GPIO

GPIO.setup("CSID0", GPIO.OUT)   #set CSID0 as an output
GPIO.output("CSID0", GPIO.HIGH)
#GPIO.output("CSID0", GPIO.LOW)

