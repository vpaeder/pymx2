"""Data types for MX2 driver."""

from .enums import Coil, Register

__all__ = ["CoilValue", "RegisterValue"]


class CoilValue:
    """A container class used to hold a value together with an associated coil.

    Attributes:
        coil(Coil): coil.
        value(bool): coil state.
    """
    def __init__(self, coil:Coil, value:bool):
        if not isinstance(coil, Coil):
            raise TypeError("Incompatible type given for coil.")
        if not isinstance(value, bool):
            raise TypeError("Value must be boolean.")
        self.coil = coil
        self.value = value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, bool):
            return self.value == other
        elif isinstance(other, CoilValue):
            return self.value == other.value and self.coil == other.coil
        return False
    
    def __neq__(self, other) -> bool:
        if isinstance(other, bool):
            return self.value != other
        elif isinstance(other, CoilValue):
            return self.value != other.value or self.coil != other.coil
        return True
    
    def is_(self, other) -> bool:
        return self.__eq__(other)
    
    def is_not(self, other) -> bool:
        return self.__neq__(other)
    
    def __repr__(self) -> str:
        return "<{}.{} (0x{:02x}): {}>".format(self.coil.__class__.__name__, self.coil._name_, self.coil.value, self.value)


class RegisterValue:
    """A container class used to hold a value together with an associated register.

    Attributes:
        register(Register): register.
        value(int): register value.
    """
    def __init__(self, register:Register, value:int):
        if not isinstance(register, Register):
            raise TypeError("Incompatible type given for register.")
        if not isinstance(value, int):
            raise TypeError("Value must be integer.")
        self.register = register
        self.value = value
    
    def __index__(self) -> int:
        return self.value
    
    def __eq__(self, other) -> bool:
        if isinstance(other, int):
            return self.value == other
        elif isinstance(other, RegisterValue):
            return self.value == other.value and self.register == other.register
        return False
    
    def __neq__(self, other) -> bool:
        if isinstance(other, int):
            return self.value != other
        elif isinstance(other, RegisterValue):
            return self.value != other.value or self.register != other.register
        return True
    
    def is_(self, other) -> bool:
        return self.__eq__(other)
    
    def is_not(self, other) -> bool:
        return self.__neq__(other)
    
    def __add__(self, other) -> int:
        if isinstance(other, int):
            return self.value + other
        elif isinstance(other, RegisterValue):
            return self.value + other.value
        else:
            raise TypeError("Can only add int or RegisterValue.")
    
    def __sub__(self, other) -> int:
        if isinstance(other, int):
            return self.value - other
        elif isinstance(other, RegisterValue):
            return self.value - other.value
        else:
            raise TypeError("Can only subtract int or RegisterValue.")
    
    def __pow__(self, other) -> int:
        if isinstance(other, int):
            return self.value**2
        elif isinstance(other, RegisterValue):
            return self.value**other.value
        else:
            raise TypeError("Can only exponentiate with int or RegisterValue.")
    
    
    def __lt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value < other
        elif isinstance(other, RegisterValue):
            return self.value < other.value
        else:
            raise TypeError("Can only compare with int or RegisterValue.")
    
    def __le__(self, other) -> bool:
        if isinstance(other, int):
            return self.value <= other
        elif isinstance(other, RegisterValue):
            return self.value <= other.value
        else:
            raise TypeError("Can only compare with int or RegisterValue.")

    def __ge__(self, other) -> bool:
        if isinstance(other, int):
            return self.value >= other
        elif isinstance(other, RegisterValue):
            return self.value >= other.value
        else:
            raise TypeError("Can only compare with int or RegisterValue.")

    def __gt__(self, other) -> bool:
        if isinstance(other, int):
            return self.value > other
        elif isinstance(other, RegisterValue):
            return self.value > other.value
        else:
            raise TypeError("Can only compare with int or RegisterValue.")
    
    def __not__(self) -> int:
        return not self.value

    def __inv__(self) -> int:
        return ~self.value

    def __lshift__(self, amount:int) -> int:
        if isinstance(amount, int):
            return self.value << amount
        elif isinstance(amount, RegisterValue):
            return self.value << amount.value
        else:
            raise TypeError("Can only shift by int or RegisterValue.")

    def __rshift__(self, amount:int) -> int:
        if isinstance(amount, int):
            return self.value >> amount
        elif isinstance(amount, RegisterValue):
            return self.value >> amount.value
        else:
            raise TypeError("Can only shift by int or RegisterValue.")
    
    def __neg__(self) -> int:
        return -self.value
    
    def __mod__(self, other) -> int:
        if isinstance(other, int):
            return self.value % other
        elif isinstance(other, RegisterValue):
            return self.value % other.value
        else:
            raise TypeError("Can only divide by int or RegisterValue.")

    def __floordiv__(self, other) -> int:
        if isinstance(other, int):
            return self.value // other
        elif isinstance(other, RegisterValue):
            return self.value // other.value
        else:
            raise TypeError("Can only divide by int or RegisterValue.")

    def __mul__(self, other) -> int:
        if isinstance(other, int):
            return self.value * other
        elif isinstance(other, RegisterValue):
            return self.value * other.value
        else:
            raise TypeError("Can only multiply by int or RegisterValue.")

    def __or__(self, other) -> int:
        if isinstance(other, int):
            return self.value | other
        elif isinstance(other, RegisterValue):
            return self.value | other.value
        else:
            raise TypeError("Can only carry bitwise operations with int or RegisterValue.")

    def __and__(self, other) -> int:
        if isinstance(other, int):
            return self.value & other
        elif isinstance(other, RegisterValue):
            return self.value & other.value
        else:
            raise TypeError("Can only carry bitwise operations with int or RegisterValue.")

    def __xor__(self, other) -> int:
        if isinstance(other, int):
            return self.value ^ other
        elif isinstance(other, RegisterValue):
            return self.value ^ other.value
        else:
            raise TypeError("Can only carry bitwise operations with int or RegisterValue.")
    
    def __iadd__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value += other
        elif isinstance(other, RegisterValue):
            self.value += other.value
        else:
            raise TypeError("Can only add int or RegisterValue.")
        return self

    def __isub__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value -= other
        elif isinstance(other, RegisterValue):
            self.value -= other.value
        else:
            raise TypeError("Can only subtract int or RegisterValue.")
        return self

    def __imul__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value *= other
        elif isinstance(other, RegisterValue):
            self.value *= other.value
        else:
            raise TypeError("Can only multiply by int or RegisterValue.")
        return self

    def __ifloordiv__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value //= other
        elif isinstance(other, RegisterValue):
            self.value //= other.value
        else:
            raise TypeError("Can only divide by int or RegisterValue.")
        return self

    def __imod__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value %= other
        elif isinstance(other, RegisterValue):
            self.value %= other.value
        else:
            raise TypeError("Can only divide by int or RegisterValue.")
        return self

    def __ipow__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value **= other
        elif isinstance(other, RegisterValue):
            self.value **= other.value
        else:
            raise TypeError("Can only exponentiate with int or RegisterValue.")
        return self

    def __iand__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value &= other
        elif isinstance(other, RegisterValue):
            self.value &= other.value
        else:
            raise TypeError("Can only carry bitwise operation with int or RegisterValue.")
        return self

    def __ior__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value |= other
        elif isinstance(other, RegisterValue):
            self.value |= other.value
        else:
            raise TypeError("Can only carry bitwise operation with int or RegisterValue.")
        return self

    def __ixor__(self, other) -> 'RegisterValue':
        if isinstance(other, int):
            self.value ^= other
        elif isinstance(other, RegisterValue):
            self.value ^= other.value
        else:
            raise TypeError("Can only carry bitwise operation with int or RegisterValue.")
        return self

    def __ilshift__(self, amount) -> 'RegisterValue':
        if isinstance(amount, int):
            self.value <<= amount
        elif isinstance(amount, RegisterValue):
            self.value <<= amount.value
        else:
            raise TypeError("Can only shift by int or RegisterValue.")
        return self

    def __irshift__(self, amount) -> 'RegisterValue':
        if isinstance(amount, int):
            self.value >>= amount
        elif isinstance(amount, RegisterValue):
            self.value >>= amount.value
        else:
            raise TypeError("Can only shift by int or RegisterValue.")
        return self
    
    def to_bytes(self, n_bytes:int, endianness:str) -> bytes:
        return self.value.to_bytes(n_bytes, endianness)

    def __repr__(self) -> str:
        return "<{}.{} (0x{:04x}): {}>".format(self.register.__class__.__name__, self.register._name_, self.register.address, self.value)
    
    def __format__(self, spec:str) -> str:
        if spec[-1] in ["d", "x", "X", "f", "F", "b", "o", "e", "E", "g", "G", "n", "%"]:
            return format(self.value, spec)
        else:
            return format(self.__repr__(), spec)

