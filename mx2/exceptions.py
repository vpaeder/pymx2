"""Exceptions for MX2 driver."""

__all__ = ["MX2Exception", "SerialException", "BadParameterException",
           "NoResponseException", "BadResponseLengthException", "BadRequestException",
           "BadResponseException", "CRCException", "FunctionNotSupportedException",
           "FunctionNotFoundException", "InvalidDataFormatException", "OutOfBoundsException",
           "FunctionNotAvailableException", "ReadOnlyTargetException"]

class MX2Exception(Exception):
    """Base class for custom exceptions."""
    pass

class SerialException(MX2Exception):
    """Used for errors relative to serial connection."""
    pass

class BadParameterException(MX2Exception):
    """For settings out of bounds, with incorrect data type, ..."""
    pass

class NoResponseException(MX2Exception):
    """This is used to notify that a command expecting a reply didn't receive any."""
    pass

class BadResponseLengthException(MX2Exception):
    """This tells that the received response length is incorrect."""
    pass

class BadResponseException(MX2Exception):
    """This is meant for for a response with incorrect content (e.g. echoed
    data expected but response differs)."""
    pass

class CRCException(MX2Exception):
    """CRC check produced non-zero result."""
    pass

class BadRequestException(MX2Exception):
    """Used to tell that a request or a request parameter is incorrect."""
    pass

class FunctionNotSupportedException(MX2Exception):
    """This is used to tell that the function is not supported by the inverter."""
    pass

class FunctionNotFoundException(MX2Exception):
    """The function couldn't be found on the inverter."""
    pass

class InvalidDataFormatException(MX2Exception):
    """The inverter didn't aknowledge the data format for the requested function."""
    pass

class OutOfBoundsException(MX2Exception):
    """The target register is out of the allowed bounds."""
    pass

class FunctionNotAvailableException(MX2Exception):
    """The function is not available at the moment of calling."""
    pass

class ReadOnlyTargetException(MX2Exception):
    """A read-only function was used with a write command."""
    pass
