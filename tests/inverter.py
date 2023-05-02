import unittest
from unittest.mock import Mock
import mx2
from mx2.exceptions import *
from mx2.enums import FunctionCode, ExceptionCode, Coil, MonitoringFunctions,\
                      StandardFunctions, MainProfileParameters
from mx2.types import CoilValue, RegisterValue


class TestInverter(unittest.TestCase):
    def setUp(self):
        self.mx = mx2.MX2()
        self.mx._ser = Mock()
        self.mx._ser.write = Mock()
        self.mx._ser.read = Mock()
    
    def test_check_validity_ok(self):
        self.mx._dev_id = 8
        data = bytes([8, 1, 1, 5, 0x92, 0x17])
        self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, data)
    
    def test_check_validity_fail(self):
        with self.assertRaises(NoResponseException):
            self.mx._MX2__check_validity(FunctionCode.LoopbackTest, None)
        self.mx._dev_id = 1
        with self.assertRaises(BadResponseException):
            self.mx._MX2__check_validity(FunctionCode.LoopbackTest, bytes([8, 1]))
        with self.assertRaises(CRCException):
            self.mx._MX2__check_validity(FunctionCode.LoopbackTest, bytes([1, 1]))
        with self.assertRaises(FunctionNotSupportedException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, ExceptionCode.FunctionNotSupported, 0x81, 0x90]))
        with self.assertRaises(FunctionNotFoundException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, ExceptionCode.FunctionNotFound, 0xC1, 0x91]))
        with self.assertRaises(InvalidDataFormatException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, ExceptionCode.InvalidDataFormat, 0, 0x51]))
        with self.assertRaises(OutOfBoundsException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, ExceptionCode.OutOfBounds, 0x80, 0x48]))
        with self.assertRaises(FunctionNotAvailableException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, ExceptionCode.FunctionNotAvailable, 0xC0, 0x49]))
        with self.assertRaises(ReadOnlyTargetException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, ExceptionCode.ReadOnlyTarget, 1, 0x89]))
        with self.assertRaises(MX2Exception):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x81, 0x50, 0x40, 0x6C]))
        with self.assertRaises(BadResponseException):
            self.mx._MX2__check_validity(FunctionCode.ReadCoilStatus, bytes([1, 0x40, 1, 0xD0]))
        
    def test_read_coil_status_ok(self):
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 1, 1, 5, 0x92, 0x17])
        self.assertEqual(self.mx.read_coil_status(Coil.OperationCommand, 5),
                         [True, False, True, False, False])
    
    def test_read_coil_status_fail(self):
        with self.assertRaises(BadParameterException):
            self.mx.read_coil_status(0, 1)
        with self.assertRaises(BadParameterException):
            self.mx.read_coil_status(0x59, 1)
        with self.assertRaises(BadParameterException):
            self.mx.read_coil_status(Coil.OperationCommand, 0)
        with self.assertRaises(BadParameterException):
            self.mx.read_coil_status(Coil.OperationCommand, 32)
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 1, 1, 5, 1, 0x57, 0x6D])
        with self.assertRaises(BadResponseLengthException):
            self.mx.read_coil_status(Coil.OperationCommand, 5)
        self.mx._dev_id = 0xFA # 1st broadcast range
        with self.assertRaises(BadRequestException):
            self.mx.read_coil_status(1, 1)

    def test_read_registers_ok(self):
        self.mx._dev_id = 1
        self.mx._ser.read.return_value = bytes([1, 3, 0x0C, 0, 3, 0, 0, 0, 0x63, 0, 0, 0, 0x1E, 1, 0x1C, 0xAF, 0x6D])
        self.assertEqual(self.mx.read_registers(MonitoringFunctions.FaultFrequencyMonitor, 5),
                         [3, 0, 0x63, 0x1E, 0x011C])

    def test_read_registers_fail(self):
        self.mx._dev_id = 1
        with self.assertRaises(BadParameterException):
            self.mx.read_registers(0, 1)
        with self.assertRaises(BadParameterException):
            self.mx.read_registers(65536, 1)
        with self.assertRaises(BadParameterException):
            self.mx.read_registers(MonitoringFunctions.FaultFrequencyMonitor, 0)
        with self.assertRaises(BadParameterException):
            self.mx.read_registers(MonitoringFunctions.FaultFrequencyMonitor, 17)
        with self.assertRaises(BadResponseLengthException):
            self.mx._ser.read.return_value = bytes([1, 3, 0x0C, 0x20, 0xF5])
            self.mx.read_registers(MonitoringFunctions.FaultFrequencyMonitor, 6)
        self.mx._dev_id = 0xFA # 1st broadcast range
        with self.assertRaises(BadRequestException):
            self.mx.read_registers(MonitoringFunctions.FaultFrequencyMonitor, 6)

    def test_write_in_coil_ok(self):
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 5, 0, 0, 0xff, 0, 0x8C, 0xA3])
        self.mx.write_in_coil(Coil.OperationCommand, True)

    def test_write_in_coil_fail(self):
        with self.assertRaises(BadParameterException):
            self.mx.write_in_coil(0, True)
        with self.assertRaises(BadParameterException):
            self.mx.write_in_coil(0x59, True)
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 5, 0, 0, 0xff, 0x85, 0x4D])
        with self.assertRaises(BadResponseLengthException):
            self.mx.write_in_coil(Coil.OperationCommand, True)
        self.mx._ser.read.return_value = bytes([8, 5, 0, 0, 0, 0, 0xCD, 0x53])
        with self.assertRaises(BadResponseException):
            self.mx.write_in_coil(Coil.OperationCommand, True)

    def test_write_in_register_ok(self):
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 6, 0x12, 0x02, 1, 0xF4, 0x2D, 0xFC])
        self.mx.write_in_register(StandardFunctions.A003, 0x01f4)
        # same but with register larger than 1 word => call write_in_multiple_registers
        self.mx._ser.read.return_value = bytes([8, 0x10, 0x12, 0x15, 0, 2, 0x55, 0xED])
        self.mx.write_in_register(StandardFunctions.A020, 65536)

    def test_write_in_register_fail(self):
        with self.assertRaises(BadParameterException):
            self.mx.write_in_register(0, 0x01f4)
        with self.assertRaises(BadParameterException):
            self.mx.write_in_register(65536, 0x01f4)
        with self.assertRaises(BadParameterException):
            self.mx.write_in_register(StandardFunctions.A020, -1)
        with self.assertRaises(BadParameterException):
            self.mx.write_in_register(StandardFunctions.A001, 65536)
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 6, 0x12, 0x02, 0xF4, 0x65, 0xAB])
        with self.assertRaises(BadResponseLengthException):
            self.mx.write_in_register(StandardFunctions.A003, 0x01f4)
        self.mx._ser.read.return_value = bytes([8, 6, 0x12, 0x02, 0, 0xF4, 0x2C, 0x6C])
        with self.assertRaises(BadResponseException):
            self.mx.write_in_register(StandardFunctions.A003, 0x01f4)

    def test_write_in_multiple_coils_ok(self):
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 0x0f, 0, 6, 0, 5, 0x75, 0x50])
        self.mx.write_in_multiple_coils(Coil.IntelligentInput1, [True, True, True, False, True])

    def test_write_in_multiple_coils_fail(self):
        self.mx._dev_id = 8
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_coils(0, [True, True])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_coils(0x59, [True, True])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_coils(Coil.IntelligentInput1, [])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_coils(Coil.IntelligentInput1, [True]*32)
        self.mx._ser.read.return_value = bytes([8, 0x0f, 0, 6, 0, 0xC5, 0x75])
        with self.assertRaises(BadResponseLengthException):
            self.mx.write_in_multiple_coils(Coil.IntelligentInput1, [True, True, True, False, True])
        self.mx._ser.read.return_value = bytes([8, 0x0f, 0, 6, 0, 4, 0xB4, 0x90])
        with self.assertRaises(BadResponseException):
            self.mx.write_in_multiple_coils(Coil.IntelligentInput1, [True, True, True, False, True])
    
    def test_write_in_multiple_registers_ok(self):
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 0x10, 0x11, 2, 0, 2, 0xE5, 0xAD])
        self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [0x0493E0])
        

    def test_write_in_multiple_registers_fail(self):
        self.mx._dev_id = 8
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_registers(0, [0, 0])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_registers(65536, [0, 0])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [0]*17)
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [-1])
        with self.assertRaises(BadParameterException):
            self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [2**32])
        self.mx._ser.read.return_value = bytes([8, 0x10, 0x11, 2, 0, 0x90, 0x64])
        with self.assertRaises(BadResponseLengthException):
            self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [4, 0x93E0])
        self.mx._ser.read.return_value = bytes([8, 0x10, 0x11, 2, 0, 3, 0x24, 0x6D])
        with self.assertRaises(BadResponseException):
            self.mx.write_in_multiple_registers(MainProfileParameters.AccelerationTime1, [4, 0x93E0])

    def test_read_and_write_registers_ok(self):
        self.mx._dev_id = 1
        self.mx._ser.read.return_value = bytes([1, 0x17, 4, 0, 0, 0x13, 0x88, 0xF4, 0x71])
        self.assertEqual(self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                                          MainProfileParameters.OutputFrequency,
                                                          1, [0x1388]), [0x1388])

    def test_read_and_write_registers_fail(self):
        self.mx._dev_id = 1
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(0, MainProfileParameters.OutputFrequency, 2, [0, 0x1388])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(65536, MainProfileParameters.OutputFrequency, 2, [0, 0x1388])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency, 0, 2, [0, 0x1388])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency, 65536, 2, [0, 0x1388])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             0, [0, 0x1388])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             17, [0, 0x1388])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             2, [])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             2, [0]*17)
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             2, [-1])
        with self.assertRaises(BadParameterException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             2, [65536])
        self.mx._ser.read.return_value = bytes([1, 0x17, 4, 0, 0, 0x13, 0x35, 0x34])
        with self.assertRaises(BadResponseLengthException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             1, [0x1388])
        self.mx._dev_id = 0xFA # 1st broadcast range
        with self.assertRaises(BadRequestException):
            self.mx.read_and_write_registers(MonitoringFunctions.OutputFrequency,
                                             MainProfileParameters.OutputFrequency,
                                             2, [0, 0x1388])

    def test_read_fault_monitor_fail(self):
        with self.assertRaises(BadParameterException):
            self.mx.read_fault_monitor(0, 0)
        with self.assertRaises(BadParameterException):
            self.mx.read_fault_monitor(7, 0)
        with self.assertRaises(BadParameterException):
            self.mx.read_fault_monitor(1, -1)
        with self.assertRaises(BadParameterException):
            self.mx.read_fault_monitor(1, 10)

    def test_save_settings_to_eeprom_ok(self):
        self.mx.read_coil_status = Mock(return_value=[CoilValue(Coil.DataWritingInProgress, False)])
        self.mx._dev_id = 8
        self.mx._ser.read.return_value = bytes([8, 6, 0x08, 0xff, 0, 1, 0x7A, 0xC3])
        self.mx.save_settings_to_eeprom()
        
    def test_save_settings_to_eeprom_fail(self):
        self.mx.read_coil_status = Mock(return_value=[CoilValue(Coil.DataWritingInProgress, True)])
        self.mx.read_registers = Mock(return_value=[RegisterValue(MonitoringFunctions.FaultMonitor1Factor, 8)])
        self.mx._ser.read.return_value = bytes([8, 6, 0x08, 0xff, 0, 1, 0x7A, 0xC3])
        self.mx._dev_id = 8
        with self.assertRaises(MX2Exception):
            self.mx.save_settings_to_eeprom()
