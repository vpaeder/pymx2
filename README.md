# pymx2

This is a python driver to communicate with an Omron MX2 inverter through Modbus ([manufacturer's page](https://industrial.omron.eu/en/products/mx2)). It is based on datasheet rev.2 (Jan 2013).

## Requirements

- An RS-485 adapter
- [pySerial](https://pypi.org/project/pyserial)

## What is provided

- Commands to handle low-level functions provided by the inverter:
  - Read coil status (01h)
  - Read holding register (03h)
  - Write in coil (05h)
  - Write in holding register (06h)
  - Loopback test (08h)
  - Write in coils (0Fh)
  - Write in holding registers (10h)
  - Read/write in holding registers (17h)
- A list of available coils and registers in the form of enums in mx2.enums:
  - Coil: list of coil addresses
  - ModbusRegisters: registers available only through Modbus
  - StandardFunctions: A group registers as described in datasheet pp. 90-120
  - FineTuningFunctions: B group registers (pp. 121-153)
  - IntelligentTerminalFunctions: C group registers (pp. 153-171)
  - MonitoringFunctions: D group registers (pp. 74-88)
  - MainProfileParameters: F group registers (p. 89)
  - MotorConstantsFunctions: H group registers (pp. 172-178)
  - OtherParameters: P group registers (pp. 179-190)
  - SecondMotorFunctions: registers from different groups assigned to 2nd motor configuration
- Data types to handle returned values and keep tracks of associated coils and registers:
  - CoilValue: holds a reference to a coil address and a boolean value
  - RegisterValue: holds a reference to a register address and an integer value

There are so many separate coils and registers that I didn't find appropriate to create a class method for each of them. Allowed values and units for each register can be found in the relevant datasheet pages. Register sizes are handled automatically.
An exception is made for fault monitors, for which as specific class method is provided.
Several examples are available in the [examples](examples) folder.
API documentation can be found within the code or in the *docs* folder (see [below](#api)).
Don't hesitate to report bugs [here](https://github.com/vpaeder/pymx2/issues).

## Setup

You can download a release from pypi using pip or clone this repository and install manually.

### From pypi

From command line, use:

```bash
python -m pip install pymx2
```

### From repository

From command line, use:

```bash
git clone https://github.com/vpaeder/pymx2.git
cd pymx2
python -m setup.py install
```

## Examples

See [examples](examples) folder.

## Tests

The [tests](tests) folder contains unit tests for most of the aspects of this package. To run them, use:

```bash
python -m unittest
```

## API

You can find docs in the [docs](docs) folder (generated from python docstrings). Alternatively, you can rely on python docstrings

1) either from the command line, use pydoc:

```bash
python -m pydoc mx2
```

2) or from within python:

```python
import mx2; help(mx2)
```
