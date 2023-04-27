#!/usr/bin/python
'''Read the content of the 1st set of fault monitor registers.
Adapted from datasheet examples on pp. 305 and 308.
'''
from mx2 import MX2
from mx2.enums import StandardFunctions, MainProfileParameters
import serial

# open connection with device
mx = MX2(port="/dev/ttyUSB0", baud_rate=9600, parity=serial.PARITY_NONE)
mx.set_device_id(1)
mx.set_latency_time(5)
mx.open()
# set multi-speed reference 0 to 50Hz
mx.write_in_register(address=StandardFunctions.MultiStepSpeedReference0, value=500)
# set 1st acceleration time to 3000 seconds
mx.write_in_register(address=MainProfileParameters.AccelerationTime1, value=300000)
# this will call the following command, as value is larger than 16bit and AccelerationTime1 is 2-word.
mx.write_in_multiple_registers(address=MainProfileParameters.AccelerationTime1, values=[300000])
