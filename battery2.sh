#!/bin/sh
# This program gets the battery info from PMU 
# Voltage and current charging/discharging
#
# Note : temperature can be more than ambient
# because of self-heating
#######################################################################
# Copyright (c) 2014 by RzBo, Bellesserre, France
#
# Permission is granted to use the source code 
# within this file in whole or in part for any 
# use, personal or commercial, without 
# restriction or limitation.
#
# No warranties, either explicit or implied, are 
# made as to the suitability of this code for any 
# purpose. Use at your own risk.
#######################################################################
# force ADC enable for battery voltage and 
# current
i2cset -y -f 0 0x34 0x82 0xC3
################################
#read Power status register @00h
POWER_STATUS=$(i2cget -y -f 0 0x34 0x00)
POWER_STATUS2=$(($POWER_STATUS))
##echo $POWER_STATUS
##echo $POWER_STATUS2
BAT_STATUS=$(($(($POWER_STATUS&0x02))/2)) # divide by 2 is like shifting rigth 1 times
#echo $(($POWER_STATUS&0x02))
#echo "BAT_STATUS="$BAT_STATUS
# echo $BAT_STATUS
echo ""
################################
#read Power OPERATING MODE register @01h
POWER_OP_MODE=$(i2cget -y -f 0 0x34 0x01)
POWER_OP_MODE2=$(($POWER_OP_MODE))
##echo $POWER_OP_MODE
##echo $POWER_OP_MODE2

if [ $POWER_STATUS2 = "1" ]; then
echo "Charger plugged in: No"
else
echo "Charger plugged in: Yes"
fi

BAT_EXIST=$(($(($POWER_OP_MODE&0x20))/32)) # divide by 32 is like shifting rigth 5 times
#echo $(($POWER_OP_MODE&0x20))
##echo "BAT_EXIST="$BAT_EXIST
# echo $BAT_EXIST
if [ $BAT_EXIST == "0" ]; then
echo "No Battery Detected!"
echo ""
exit 0
else
echo "Battery Detected: Yes"
CHARG_IND=$(($(($POWER_OP_MODE&0x40))/64)) # divide by 64 is like shifting rigth 6 times
#echo $(($POWER_OP_MODE&0x40))
#echo "CHARG_IND="$CHARG_IND
if [ $CHARG_IND = "1" ]; then
echo "Charging: Yes"
BAT_ICHG_MSB=$(i2cget -y -f 0 0x34 0x7A)
BAT_ICHG_LSB=$(i2cget -y -f 0 0x34 0x7B)
#echo $BAT_ICHG_MSB $BAT_ICHG_LSB
BAT_ICHG_BIN=$(( $(($BAT_ICHG_MSB << 4)) | $(($(($BAT_ICHG_LSB & 0x0F)) )) ))
BAT_ICHG=$(echo "($BAT_ICHG_BIN*0.5)"|bc)
echo "Charging current: "$BAT_ICHG" mA"
else
echo "Charging: No"
BAT_IDISCHG_MSB=$(i2cget -y -f 0 0x34 0x7C)
BAT_IDISCHG_LSB=$(i2cget -y -f 0 0x34 0x7D)
#echo $BAT_IDISCHG_MSB $BAT_IDISCHG_LSB
BAT_IDISCHG_BIN=$(( $(($BAT_IDISCHG_MSB << 5)) | $(($(($BAT_IDISCHG_LSB & 0x1F)) )) ))
BAT_IDISCHG=$(echo "($BAT_IDISCHG_BIN*0.5)"|bc)
echo "Discharge current: "$BAT_IDISCHG" mA"
fi
	fi
################################
#read battery voltage	79h, 78h	0 mV -> 
#000h,	1.1 mV/bit	FFFh -> 4.5045 V
BAT_VOLT_MSB=$(i2cget -y -f 0 0x34 0x78) 
BAT_VOLT_LSB=$(i2cget -y -f 0 0x34 0x79)
#echo $BAT_VOLT_MSB $BAT_VOLT_LSB
# bash math -- converts hex to decimal so `bc` 
# won't complain later... MSB is 8 bits, LSB is 
# lower 4 bits
BAT_BIN=$(( $(($BAT_VOLT_MSB << 4)) | $(($(($BAT_VOLT_LSB & 0x0F)) )) )) 
BAT_VOLT=$(echo " scale=2;($BAT_BIN*1.1/1000.0)"|bc -l) 
echo "Battery voltage = "$BAT_VOLT"v"

###################
#read internal temperature 5eh, 5fh -144.7c -> 
#000h, 0.1c/bit FFFh -> 264.8c
TEMP_MSB=$(i2cget -y -f 0 0x34 0x5e) 
TEMP_LSB=$(i2cget -y -f 0 0x34 0x5f)
# bash math -- converts hex to decimal so `bc` 
# won't complain later... MSB is 8 bits, LSB is 
# lower 4 bits
TEMP_BIN=$(( $(($TEMP_MSB << 4)) | $(($(($TEMP_LSB & 0x0F)) )) ))
TEMP_C=$(echo "($TEMP_BIN*0.1-144.7)"|bc)
TEMP_F=$(echo "(($TEMP_C*1.8)+32)"|bc) 
echo "Battery temp: = "$TEMP_F"f"

###################
#read fuel gauge B9h
BAT_GAUGE_HEX=$(i2cget -y -f 0 0x34 0xb9)
# bash math -- converts hex to decimal so `bc` 
# won't complain later... MSB is 8 bits, LSB is 
# lower 4 bits
BAT_GAUGE_DEC=$(($BAT_GAUGE_HEX))
echo "Battery level: "$BAT_GAUGE_DEC"%"
if [ $BAT_GAUGE_DEC -lt "40" -a $CHARG_IND = "0" ]; then
echo "** BATTERY LOW, PLEASE RECHARGE SOON **"
echo ""
else
echo ""
exit 0
fi
