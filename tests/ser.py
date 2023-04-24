import unittest
from unittest.mock import patch, Mock
import mx2
from mx2.exceptions import SerialException, BadParameterException

class TestSerial(unittest.TestCase):
    def setUp(self):
        self.mx = mx2.MX2()
        self.mx._ser.is_open = Mock()

    def test_open_ok(self):
        self.mx._ser.is_open = False
        with patch.object(self.mx._ser, "open", return_value=True):
            self.mx.open()

    def test_open_fail(self):
        self.mx._ser.is_open = True
        with self.assertRaises(SerialException):
            self.mx.open()
    
    def test_close_ok(self):
        self.mx._ser.is_open = True
        with patch.object(self.mx._ser, "close", return_value=True):
            self.mx.close()
    
    def test_close_fail(self):
        self.mx._ser.is_open = False
        with self.assertRaises(SerialException):
            self.mx.close()

    def test_set_port_ok(self):
        self.mx._ser.is_open = False
        self.mx.set_port("something")
        self.assertEqual(self.mx.get_port(), "something")
    
    def test_set_port_fail(self):
        self.mx._ser.is_open = False
        with self.assertRaises(BadParameterException):
            self.mx.set_port(None)
        self.mx._ser.is_open = True
        with self.assertRaises(SerialException):
            self.mx.set_port("something")

    def test_set_baud_rate_ok(self):
        self.mx._ser.is_open = False
        for baud_rate in [2400, 4800, 9600, 19200, 38400, 57600, 76800, 115200]:
            self.mx.set_baud_rate(baud_rate)
            self.assertEqual(self.mx.get_baud_rate(), baud_rate)
    
    def test_set_baud_rate_fail(self):
        # set invalid baud rate
        self.mx._ser.is_open = False
        with self.assertRaises(BadParameterException):
            self.mx.set_baud_rate(1234)
        self.assertNotEqual(self.mx.get_baud_rate(), 1234)
        # port already open
        self.mx._ser.is_open = True
        with self.assertRaises(SerialException):
            self.mx.set_baud_rate(2400)
        with self.assertRaises(SerialException):
            self.mx.set_baud_rate(1234)

    def test_set_parity_ok(self):
        self.mx._ser.is_open = False
        for parity in [mx2.serial.PARITY_NONE, mx2.serial.PARITY_EVEN, mx2.serial.PARITY_ODD]:
            self.mx.set_parity(parity)
            self.assertEqual(self.mx.get_parity(), parity)
    
    def test_set_parity_fail(self):
        # set invalid parity
        self.mx._ser.is_open = False
        with self.assertRaises(BadParameterException):
            self.mx.set_parity("INVALID")
        self.assertNotEqual(self.mx.get_parity(), "INVALID")
        # port already open
        self.mx._ser.is_open = True
        with self.assertRaises(SerialException):
            self.mx.set_parity(mx2.serial.PARITY_NONE)
        with self.assertRaises(SerialException):
            self.mx.set_parity("INVALID")

    def test_set_stop_bits_ok(self):
        self.mx._ser.is_open = False
        for stop_bits in [1, 2]:
            self.mx.set_stop_bits(stop_bits)
            self.assertEqual(self.mx.get_stop_bits(), stop_bits)
    
    def test_set_stop_bits_fail(self):
        # set invalid stop bits
        self.mx._ser.is_open = False
        with self.assertRaises(BadParameterException):
            self.mx.set_stop_bits(3)
        self.assertNotEqual(self.mx.get_stop_bits(), 3)
        # port already open
        self.mx._ser.is_open = True
        with self.assertRaises(SerialException):
            self.mx.set_stop_bits(1)
        with self.assertRaises(SerialException):
            self.mx.set_stop_bits(3)

