import unittest
from unittest.mock import patch, Mock
import mx2
from mx2.exceptions import BadParameterException, SerialException
from mx2.enums import FunctionCode


class TestModbus(unittest.TestCase):
    def setUp(self):
        self.mx = mx2.MX2()
        self.mx._ser.is_open = Mock()
    
    def test_set_latency_time_ok(self):
        self.mx._ser.is_open = False
        for t in range(0,1001):
            self.mx.set_latency_time(t)
            self.assertEqual(self.mx.get_latency_time(), t)
            self.mx.set_baud_rate(9600)
            self.assertEqual(self.mx._wait_time, t/1000.0 + 11*3.5/self.mx.get_baud_rate())
            self.mx.set_baud_rate(2400)
            self.assertEqual(self.mx._wait_time, t/1000.0 + 11*3.5/self.mx.get_baud_rate())
    
    def test_set_latency_time_fail(self):
        for t in [-100, 1100]:
            with self.assertRaises(BadParameterException):
                self.mx.set_latency_time(t)
            self.assertNotEqual(self.mx.get_latency_time(), t)
    
    def test_set_device_id_ok(self):
        for d in range(1,248):
            self.mx.set_device_id(d)
            self.assertEqual(self.mx.get_device_id(), d)
        for d in range(250, 255):
            self.mx.set_device_id(d)
            self.assertEqual(self.mx.get_device_id(), d)

    def test_set_device_id_fail(self):
        for d in [-10, 0, 248, 249, 255]:
            with self.assertRaises(BadParameterException):
                self.mx.set_device_id(d)
            self.assertNotEqual(self.mx.get_device_id(), d)
    
    def test_send_ok(self):
        self.mx._ser.is_open = True
        with patch.object(self.mx._ser, "write"):
            # test with datasheet example in section B-3-4, p. 302.
            self.mx._dev_id = 8
            self.mx._send(FunctionCode.ReadCoilStatus, bytes([0, 6, 0, 5]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([8, 1, 0, 6, 0, 5, 0x1C, 0x91]))
            # test with datasheet example in section B-3-4, p. 303.
            self.mx._dev_id = 1
            self.mx._send(FunctionCode.ReadHoldingRegister, bytes([0, 0x11, 0, 6]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([1, 3, 0, 0x11, 0, 6, 0x95, 0xCD]))
            # test with datasheet example in section B-3-4, p. 304.
            self.mx._dev_id = 8
            self.mx._send(FunctionCode.WriteInCoil, bytes([0, 0, 0xff, 0]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([8, 5, 0, 0, 0xff, 0, 0x8C, 0xA3]))
            # test with datasheet example in section B-3-4, p. 305.
            self.mx._dev_id = 8
            self.mx._send(FunctionCode.WriteInHoldingRegister, bytes([0x10, 0x28, 1, 0xF4]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([8, 6, 0x10, 0x28, 1, 0xF4, 0x0D, 0x8C]))
            # test with datasheet example in section B-3-4, p. 307.
            self.mx._dev_id = 8
            self.mx._send(FunctionCode.WriteInMultipleCoils, bytes([0, 6, 0, 5, 2, 0x17, 0]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([8, 0x0F, 0, 6, 0, 5, 2, 0x17, 0, 0x83, 0xEA]))
            # test with datasheet example in section B-3-4, p. 308.
            self.mx._dev_id = 8
            self.mx._send(FunctionCode.WriteInRegisters, bytes([0x10, 0x13, 0, 2, 4, 0, 4, 0x93, 0xE0]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([8, 0x10, 0x10, 0x13, 0, 2, 4, 0, 4, 0x93, 0xE0, 0x7D, 0x53]))
            # test with datasheet example in section B-3-4, p. 309.
            self.mx._dev_id = 1
            self.mx._send(FunctionCode.ReadWriteRegisters, bytes([0x10, 0, 0, 2, 0, 0, 0, 2, 4, 0, 0, 0x13, 0x88]))
            self.assertEqual(self.mx._ser.write.call_args[0][0], bytes([1, 0x17, 0x10, 0, 0, 2, 0, 0, 0, 2, 4, 0, 0, 0x13, 0x88, 0xF4, 0x86]))

    def test_send_fail(self):
        self.mx._ser.is_open = False
        with self.assertRaises(SerialException):
            self.mx._send(FunctionCode.LoopbackTest, bytes())

    def test_read_ok(self):
        self.mx._ser = Mock()
        self.mx._ser.is_open = True
        self.mx._ser.in_waiting = 0
        self.assertEqual(self.mx._read(), None)
        self.mx._ser.in_waiting = 10
        with patch.object(self.mx._ser, "read", return_value=bytes(10)):
            self.assertEqual(self.mx._read(), bytes(10))

    def test_read_fail(self):
        self.mx._ser.is_open = False
        with self.assertRaises(SerialException):
            self.mx._read()
