#!/usr/bin/python
'''Wait that the inverter is ready,
then set the state of a coil (RUN)
and query the state of the device.
Adapted from datasheet examples on pp. 302 and 304.
'''
from mx2 import MX2
from mx2.enums import Coil
from time import sleep
import serial

# open connection with device
mx = MX2(port="/dev/ttyUSB0", baud_rate=9600, parity=serial.PARITY_NONE)
mx.set_device_id(1)
mx.set_latency_time(5)
mx.open()
# read device state
while not mx.read_coil_status(Coil.InverterReady, 1)[0]:
    sleep(0.1)
print("Device ready. Starting motor...")
# set RUN coil state to 1
mx.write_in_coil(Coil.OperationCommand, True)
# read device state
# here we read 3 coils: operation status, rotation direction, device ready
state = mx.read_coil_status(Coil.OperationStatus, 3)
print("Device is {}ready".format("" if state[2] else "not "))
print("Motor is {}running".format("" if state[0] else "not "))
print("Rotation direction is {}".format("reverse" if state[1] else "forward"))
