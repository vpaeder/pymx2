"""A driver to communicate with an Omron MX2 inverter through Modbus.

   Classes:
       MX2
   
   Functions:
       crc16
   
   Submodules:
       enums
       exceptions
"""
import serial
from serial.rs485 import RS485
from time import time, sleep

__all__ = ["MX2"]

from .enums import FunctionCode, ExceptionCode, Coil, Register, MonitoringFunctions,\
                   FaultMonitorData, ModbusRegisters, TripFactor
from .exceptions import *
from .types import CoilValue, RegisterValue


def crc16(data:bytes) -> bytes:
    """Compute CRC-16-Modbus of a byte string.

    Parameters:
        data(bytes): input byte string.
    
    Returns:
        bytes: a 2-byte string containing CRC-16-Modbus value
        in little endian order.
    """
    crc = 0xffff
    poly = 0xA001
    for b in data:
        crc ^= b
        for i in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    
    return crc.to_bytes(2,"little")


class MX2():
    """A driver to control an Omron MX2 inverter
    using RS-485 (Modbus).
    
    Protected attributes:
        _latency_time(int): additional delay, in ms, between request and response (default: 30).
        _wait_time(float): total delay, in s, between request and response (_latency_time + 3.5 characters).
        _last_req_time(float): time when last request was issued.
        _dev_id(int): device ID (default: 1).
        _ser(serial.rs485.RS485): Modbus driver instance.
    """
    _latency_time = 30
    _wait_time = 0.030 + 11*3.5/9600
    _last_req_time = 0
    _dev_id = 1
    _ser = None

    def __init__(self, port:str="", baud_rate:int=9600, parity:str=serial.PARITY_NONE) -> None:
        """Constructor.
        
        Parameters:
            port(str): logical path of RS-485 device (default: "").
            baud_rate(int): serial baud rate (default: 9600).
            parity(str): serial parity (default: serial.PARITY_NONE).
        """
        self._ser = RS485()
        self.set_port(port)
        self.set_baud_rate(baud_rate)
        self.set_parity(parity)

    def get_port(self) -> str:
        """Get path of RS-485 device port.

        Returns:
            str: port path.
        """
        return self._ser.port

    def set_port(self, port:str) -> None:
        """Set path of RS-485 device port.
        
        Parameters:
            port(str): logical path of RS-485 device.

        Raises:
            SerialException: if connection is already open.
            BadParameterException: if port path is None.
        """
        if self._ser.is_open:
            raise SerialException("Connection is currently open.")
        if port is not None:
            self._ser.port = port
        else:
            raise BadParameterException("Port path cannot be None.")

    port = property(get_port, set_port)
    
    def get_baud_rate(self) -> int:
        """Get serial baud rate.

        Returns:
            int: baud rate.
        """
        return self._ser.baudrate
    
    def set_baud_rate(self, baud_rate:int) -> None:
        """Set serial baud rate. Can take the following values:
           2400, 4800, 9600, 19200, 38400, 57600, 76800, 115200.
        Must match setting C071 of MX2 inverter.

        Parameters:
            baud_rate(int): serial baud rate.
        
        Raises:
            SerialException: if connection is already open.
            BadParameterException: if baud rate is invalid.
        """
        if self._ser.is_open:
            raise SerialException("Connection is currently open.")
        if baud_rate in [2400, 4800, 9600, 19200, 38400, 57600, 76800, 115200]:
            self._ser.baudrate = baud_rate
            self._wait_time = self._latency_time/1000.0 + 11*3.5/baud_rate
        else:
            raise BadParameterException("Invalid baud rate.")
    
    baud_rate = property(get_baud_rate, set_baud_rate)

    def get_parity(self) -> str:
        """Get serial parity.

        Returns:
            str: serial parity.
        """
        return self._ser.parity
    
    def set_parity(self, parity:str) -> None:
        """Set serial parity. Can be serial.PARITY_NONE,
        serial.PARITY_EVEN, serial.PARITY_ODD.
        Must match setting C074 of MX2 inverter.

        Parameters:
            parity(str): serial parity.

        Raises:
            SerialException: if connection is already open.
            BadParameterException: if parity is not amongst allowed values.
        """
        if self._ser.is_open:
            raise SerialException("Connection is currently open.")
        if parity in [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD]:
            self._ser.parity = parity
        else:
            raise BadParameterException("Parity not recognized.")
    
    parity = property(get_parity, set_parity)

    def get_stop_bits(self) -> int:
        """Get number of stop bits.

        Returns:
            int: number of stop bits.
        """
        return self._ser.stopbits
    
    def set_stop_bits(self, stop_bits:int) -> None:
        """Set number of stop bits (either 1 or 2).
        Must match setting C075 of MX2 inverter.
        
        Parameters:
            stop_bits(int): number of stop bits.

        Raises:
            SerialException: if connection is already open.
            BadParameterException: if stop bit value is not 1 or 2.
        """
        if self._ser.is_open:
            raise SerialException("Connection is currently open.")
        if stop_bits in [1, 2]:
            self._ser.stopbits = stop_bits
        else:
            raise BadParameterException("Stop bits can be 1 or 2 only.")
    
    stop_bits = property(get_stop_bits, set_stop_bits)

    def open(self) -> None:
        """Open serial connection with MX2 inverter.

        Raises:
            SerialException: if connection is already open.
            SerialException: if connection couldn't be opened.
        """
        if self._ser.is_open:
            raise SerialException("Connection is already open.")
        try:
            self._ser.open()
        except serial.SerialException:
            raise SerialException("Couldn't open serial connection.")
    
    def close(self) -> None:
        """Close serial connection with MX2 inverter.

        Raises:
            SerialException: if connection is not open.
            SerialException: if connection couldn't be closed.
        """
        if not self._ser.is_open:
            raise SerialException("Connection is not open.")
        try:
            self._ser.close()
        except serial.SerialException:
            raise SerialException("Couldn't close serial connection.")

    is_open = property(lambda s: s._ser.is_open)

    def get_latency_time(self) -> int:
        """Get latency time, in ms.

        Returns:
            int: latency time.
        """
        return self._latency_time
    
    def set_latency_time(self, latency_time:int) -> None:
        """Set latency time, betweeen 0 and 1000 ms.
        Must be at least as much as setting C078 of MX2 inverter.
        In case device returns no data, try increasing this.
        """
        if latency_time>=0 and latency_time<=1000:
            self._latency_time = latency_time
            self._wait_time = latency_time/1000.0 + 11*3.5/self._ser.baudrate
        else:
            raise BadParameterException("Latency can be between 0 and 1000 ms.")
    
    latency_time = property(get_latency_time, set_latency_time)

    def get_device_id(self) -> int:
        """Get device ID.

        Returns:
            int: device ID.
        """
        return self._dev_id
    
    def set_device_id(self, dev_id:int) -> None:
        """Set device ID. This can be between 1 and 247 for
        single device or between 250 and 254 for broadcast and
        must match setting C072 of MX2 inverter."""
        if dev_id>0 and dev_id<248:
            self._dev_id = dev_id
        elif dev_id in [0xFA, 0xFB, 0xFC, 0xFD, 0xFE]:
            # broadcast address
            self._dev_id = dev_id
        else:
            raise BadParameterException("Device ID can be between 1 and 247 or 250 and 254.")

    device_id = property(get_device_id, set_device_id)


    def _send(self, command:FunctionCode, data:bytes) -> None:
        """Send a message to the MX2 inverter.

        Parameters:
            command(FunctionCode): command code.
            data(bytes): command data.
        
        Raises:
            SerialException: if serial port is not open.
        """
        if not self._ser.is_open:
            raise SerialException("Serial port not open.")
        
        request = bytes([self._dev_id, command]) + data
        request += crc16(request)
        self._ser.write(request)
        self._last_req_time = time()
    

    def _wait(self) -> None:
        """Wait, if necessary, until enough time has elapsed
        after previous request."""
        rem_time = self._wait_time - time() + self._last_req_time
        if rem_time<=0:
            return
        sleep(rem_time)


    def _read(self) -> bytes:
        """Read incoming bytes.
        
        Returns:
            bytes|None: bytes received from MX2 inverter.

        Raises:
            SerialException: if serial port is not open.
        """
        if not self._ser.is_open:
            raise SerialException("Serial port not open.")
        
        nbytes = self._ser.in_waiting
        if nbytes == 0:
            return None
        return self._ser.read(nbytes)
    

    def __check_validity(self, command:FunctionCode, data:bytes) -> None:
        """Check validity of a byte string against given command.
        
        Parameters:
            command(FunctionCode): command expected to match with data.
            data(bytes): byte string to check.
        
        Raises:
            NoResponseException: if data is None.
            BadResponseException: if data is issued for another device.
            BadResponseException: if data is issued for another function.
            CRCException: if CRC check failed.
            FunctionNotSupportedException: if inverter doesn't support the function.
            FunctionNotFoundException: if inverter doesn't know the function code.
            FunctionNotAvailableException: if function isn't available at the moment.
            InvalidDataFormatException: if inverter didn't recognize the data format.
            ReadOnlyTargetException: if inverter cannot write in register or coil.
            MX2Exception: for other issues.
        """
        if data is None:
            raise NoResponseException("No data.")
        if data[0]!=self._dev_id:
            raise BadResponseException("Data issued for incorrect device ID.")
        if crc16(data)!=b"\x00\x00":
            raise CRCException("Bad CRC.")
        if data[1]!=command:
            # is it an exception?
            if data[1]==command+0x80:
                if data[2]==ExceptionCode.FunctionNotSupported:
                    raise FunctionNotSupportedException("Function not supported.")
                elif data[2]==ExceptionCode.FunctionNotFound:
                    raise FunctionNotFoundException("Function not found.")
                elif data[2]==ExceptionCode.FunctionNotAvailable:
                    raise FunctionNotAvailableException("Function not available.")
                elif data[2]==ExceptionCode.OutOfBounds:
                    raise OutOfBoundsException("Target address out of bounds.")
                elif data[2]==ExceptionCode.InvalidDataFormat:
                    raise InvalidDataFormatException("Invalid data format.")
                elif data[2]==ExceptionCode.ReadOnlyTarget:
                    raise ReadOnlyTargetException("Target is read-only.")
                else:
                    raise MX2Exception("Unknown exception.")
            else:
                raise BadResponseException("Data issued for incorrect function code.")
    

    def read_coil_status(self, start_address:Coil, coil_count:int=1) -> 'list[CoilValue]':
        """Read the status of one or more coils.

        Parameters:
            start_address(Coil): address of 1st coil to read.
            coil_count(int): number of coils to query, between 1 and 31 (default: 1).
        
        Returns:
            list[CoilValue]: the coil states as coil value objects.
        
        Raises:
            BadRequestException: if device ID is a broadcast address.
            BadParameterException: if start address is outside bounds.
            BadParameterException: if coil_count is outside bounds.
            BadResponseLengthException: if response length is inconsistent with coil_count.
        """
        if self._dev_id > 249:
            raise BadRequestException("Cannot broadcast a read command.")
        if start_address<1 or start_address>0x58:
            raise BadParameterException("Start address out of range (must be between 1 and 0x58).")
        if coil_count<=0 or coil_count>31:
            raise BadParameterException("Invalid coil count (must be between 1 and 31).")
        
        self._send(FunctionCode.ReadCoilStatus, bytes([
            0,
            start_address-1,
            0,
            coil_count
        ]))
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.ReadCoilStatus, response)
        if len(response)!=6+int(coil_count/8):
            raise BadResponseLengthException("Incorrect response length for coil status request.")
        
        result = list()
        # reformat results as list of booleans
        for v in response[3+response[2]-1:2:-1]:
            result += [True if b=="1" else False for b in "{:08b}".format(v)[::-1]]
        # generate a list of (coil, value) pairs excluding invalid addresses
        addr = start_address
        values = list()
        for r in result:
            if Coil.contains(addr.value):
                values.append(CoilValue(addr, r))
                addr = addr.next()[0]
                if addr is None:
                    break
                if len(values) == coil_count:
                    break
        return values
    

    def __format_register_values(self, start_address:Register, data:bytes) -> 'list[RegisterValue]':
        """Format a byte string into a list of register values matching register sizes.
        
        Parameters:
            start_address(Register): address of 1st register to read.
            data(bytes): byte string to convert.
        
        Returns:
            list[RegisterValue]: the converted list of register values.
        """
        reg_cls = start_address.__class__
        addr = start_address
        nb = addr.n_words
        values = list()
        value = 0
        for v in [(data[n] << 8) + data[n+1] for n in range(0,len(data),2)]:
            if reg_cls.contains(addr.address):
                nb-=1
                value += v << (16*nb)
                if nb==0:
                    values.append(RegisterValue(addr, value))
                    value = 0
                    try:
                        addr = addr.next()[0]
                    except IndexError:
                        break
                    nb = addr.n_words
        return values


    def read_registers(self, start_address:Register, register_count:int=1) -> 'list[RegisterValue]':
        """Read the content of one or more registers.

        Parameters:
            start_address(Register): address of 1st register to read.
            register_count(int): number of registers to query, from 1 to 16 (default: 1).
        
        Returns:
            list[RegisterValue]: register values as a list of RegisterValue objects.

        Raises:
            BadRequestException: if device ID is a broadcast address.
            BadParameterException: if start address is outside bounds.
            BadParameterException: if register count is outside bounds.
            BadResponseLengthException: if response length doesn't match register count.
        """
        if self._dev_id > 249:
            raise BadRequestException("Cannot broadcast a read command.")
        if start_address<1 or start_address>0xffff:
            raise BadParameterException("Start address out of range (must be between 1 and 0xffff).")
        if register_count<1 or register_count>16:
            raise BadParameterException("Invalid register count (must be between 1 and 16).")

        if isinstance(start_address, Register):
            last_reg = start_address.next(register_count-1)[-1]
            word_count = last_reg.address - start_address.address + last_reg.n_words
            if word_count > 16:
                BadParameterException("Register count spans a too large address range.")
        else:
            word_count = register_count
        
        self._send(FunctionCode.ReadHoldingRegister, bytes([
            (start_address-1) >> 8,
            (start_address-1) & 0xff,
            0,
            word_count
        ]))
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.ReadHoldingRegister, response)
        if len(response)!=5+word_count*2:
            raise BadResponseLengthException("Incorrect response length for register content request.")
        
        return self.__format_register_values(start_address, response[3:3+word_count*2])


    def write_in_coil(self, address:Coil, state:bool) -> None:
        """Set the state of a coil.

        Parameters:
            address(Coil): coil address.
            state(bool): state to set.
        
        Raises:
            BadParameterException: if address is outside bounds.
            BadResponseLengthException: if response length isn't 8.
            BadResponseException: if response data differs from request.
        """
        if address<1 or address>0x58:
            raise BadParameterException("Address out of range (must be between 1 and 0x58).")
        
        msg = bytes([
            0,
            address-1,
            0xff if state else 0,
            0
        ])
        self._send(FunctionCode.WriteInCoil, msg)
        if self._dev_id > 249: # broadcast
            return
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.WriteInCoil, response)
        if len(response) != 8:
            raise BadResponseLengthException("Incorrect response length for write in coil command.")
        if response[2:6] != msg:
            raise BadResponseException("Response content differs from command content.")
    

    def write_in_register(self, address:Register, value: int) -> None:
        """Set the value of a register.
        
        Parameters:
            address(Register): register address.
            value(int): value to set, from 0 to 65535.
        
        Raises:
            BadParameterException: if address is outside bounds.
            BadParameterException: if value is outside bounds.
            BadResponseLengthException: if response length isn't 8.
            BadResponseException: if response data differs from request.
        """
        if address<1 or address>0xffff:
            raise BadParameterException("Address out of range (must be between 1 and 0xffff).")
        # if address is a Register object and n_words>1, we use write_in_multiple_registers instead
        if isinstance(address, Register) and address.n_words>1:
                return self.write_in_multiple_registers(address, [value])
        if value<0 or value>0xffff:
            raise BadParameterException("Value out of range (must be between 0 and 65535).")
        
        msg = bytes([
            (address-1) >> 8,
            (address-1) & 0xff,
            value >> 8,
            value & 0xff
        ])
        self._send(FunctionCode.WriteInHoldingRegister, msg)
        if self._dev_id > 249: # broadcast
            return
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.WriteInHoldingRegister, response)
        if len(response) != 8:
            raise BadResponseLengthException("Incorrect response length for write in register command.")
        if response[2:6] != msg:
            raise BadResponseException("Response content differs from command content.")


    def loopback_test(self) -> None:
        """Perform a loopback test.
        
        Raises:
            BadRequestException: if device ID is a broadcast address.
            BadResponseLengthException: if response length isn't 8.
            BadResponseException: if response data differs from request.
        """
        if self._dev_id > 249:
            raise BadRequestException("Cannot broadcast the loopback test.")
        value = int(time()*1000) & 0xffff
        msg = bytes([0, 0, value >> 8, value & 0xff])
        self._send(FunctionCode.LoopbackTest, msg)
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.LoopbackTest, response)
        if len(response) != 8:
            raise BadResponseLengthException("Incorrect response length for loopback test.")
        if response[2:6] != msg:
            raise BadResponseException("Response content differs from command content.")


    def write_in_multiple_coils(self, start_address:Coil, values:'list[bool]') -> None:
        """Set the state of multiple coils at once.

        Parameters:
            start_address(Coil): address of 1st coil to set.
            values(list[bool]): coil values.
        
        Raises:
            BadParameterException: if start address is outside bounds.
            BadParameterException: if len(values) is zero or more than 31.
            BadResponseLengthException: if response length isn't 8.
            BadResponseException: if response data differs from request.
        """
        if start_address<1 or start_address>0x58:
            raise BadParameterException("Start address out of range (must be between 1 and 0x58).")
        if len(values)==0 or len(values)>31:
            raise BadParameterException("Invalid data array length (must be between 1 and 31).")
        
        nbytes = min(4, int(len(values)/8) + 1)
        intval = sum([((1 if values[n] else 0) << (len(values)-n-1)) for n in range(len(values))])
        msg = bytes([
            0,
            start_address-1,
            0,
            len(values),
            nbytes
        ])
        for n in range(nbytes):
            msg += bytes([(intval >> 8*(nbytes-n-1)) & 0xff])

        self._send(FunctionCode.WriteInMultipleCoils, msg)
        if self._dev_id > 249: # broadcast
            return
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.WriteInMultipleCoils, response)
        if len(response) != 8:
            raise BadResponseLengthException("Incorrect response length for write in multiple coils command.")
        if response[2:6] != msg[0:4]:
            raise BadResponseException("Response content differs from command content.")
    

    def __prepare_for_writing(self, start_address:Register, values:'list[int]') -> bytes:
        """Convert a list of integers into a byte string matching register sizes.
        
        Parameters:
            start_address(Register): address of 1st register.
            values(list[int]): values to convert.
        
        Returns:
            bytes: the converted byte string.
        
        Raises:
            BadParameterException: if any value if out of range.
        """
        msg = bytes()
        if isinstance(start_address, Register):
            regs = [start_address] + start_address.next(len(values))
            for rv in zip(regs, values):
                if rv[1]<0 or rv[1]>=(1 << 16*rv[0].n_words):
                    raise BadParameterException("Value out of range.")
                msg += rv[1].to_bytes(2*rv[0].n_words, 'big')
        else:
            for v in values:
                if v<0 or v>0xffff:
                    raise BadParameterException("Value out of range (must be between 0 and 65535).")
                msg += bytes([v >> 8, v & 0xff])
        return msg


    def write_in_multiple_registers(self, start_address:Register, values:'list[int]') -> None:
        """Set the values of multiple registers at once.

        Parameters:
            start_address(Register): address of 1st register to set.
            values(list[int]): register values.
        
        Raises:
            BadParameterException: if start address is outside bounds.
            BadParameterException: if len(values) is zero or more than 16.
            BadParameterException: if any of the values is less than 0 or more than 65535.
            BadResponseLengthException: if response length isn't 8.
            BadResponseException: if response data differs from request.
        """
        if start_address<1 or start_address>0xffff:
            raise BadParameterException("Start address out of range (must be between 1 and 0xffff).")
        if len(values)==0 or len(values)>16:
            raise BadParameterException("Invalid data array length (must be between 1 and 16).")
        
        if isinstance(start_address, Register):
            last_reg = start_address.next(len(values)-1)[-1]
            word_count = last_reg.address - start_address.address + last_reg.n_words
            if word_count > 16:
                raise BadParameterException("Register count spans a too large address range.")
        else:
            word_count = len(values)

        msg = bytes([
            (start_address-1) >> 8,
            (start_address-1) & 0xff,
            0,
            word_count,
            2*word_count
        ])

        msg += self.__prepare_for_writing(start_address, values)
        
        self._send(FunctionCode.WriteInRegisters, msg)
        if self._dev_id > 249: # broadcast
            return
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.WriteInRegisters, response)
        if len(response) != 8:
            raise BadResponseLengthException("Incorrect response length for write in multiple registers command.")
        if response[2:6] != msg[0:4]:
            raise BadResponseException("Response content differs from command content.")


    def read_and_write_registers(self, read_start_address:Register, write_start_address:Register, read_count:int, write_values:'list[int]') -> bytes:
        """Read from and write to one or more registers at once.

        Parameters:
            read_start_address(Register): address of 1st register to read.
            write_start_address(Register): address of 1st register to set.
            read_count(int): number of registers to query, from 1 to 16.
            values(list[int]): register values to write.

        Returns:
            list[int]: the values of requested registers as a list of integers.

        Raises:
            BadRequestException: if device ID is a broadcast address.
            BadParameterException: if read start address is outside bounds.
            BadParameterException: if write start address is outside bounds.
            BadParameterException: if read_count is outside bounds.
            BadParameterException: if len(values) is zero or more than 16.
            BadParameterException: if any of the values is less than 0 or more than 65535.
            BadResponseLengthException: if response length doesn't match read_count.
        """
        if self._dev_id > 249:
            raise BadRequestException("Cannot broadcast a read command.")
        if read_start_address<1 or read_start_address>0xffff:
            raise BadParameterException("Read start address out of range (must be between 1 and 0xffff).")
        if write_start_address<1 or write_start_address>0xffff:
            raise BadParameterException("Write start address out of range (must be between 1 and 0xffff).")
        if read_count<1 or read_count>16:
            raise BadParameterException("Invalid read count (must be between 1 and 16).")
        if len(write_values)==0 or len(write_values)>16:
            raise BadParameterException("Invalid write data length (must be between 1 and 16).")
        for v in write_values:
            if v<0 or v>0xffff:
                raise BadParameterException("Value out of range (must be between 0 and 65535).")
        
        if isinstance(read_start_address, Register):
            last_reg = read_start_address.next(read_count-1)[-1]
            read_word_count = last_reg.address - read_start_address.address + last_reg.n_words
            if read_word_count > 16:
                BadParameterException("Register count spans a too large address range.")
        else:
            read_word_count = read_count

        if isinstance(write_start_address, Register):
            last_reg = write_start_address.next(len(write_values)-1)[-1]
            write_word_count = last_reg.address - write_start_address.address + last_reg.n_words
            if write_word_count > 16:
                raise BadParameterException("Register count spans a too large address range.")
        else:
            write_word_count = len(write_values)

        msg = bytes([
            (read_start_address-1) >> 8,
            (read_start_address-1) & 0xff,
            0,
            read_word_count,
            (write_start_address-1) >> 8,
            (write_start_address-1) & 0xff,
            0,
            write_word_count,
            2*write_word_count
        ])

        msg += self.__prepare_for_writing(write_start_address, write_values)

        self._send(FunctionCode.ReadWriteRegisters, msg)
        self._wait()
        response = self._read()

        self.__check_validity(FunctionCode.ReadWriteRegisters, response)
        if len(response)!=5+read_word_count*2:
            raise BadResponseLengthException("Incorrect response length for register content request.")
        
        return self.__format_register_values(read_start_address, response[3:3+read_word_count*2])


    def read_fault_monitor(self, index:int, value:FaultMonitorData) -> int:
        """Query fault monitor.

        Parameters:
            index(int): fault monitor index (from 1 to 6).
            value(FaultMonitorData): index of fault monitor data to read (from 0 to 9, see enum).

        Returns:
            int: fault monitor value.

        Raises:
            BadParameterException: if fault monitor index if outside bounds.
            BadParameterException: if fault monitor data index is outside bounds.
        """
        if index<1 or index>6:
            raise BadParameterException("Fault monitor index can be between 1 and 6.")
        if value<0 or value>9:
            raise BadParameterException("Fault monitor data index can be between 0 and 9.")
        
        addr = [MonitoringFunctions.FaultMonitor1, MonitoringFunctions.FaultMonitor2,
                MonitoringFunctions.FaultMonitor3, MonitoringFunctions.FaultMonitor4,
                MonitoringFunctions.FaultMonitor5, MonitoringFunctions.FaultMonitor6][index] + value

        if value in [FaultMonitorData.Frequency, FaultMonitorData.RunningTime, FaultMonitorData.PowerOnTime]:
            result = self.read_registers(addr, 2)
            return (result[0] << 16) + result[1]
        else:
            result = self.read_registers(addr, 1)
            return result[0]


    def save_settings_to_eeprom(self) -> None:
        """Attempt to save modified registers to EEPROM.
        
        Raises:
            MX2Exception: if writing to EEPROM failed.
        """
        self.write_in_register(ModbusRegisters.WriteToEEPROM, 1)
        while self.read_coil_status(Coil.DataWritingInProgress, 1)[0] == True:
            sleep(self._wait_time)
            if self.read_registers(MonitoringFunctions.FaultMonitor1, 1)[0] == TripFactor.EEPROMError:
                raise MX2Exception("EEPROM write failed.")
