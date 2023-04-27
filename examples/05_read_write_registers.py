#!/usr/bin/python
'''Set frequency to 50 Hz and read output frequency using
combined command (command code 0x17).
Adapted from datasheet example on p. 309.
'''
from mx2 import MX2
from mx2.enums import MainProfileParameters, MonitoringFunctions, Coil
import serial

# open connection with device
mx = MX2(port="/dev/ttyUSB0", baud_rate=9600, parity=serial.PARITY_NONE)
mx.set_device_id(1)
mx.set_latency_time(5)
mx.open()
# set RUN coil state to 1
mx.write_in_coil(Coil.OperationCommand, True)
# set output frequency to 50Hz and read frequency monitor
result = mx.read_and_write_registers(read_start_address=MonitoringFunctions.OutputFrequency,
                                     write_start_address=MainProfileParameters.OutputFrequency,
                                     read_count = 1,
                                     write_values = [500])
print(result[0])
# Output should look like:
#    <MonitoringFunctions.OutputFrequency (0x1001): 500>
