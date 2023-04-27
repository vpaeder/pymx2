#!/usr/bin/python
'''This demonstrates how to handle data types returned by read functions.
'''
from mx2 import MX2
from mx2.enums import Coil, MonitoringFunctions
import serial

# open connection with device
mx = MX2(port="/dev/ttyUSB0", baud_rate=9600, parity=serial.PARITY_NONE)
mx.set_device_id(1)
mx.set_latency_time(5)
mx.open()

### Coil value handling ###
# read the state of 3 coils;
# this returns a list of 3 CoilValue objects that hold a reference
# to the coil address and the coil value
coil_state = mx.read_coil_status(Coil.OperationStatus, 3)
# print out the 1st coil value; this should look like:
#   <Coil.OperationStatus (0x0f): False>
print(coil_state[0])
# A CoilValue object can be handled similarly as a boolean.
# For example:
print("Inverter output is {}active".format("" if coil_state[0] else "not "))
# One can also access coil reference and value directly:
print("Coil {} is {}active".format(coil_state[0].coil.name, "" if coil_state[0].value else "not "))

### Register value handling ###
register_values = mx.read_registers(MonitoringFunctions.OutputFrequency, 1)
# this returns a list of RegisterValue objects, which contain
# a reference to the register and the value that has been read.
# Print out the result; this should look like:
#   <MonitoringFunctions.OutputFrequency (0x1001): 500>
print(register_values[0])
# A RegisterValue object will automatically downcast to integer when
# used with an operator that involves another integer or RegisterValue.
# For example:
print("Register {} value is: {:d}".format(register_values[0].register.name, register_values[0]))
if register_values[0] > 300:
    print("Output frequency is larger than 30 Hz.")
if register_values[0]-500 > 0:
    print("Output frequency is larger than 50 Hz.")
