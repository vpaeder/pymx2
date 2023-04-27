#!/usr/bin/python
'''Read the content of the 1st set of fault monitor registers.
Adapted from datasheet example on p. 303.
'''
from mx2 import MX2
from mx2.enums import MonitoringFunctions, FaultMonitorData
import serial

# open connection with device
mx = MX2(port="/dev/ttyUSB0", baud_rate=9600, parity=serial.PARITY_NONE)
mx.set_device_id(1)
mx.set_latency_time(5)
mx.open()
# read first 5 registers: trip factor, inverter status, frequency, current, voltage
regs = mx.read_registers(MonitoringFunctions.FaultMonitor1, 5)
# regs[0] (trip factor) can be compared with mx2.enums.TripFactor to make sense of it;
# regs[1] (inverter status) can be compared with mx2.enums.InverterStatus

# alternative way to obtain fault monitor data (one at a time)
trip_factor = mx.read_fault_monitor(index=1, value=FaultMonitorData.Factor)
frequency = mx.read_fault_monitor(index=1, value=FaultMonitorData.Frequency)
