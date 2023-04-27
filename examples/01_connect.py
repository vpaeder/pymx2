#!/usr/bin/python
'''This shows how to connect with an inverter
and set basic connection parameters.
'''
from mx2 import MX2
import serial

# initialize device using port /dev/ttyUSB0
mx = MX2(port="/dev/ttyUSB0", baud_rate=9600, parity=serial.PARITY_NONE)
# set device ID; this must match C072 setting
mx.set_device_id(1)
# set latency (here 5ms); this should match C078 setting
mx.set_latency_time(5)
# open connection
mx.open()
