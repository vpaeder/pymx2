"""Enums for MX2 driver."""

import enum

__all__ = ["FunctionCode", "ExceptionCode", "Coil", "Register", "ModbusRegisters",
           "StandardFunctions", "FineTuningFunctions", "IntelligentTerminalFunctions",
           "MonitoringFunctions", "MainProfileParameters", "MotorConstantsFunctions",
           "OtherParameters", "SecondMotorFunctions", "FaultMonitorData", "TripFactor",
           "InverterStatus", "GroupA", "GroupB", "GroupC", "GroupD", "GroupF",
           "GroupH", "GroupP"]

class FunctionCode(enum.IntEnum):
    """Function codes (2nd byte of Modbus message).
    See datasheet section B-3, p. 299."""
    ReadCoilStatus = 0x01
    ReadHoldingRegister = 0x03
    WriteInCoil = 0x05
    WriteInHoldingRegister = 0x06
    LoopbackTest = 0x08
    WriteInMultipleCoils = 0x0f
    WriteInRegisters = 0x10
    ReadWriteRegisters = 0x17


class ExceptionCode(enum.IntEnum):
    """Exception codes replied by inverter if an exception occurs
    (datasheet section B-3, p. 300)."""
    FunctionNotSupported = 0x01
    FunctionNotFound = 0x02
    InvalidDataFormat = 0x03
    OutOfBounds = 0x21
    FunctionNotAvailable = 0x22
    ReadOnlyTarget = 0x23


class Coil(enum.IntEnum):
    """Coil addresses (datasheet section B-4, p. 316)."""
    OperationCommand = 0x01
    RotationDirectionCommand = 0x02
    ExternalTrip = 0x03
    TripReset = 0x04
    IntelligentInput1 = 0x07
    IntelligentInput2 = 0x08
    IntelligentInput3 = 0x09
    IntelligentInput4 = 0x0A
    IntelligentInput5 = 0x0B
    IntelligentInput6 = 0x0C
    IntelligentInput7 = 0x0D
    OperationStatus = 0x0F
    RotationDirectionStatus = 0x10
    InverterReady = 0x11
    Running = 0x13
    ConstantSpeedReached = 0x14
    SetFrequencyOverreached = 0x15
    Overload = 0x16
    OutputDeviation = 0x17
    Alarm = 0x18
    SetFrequencyReached = 0x19
    OverTorque = 0x1A
    UnderVoltage = 0x1C
    TorqueLimited = 0x1D
    OperationTimeOver = 0x1E
    PlugInTimeOver = 0x1F
    ThermalAlarm = 0x20
    BrakeRelease = 0x26
    BrakeError = 0x27
    ZeroHzDetection = 0x28
    SpeedDeviationMaximum = 0x29
    PositioningCompleted = 0x2A
    SetFrequencyOverreached2 = 0x2B
    SetFrequencyReached2 = 0x2C
    Overload2 = 0x2D
    AnalogVoltageIODisconnected = 0x2E
    AnalogCurrentIODisconnected = 0x2F
    PIDFeedbackComparison = 0x32
    CommunicationTrainDisconnection = 0x33
    LogicalOperationResult1 = 0x34
    LogicalOperationResult2 = 0x35
    LogicalOperationResult3 = 0x36
    CapacitorLifeWarning = 0x3A
    CoolingFanSpeedDrop = 0x3B
    StartingContactSignal = 0x3C
    HeatSinkOverheatWarning = 0x3D
    LowCurrentIndicator = 0x3E
    GeneralOutput1 = 0x3F
    GeneralOutput2 = 0x40
    GeneralOutput3 = 0x41
    InverterReadyOutput = 0x45
    ForwardRotation = 0x46
    ReverseRotation = 0x47
    MajorFailure = 0x48
    DataWritingInProgress = 0x49
    CRCError = 0x4A
    Overrun = 0x4B
    FramingError = 0x4C
    ParityError = 0x4D
    SumCheckError = 0x4E
    WindowComparatorVoltage = 0x50
    WindowComparatorCurrent = 0x51
    OptionDisconnection = 0x53
    FrequencyCommandSource = 0x54
    RunCommandSource = 0x55
    SecondMotorSelected = 0x56
    GateSuppressMonitor = 0x58

    def __repr__(self) -> str:
        return "<{}.{}: 0x{:02x}>".format(self.__class__.__name__, self._name_, self.value)

    def next(self, n_items=1):
        if n_items<0:
            raise ValueError("Item count must be positive or zero.")
        if n_items==0:
            return [self]
        i_start = self._member_names_.index(self.name)+1
        i_end = min(len(self._member_names_), i_start + n_items)
        return [self._member_map_[self._member_names_[i]] for i in range(i_start, i_end)]
    
    @staticmethod
    def contains(value:int):
        for k in Coil._member_map_:
            if Coil._member_map_[k].value == value:
                return Coil._member_map_[k]
        return None


class Register(enum.Enum):
    """Base enum class for register address."""

    def __init__(self, address:int, n_words:int=1) -> None:
        """Constructor.

        Parameters:
            address(int): register address (between 0 and 0xffff).
            n_words(int): number of words; must be larger than 0 (default: 1).
        
        Raises:
            ValueError: if address is out of bounds.
            ValueError: if n_words is less than 1.
        """
        if address<0 or address>0xffff:
            raise ValueError("Register address out of bounds.")
        if n_words<=0:
            raise ValueError("Number of words must be strictly positive.")
        self.address = address
        self.n_words = n_words
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Register):
            return other.address == self.address and other.n_words == self.n_words
        elif isinstance(other, int):
            return other == self.address
        else:
            return False
    
    def __add__(self, other) -> int:
        if isinstance(other, int):
            candidates = self.next(other)
            for c in candidates:
                if c.address == self.address + other:
                    return c
            return self.address + other
        else:
            raise TypeError("Register address can only be incremented by integer values.")

    def __sub__(self, other) -> int:
        if isinstance(other, int):
            return self.address - other
        else:
            raise TypeError("Register address can only be decremented by integer values.")
    
    def __le__(self, other) -> bool:
        if isinstance(other, Register):
            return self.address <= other.address
        elif isinstance(other, int):
            return self.address <= other

    def __lt__(self, other) -> bool:
        if isinstance(other, Register):
            return self.address < other.address
        elif isinstance(other, int):
            return self.address < other

    def __gt__(self, other) -> bool:
        if isinstance(other, Register):
            return self.address > other.address
        elif isinstance(other, int):
            return self.address > other

    def __ge__(self, other) -> bool:
        if isinstance(other, Register):
            return self.address >= other.address
        elif isinstance(other, int):
            return self.address >= other
    
    def __lshift__(self, amount:int) -> int:
        if isinstance(amount, int):
            return self.address << amount
        else:
            raise TypeError("Register address can only be shifted by integer values.")

    def __rshift__(self, amount:int) -> int:
        if isinstance(amount, int):
            return self.address >> amount
        else:
            raise TypeError("Register address can only be shifted by integer values.")

    def __and__(self, value:int) -> int:
        if isinstance(value, int):
            return self.address & value
        else:
            raise TypeError("Bitwise AND operation on register address can only occur with integer values.")

    def __or__(self, value:int) -> int:
        if isinstance(value, int):
            return self.address | value
        else:
            raise TypeError("Bitwise OR operation on register address can only occur with integer values.")

    def __repr__(self) -> str:
        return "<{}.{}: (0x{:02x}, {})>".format(self.__class__.__name__, self._name_, self.address, self.n_words)
    
    def next(self, n_items=1):
        if n_items<0:
            raise ValueError("Item count must be positive or zero.")
        if n_items==0:
            return [self]
        i_start = self._member_names_.index(self.name)+1
        i_end = min(len(self._member_names_), i_start + n_items)
        return [self._member_map_[self._member_names_[i]] for i in range(i_start, i_end)]

    @staticmethod
    def contains(cls, value:int):
        for k in cls._member_map_:
            if cls._member_map_[k].address == value:
                return cls._member_map_[k]
        return None


class ModbusRegisters(Register):
    """Modbus-only registers. These registers aren't accessible
    through the keypad interface (datasheet section B-4, pp. 318 and 320)."""
    def contains(value:int):
        return Register.contains(ModbusRegisters, value)
    InverterStatusA = 0x0003
    InverterStatusB = 0x0004
    InverterStatusC = 0x0005
    PIDFeedback = 0x0006
    WriteToEEPROM = 0x0900
    EEPROMWriteMode = 0x0902


class StandardFunctions(Register):
    """Standard function group. See datasheet
    sections 3-5 (pp. 90-120) and B-4 (pp. 324-327)."""
    def contains(value:int):
        return Register.contains(StandardFunctions, value)
    # A group
    FrequencyReferenceSelection = 0x1201
    A001 = 0x1201
    RunCommandSelection = 0x1202
    A002 = 0x1202
    BaseFrequency = 0x1203
    A003 = 0x1203
    MaximumFrequency = 0x1204
    A004 = 0x1204
    IOVoltageCurrentSelection = 0x1205
    A005 = 0x1205
    VoltageStartFrequency = (0x120B, 2)
    A011 = (0x120B, 2)
    VoltageEndFrequency = (0x120D, 2)
    A012 = (0x120D, 2)
    VoltageStartRatio = 0x120F
    A013 = 0x120F
    VoltageEndRatio = 0x1210
    A014 = 0x1210
    VoltageStartSelection = 0x1211
    A015 = 0x1211
    ExternalFrequencyFilterTimeConstant = 0x1212
    A016 = 0x1212
    DriveProgramming = 0x1213
    A017 = 0x1213
    MultiStepSpeedSelection = 0x1215
    A019 = 0x1215
    MultiStepSpeedReference0 = (0x1216, 2)
    A020 = (0x1216, 2)
    MultiStepSpeedReference1 = (0x1218, 2)
    A021 = (0x1218, 2)
    MultiStepSpeedReference2 = (0x121A, 2)
    A022 = (0x121A, 2)
    MultiStepSpeedReference3 = (0x121C, 2)
    A023 = (0x121C, 2)
    MultiStepSpeedReference4 = (0x121E, 2)
    A024 = (0x121E, 2)
    MultiStepSpeedReference5 = (0x1220, 2)
    A025 = (0x1220, 2)
    MultiStepSpeedReference6 = (0x1222, 2)
    A026 = (0x1222, 2)
    MultiStepSpeedReference7 = (0x1224, 2)
    A027 = (0x1224, 2)
    MultiStepSpeedReference8 = (0x1226, 2)
    A028 = (0x1226, 2)
    MultiStepSpeedReference9 = (0x1228, 2)
    A029 = (0x1228, 2)
    MultiStepSpeedReference10 = (0x122A, 2)
    A030 = (0x122A, 2)
    MultiStepSpeedReference11 = (0x122C, 2)
    A031 = (0x122C, 2)
    MultiStepSpeedReference12 = (0x122E, 2)
    A032 = (0x122E, 2)
    MultiStepSpeedReference13 = (0x1230, 2)
    A033 = (0x1230, 2)
    MultiStepSpeedReference14 = (0x1232, 2)
    A034 = (0x1232, 2)
    MultiStepSpeedReference15 = (0x1234, 2)
    A035 = (0x1234, 2)
    JoggingFrequency = 0x1238
    A038 = 0x1238
    JoggingStopSelection = 0x1239
    A039 = 0x1239
    TorqueBoostSelection = 0x123B
    A041 = 0x123B
    ManualTorqueBoostVoltage = 0x123C
    A042 = 0x123C
    ManualTorqueBoostFrequency = 0x123D
    A043 = 0x123D
    VFCharacteristicsSelection = 0x123E
    A044 = 0x123E
    OutputVoltageGain = 0x123F
    A045 = 0x123F
    AutomaticTorqueBoostVoltageCompensationGain = 0x1240
    A046 = 0x1240
    AutomaticTorqueBoostSlipCompensationGain = 0x1241
    A047 = 0x1241
    DCInjectionBrakingEnable = 0x1245
    A051 = 0x1245
    DCInjectionBrakingFrequency = 0x1246
    A052 = 0x1246
    DCInjectionBrakingDelayTime = 0x1247
    A053 = 0x1247
    DCInjectionBrakingPower = 0x1248
    A054 = 0x1248
    DCInjectionBrakingTime = 0x1249
    A055 = 0x1249
    DCInjectionBrakingMethodSelection = 0x124A
    A056 = 0x124A
    StartupDCInjectionBrakingPower = 0x124B
    A057 = 0x124B
    StartupDCInjectionBrakingTime = 0x124C
    A058 = 0x124C
    DCInjectionBrakingCarrierFrequency = 0x124D
    A059 = 0x124D
    FrequencyUpperLimit = (0x124F, 2)
    A061 = (0x124F, 2)
    FrequencyLowerLimit = (0x1251, 2)
    A062 = (0x1251, 2)
    JumpFrequency1 = (0x1253, 2)
    A063 = (0x1253, 2)
    JumpFrequencyWidth1 = 0x1255
    A064 = 0x1255
    JumpFrequency2 = (0x1256, 2)
    A065 = (0x1256, 2)
    JumpFrequencyWidth2 = 0x1258
    A066 = 0x1258
    JumpFrequency3 = (0x1259, 2)
    A067 = (0x1259, 2)
    JumpFrequencyWidth3 = 0x125B
    A068 = 0x125B
    AccelerationStopFrequency = (0x125C, 2)
    A069 = (0x125C, 2)
    AccelerationStopTime = 0x125E
    A070 = 0x125E
    PIDSelection = 0x125F
    A071 = 0x125F
    PIDPGain = 0x1260
    A072 = 0x1260
    PIDIGain = 0x1261
    A073 = 0x1261
    PIDDGain = 0x1262
    A074 = 0x1262
    PIDScale = 0x1263
    A075 = 0x1263
    PIDFeedbackSelection = 0x1264
    A076 = 0x1264
    ReversePIDFunction = 0x1265
    A077 = 0x1265
    PIDOutputLimitFunction = 0x1266
    A078 = 0x1266
    PIDFeedForwardSelection = 0x1267
    A079 = 0x1267
    AVRSelection = 0x1269
    A081 = 0x1269
    AVRVoltageSelection = 0x126A
    A082 = 0x126A
    AVRFilterTimeConstant = 0x126B
    A083 = 0x126B
    AVRDecelerationGain = 0x126C
    A084 = 0x126C
    EnergySavingOperationMode = 0x126D
    A085 = 0x126D
    EnergySavingResponseAccuracyAdjustment = 0x126E
    A086 = 0x126E
    AccelerationTime2 = (0x1274, 2)
    A092 = (0x1274, 2)
    DecelerationTime2 = (0x1276, 2)
    A093 = (0x1276, 2)
    MethodToSwitchToAcc2Dec2 = 0x1278
    A094 = 0x1278
    Acc1ToAcc2FrequencyTransitionPoint = (0x1279, 2)
    A095 = (0x1279, 2)
    Dec1ToDec2FrequencyTransitionPoint = (0x127B, 2)
    A096 = (0x127B, 2)
    AccelerationCurveSelection = 0x127D
    A097 = 0x127D
    DecelerationCurveSelection = 0x127E
    A098 = 0x127E
    CurrentInputActiveRangeStartFrequency = (0x1281, 2)
    A101 = (0x1281, 2)
    CurrentInputActiveRangeEndFrequency = (0x1283, 2)
    A102 = (0x1283, 2)
    CurrentInputActiveRangeStartRatio = 0x1285
    A103 = 0x1285
    CurrentInputActiveRangeEndRatio = 0x1286
    A104 = 0x1286
    CurrentInputStartFrequencyEnable = 0x1287
    A105 = 0x1287
    AccelerationCurveParameter = 0x12A5
    A131 = 0x12A5
    DecelerationCurveParameter = 0x12A6
    A132 = 0x12A6
    OperationFrequencyInputASelection = 0x12AF
    A141 = 0x12AF
    OperationFrequencyInputBSelection = 0x12B0
    A142 = 0x12B0
    OperationSelection = 0x12B1
    A143 = 0x12B1
    FrequencyAdditionAmount = (0x12B3, 2)
    A145 = (0x12B3, 2)
    FrequencyAdditionDirection = 0x12B5
    A146 = 0x12B5
    ELSCurveRatio1DuringAcceleration = 0x12B9
    A150 = 0x12B9
    ELSCurveRatio2DuringAcceleration = 0x12BA
    A151 = 0x12BA
    ELSCurveRatio1DuringDeceleration = 0x12BB
    A152 = 0x12BB
    ELSCurveRatio2DuringDeceleration = 0x12BC
    A153 = 0x12BC
    DecelerationHoldFrequency = (0x12BD, 2)
    A154 = (0x12BD, 2)
    DecelerationHoldTime = 0x12BF
    A155 = 0x12BF
    PIDSleepFunctionActionThreshold = (0x12C0, 2)
    A156 = (0x12C0, 2)
    PIDSleepFunctionActionDelayTime = 0x12C2
    A157 = 0x12C2
    VRInputActiveRangeStartFrequency = (0x12C6, 2)
    A161 = (0x12C6, 2)
    VRInputActiveRangeEndFrequency = (0x12C8, 2)
    A162 = (0x12C8, 2)
    VRInputActiveRangeStartCurrent = 0x12CA
    A163 = 0x12CA
    VRInputActiveRangeEndVoltage = 0x12CB
    A164 = 0x12CB
    VRInputStartFrequencyEnable = 0x12CC
    A165 = 0x12CC

GroupA = StandardFunctions


class FineTuningFunctions(Register):
    """Fine tuning function group. See datasheet
    sections 3-6 (pp. 121-153) and B-4 (pp. 328-331)."""
    def contains(value:int):
        return Register.contains(FineTuningFunctions, value)
    # B group
    RetrySelection = 0x1301
    B001 = 0x1301
    AllowableMomentaryPowerInterruptionTime = 0x1302
    B002 = 0x1302
    RetryWaitTime = 0x1303
    B003 = 0x1303
    UndervoltageTripDuringStopSelection = 0x1304
    B004 = 0x1304
    MomentaryPowerInterruptionRetryTimeSelection = 0x1305
    B005 = 0x1305
    FrequencyMatchingLowerLimit = (0x1307, 2)
    B007 = (0x1307, 2)
    TripRetrySelection = 0x1309
    B008 = 0x1309
    OvervoltageRetryTimeSelection = 0x130B
    B010 = 0x130B
    TripRetryWaitTime = 0x130C
    B011 = 0x130C
    ElectronicThermalLevel = 0x130D
    B012 = 0x130D
    ElectronicThermalCharacteristicsSelection = 0x130E
    B013 = 0x130E
    ElectronicThermalFrequency1 = 0x1310
    B015 = 0x1310
    ElectronicThermalCurrent1 = 0x1311
    B016 = 0x1311
    ElectronicThermalFrequency2 = 0x1312
    B017 = 0x1312
    ElectronicThermalCurrent2 = 0x1313
    B018 = 0x1313
    ElectronicThermalFrequency3 = 0x1314
    B019 = 0x1314
    ElectronicThermalCurrent3 = 0x1315
    B020 = 0x1315
    OverloadLimitSelection = 0x1316
    B021 = 0x1316
    OverloadLimitLevel = 0x1317
    B022 = 0x1317
    OverloadLimitParameter = 0x1318
    B023 = 0x1318
    OverloadLimitSelection2 = 0x1319
    B024 = 0x1319
    OverloadLimitLevel2 = 0x131A
    B025 = 0x131A
    OverloadLimitParameter2 = 0x131B
    B026 = 0x131B
    OvercurrentSuppressionFunction = 0x131C
    B027 = 0x131C
    ActiveFrequencyMatchingRestartLevel = 0x131D
    B028 = 0x131D
    ActiveFrequencyMatchingRestartParameter = 0x131E
    B029 = 0x131E
    StartingFrequencyAtActiveFrequencyMatchingRestart = 0x131F
    B030 = 0x131F
    SoftLockSelection = 0x1320
    B031 = 0x1320
    MotorCableLengthParameter = 0x1322
    B033 = 0x1322
    PowerOnTimeSetting = (0x1323, 2)
    B034 = (0x1323, 2)
    RotationDirectionLimitSelection = 0x1325
    B035 = 0x1325
    ReducedVoltageStartupSelection = 0x1326
    B036 = 0x1326
    DisplaySelection = 0x1327
    B037 = 0x1327
    InitialScreenSelection = 0x1328
    B038 = 0x1328
    UserParameterAutomaticSettingFunctionSelection = 0x1329
    B039 = 0x1329
    TorqueLimitSelection = 0x132A
    B040 = 0x132A
    TorqueLimit1 = 0x132B
    B041 = 0x132B
    TorqueLimit2 = 0x132C
    B042 = 0x132C
    TorqueLimit3 = 0x132D
    B043 = 0x132D
    TorqueLimit4 = 0x132E
    B044 = 0x132E
    TorqueLADSTOPSelection = 0x132F
    B045 = 0x132F
    ReverseRotationPreventionSelection = 0x1330
    B046 = 0x1330
    DualRateSelection = 0x1333
    B049 = 0x1333
    NonStopFunctionOnPowerInterruptionSelection = 0x1334
    B050 = 0x1334
    StartingVoltageOfNonStopFunction = 0x1335
    B051 = 0x1335
    StopDecelerationLevelOfNonStopFunction = 0x1336
    B052 = 0x1336
    DecelerationTimeOfNonStopFunction = (0x1337, 2)
    B053 = (0x1337, 2)
    DecelerationStartingWidthOfNonStopFunction = 0x1339
    B054 = 0x1339
    WindowComparatorUpperVoltageLevel = 0x133F
    B060 = 0x133F
    WindowComparatorLowerVoltageLevel = 0x1340
    B061 = 0x1340
    WindowComparatorVoltageHysteresisWidth = 0x1341
    B062 = 0x1341
    WindowComparatorUpperCurrentLevel = 0x1342
    B063 = 0x1342
    WindowComparatorLowerCurrentLevel = 0x1343
    B064 = 0x1343
    WindowComparatorCurrentHysteresisWidth = 0x1344
    B065 = 0x1344
    AnalogVoltageLevelAtDisconnection = 0x1349
    B070 = 0x1349
    AnalogCurrentLevelAtDisconnection = 0x134A
    B071 = 0x134A
    AmbientTemperature = 0x134E
    B075 = 0x134E
    IntegratedPowerClear = 0x1351
    B078 = 0x1351
    IntegratedPowerDisplayGain = 0x1352
    B079 = 0x1352
    StartingFrequency = 0x1355
    B082 = 0x1355
    CarrierFrequency = 0x1356
    B083 = 0x1356
    InitializationSelection = 0x1357
    B084 = 0x1357
    InitializationParameterSelection = 0x1358
    B085 = 0x1358
    FrequencyConversionCoefficient = 0x1359
    B086 = 0x1359
    StopKeySelection = 0x135A
    B087 = 0x135A
    FreeRunStopSelection = 0x135B
    B088 = 0x135B
    AutomaticCarrierFrequencyReduction = 0x135C
    B089 = 0x135C
    RateOfRegenerativeBrakingFunction = 0x135D
    B090 = 0x135D
    StopSelection = 0x135E
    B091 = 0x135E
    CoolingFanControl = 0x135F
    B092 = 0x135F
    ClearElapsedTimeOfCoolingFan = 0x1360
    B093 = 0x1360
    InitializationTargetData = 0x1361
    B094 = 0x1361
    RegenerativeBrakingOperation = 0x1362
    B095 = 0x1362
    RegenerativeBrakingONLevel = 0x1363
    B096 = 0x1363
    BRDResistor = 0x1364
    B097 = 0x1364
    FreeVfFrequency1 = 0x1367
    B100 = 0x1367
    FreeVfVoltage1 = 0x1368
    B101 = 0x1368
    FreeVfFrequency2 = 0x1369
    B102 = 0x1369
    FreeVfVoltage2 = 0x136A
    B103 = 0x136A
    FreeVfFrequency3 = 0x136B
    B104 = 0x136B
    FreeVfVoltage3 = 0x136C
    B105 = 0x136C
    FreeVfFrequency4 = 0x136D
    B106 = 0x136D
    FreeVfVoltage4 = 0x136E
    B107 = 0x136E
    FreeVfFrequency5 = 0x136F
    B108 = 0x136F
    FreeVfVoltage5 = 0x1370
    B109 = 0x1370
    FreeVfFrequency6 = 0x1371
    B110 = 0x1371
    FreeVfVoltage6 = 0x1372
    B111 = 0x1372
    FreeVfFrequency7 = 0x1373
    B112 = 0x1373
    FreeVfVoltage7 = 0x1374
    B113 = 0x1374
    BrakeControlSelection = 0x137B
    B120 = 0x137B
    BrakeWaitTimeForRelease = 0x137C
    B121 = 0x137C
    BrakeWaitTimeForAcceleration = 0x137D
    B122 = 0x137D
    BrakeWaitTimeForStopping = 0x137E
    B123 = 0x137E
    BrakeWaitTimeForConfirmation = 0x137F
    B124 = 0x137F
    BrakeReleaseFrequency = 0x1380
    B125 = 0x1380
    BrakeReleaseCurrent = 0x1381
    B126 = 0x1381
    BrakeInputFrequency = 0x1382
    B127 = 0x1382
    OvervoltageProtectionDuringDeceleration = 0x1385
    B130 = 0x1385
    OvervoltageProtectionLevelDuringDeceleration = 0x1386
    B131 = 0x1386
    OvervoltageProtectionParameter = 0x1387
    B132 = 0x1387
    OvervoltageProtectionProportionalGain = 0x1388
    B133 = 0x1388
    OvervoltageProtectionIntegralGain = 0x1389
    B134 = 0x1389
    GSInputMode = 0x1394
    B145 = 0x1394
    DisplayExternalOperatorConnected = 0x139A
    B150 = 0x139A
    FirstDualMonitorParameter = 0x13A3
    B160 = 0x13A3
    SecondDualMonitorParameter = 0x13A4
    B161 = 0x13A4
    FrequencySetInMonitoring = 0x13A6
    B163 = 0x13A6
    AutoReturnInitialDisplay = 0x13A7
    B164 = 0x13A7
    ExternalOperatorDisconnectionAction = 0x13A8
    B165 = 0x13A8
    DataReadWriteSelection = 0x13A9
    B166 = 0x13A9
    InverterModeSelection = 0x13AE
    B171 = 0x13AE
    InitializeTrigger = 0x13B7
    B180 = 0x13B7
    ThermalDecrementMode = 0x13C6
    B910 = 0x13C6
    ThermalDecrementTime = (0x13C7, 2)
    B911 = (0x13C7, 2)
    ThermalDecrementTimeConstant = (0x13C9, 2)
    B912 = (0x13C9, 2)
    ThermalAccumulatorGain = 0x13CB
    B913 = 0x13CB

GroupB = FineTuningFunctions


class IntelligentTerminalFunctions(Register):
    """Intelligent terminal function group. See datasheet
    sections 3-7 (pp. 153-171) and B-4 (pp. 332-336)."""
    def contains(value:int):
        return Register.contains(IntelligentTerminalFunctions, value)
    # C group
    MultiFunctionInput1Function = 0x1401
    C001 = 0x1401
    MultiFunctionInput2Function = 0x1402
    C002 = 0x1402
    MultiFunctionInput3Function = 0x1403
    C003 = 0x1403
    MultiFunctionInput4Function = 0x1404
    C004 = 0x1404
    MultiFunctionInput5Function = 0x1405
    C005 = 0x1405
    MultiFunctionInput6Function = 0x1406
    C006 = 0x1406
    MultiFunctionInput7Function = 0x1407
    C007 = 0x1407
    MultiFunctionInput1Type = 0x140B
    C011 = 0x140B
    MultiFunctionInput2Type = 0x140C
    C012 = 0x140C
    MultiFunctionInput3Type = 0x140D
    C013 = 0x140D
    MultiFunctionInput4Type = 0x140E
    C014 = 0x140E
    MultiFunctionInput5Type = 0x140F
    C015 = 0x140F
    MultiFunctionInput6Type = 0x1410
    C016 = 0x1410
    MultiFunctionInput7Type = 0x1411
    C017 = 0x1411
    MultiFunctionOutput11Function = 0x1415
    C021 = 0x1415
    MultiFunctionOutput12Function = 0x1416
    C022 = 0x1416
    RelayOutputFunction = 0x141A
    C026 = 0x141A
    EOTerminalFunction = 0x141B
    C027 = 0x141B
    AMTerminalFunction = 0x141C
    C028 = 0x141C
    CurrentMonitorReferenceValue = 0x141E
    C030 = 0x141E
    MultiFunctionOutput11Type = 0x141F
    C031 = 0x141F
    MultiFunctionOutput12Type = 0x1420
    C032 = 0x1420
    RelayOutputType = 0x1424
    C036 = 0x1424
    LightLoadSignalOutputMode = 0x1426
    C038 = 0x1426
    LightLoadDetectionLevel = 0x1427
    C039 = 0x1427
    OverloadWarningSignalOutputMode = 0x1428
    C040 = 0x1428
    OverloadWarningLevel = 0x1429
    C041 = 0x1429
    TargetFrequencyDuringAcceleration = (0x142A, 2)
    C042 = (0x142A, 2)
    TargetFrequencyDuringDeceleration = (0x142C, 2)
    C043 = (0x142C, 2)
    PIDDeviationExcessiveLevel = 0x142E
    C044 = 0x142E
    TargetFrequencyDuringAcceleration2 = (0x142F, 2)
    C045 = (0x142F, 2)
    TargetFrequencyDuringDeceleration2 = (0x1431, 2)
    C046 = (0x1431, 2)
    EOOutputPulseTrainScaleConversion = 0x1433
    C047 = 0x1433
    PIDFeedbackUpperLimit = 0x1438
    C052 = 0x1438
    PIDFeedbackLowerLimit = 0x1439
    C053 = 0x1439
    TorqueModeSelection = 0x143A
    C054 = 0x143A
    ForwardPowerRunningOvertorqueLevel = 0x143B
    C055 = 0x143B
    ReverseRegenerationOvertorqueLevel = 0x143C
    C056 = 0x143C
    ReversePowerRunningOvertorqueLevel = 0x143D
    C057 = 0x143D
    ForwardRegenerationOvertorqueLevel = 0x143E
    C058 = 0x143E
    TorqueSignalOutputMode = 0x143F
    C059 = 0x143F
    ThermalWarningLevel = 0x1441
    C061 = 0x1441
    ZeroHzDetectionLevel = 0x1443
    C063 = 0x1443
    FinOverheatWarningLevel = 0x1444
    C064 = 0x1444
    BaudRate = 0x144B
    C071 = 0x144B
    DeviceID = 0x144C
    C072 = 0x144C
    CommunicationParity = 0x144E
    C074 = 0x144E
    CommunicationStopBits = 0x144F
    C075 = 0x144F
    CommunicationErrorEffect = 0x1450
    C076 = 0x1450
    CommunicationErrorTimeout = 0x1451
    C077 = 0x1451
    CommunicationWaitTime = 0x1452
    C078 = 0x1452
    OAdjustment = 0x1455
    C081 = 0x1455
    OIAdjustment = 0x1456
    C082 = 0x1456
    ThermistorAdjustment = 0x1459
    C085 = 0x1459
    DebugMode = 0x145F
    C091 = 0x145F
    CommunicationSelection = 0x1464
    C096 = 0x1464
    EzCOMMasterStartAddress = 0x1466
    C098 = 0x1466
    EzCOMMasterEndAddress = 0x1467
    C099 = 0x1467
    EzCOMStartingTrigger = 0x1468
    C100 = 0x1468
    UpDownButtonSetting = 0x1469
    C101 = 0x1469
    ResetButtonSetting = 0x146A
    C102 = 0x146A
    RestartFrequencyMatchingSelection = 0x146B
    C103 = 0x146B
    UpDownButtonClearMode = 0x146C
    C104 = 0x146C
    EOGain = 0x146D
    C105 = 0x146D
    AMGain = 0x146E
    C106 = 0x146E
    AMBias = 0x1471
    C109 = 0x1471
    OverloadWarningLevel2 = 0x1473
    C111 = 0x1473
    Output11OnDelay = 0x1486
    C130 = 0x1486
    Output11OffDelay = 0x1487
    C131 = 0x1487
    Output12OnDelay = 0x1488
    C132 = 0x1488
    Output12OffDelay = 0x1489
    C133 = 0x1489
    RelayOutputOnDelay = 0x1490
    C140 = 0x1490
    RelayOutputOffDelay = 0x1491
    C141 = 0x1491
    LogicOutputSignal1Selection1 = 0x1492
    C142 = 0x1492
    LogicOutputSignal1Selection2 = 0x1493
    C143 = 0x1493
    LogicOutputSignal1OperatorSelection = 0x1494
    C144 = 0x1494
    LogicOutputSignal2Selection1 = 0x1495
    C145 = 0x1495
    LogicOutputSignal2Selection2 = 0x1496
    C146 = 0x1496
    LogicOutputSignal2OperatorSelection = 0x1497
    C147 = 0x1497
    LogicOutputSignal3Selection1 = 0x1498
    C148 = 0x1498
    LogicOutputSignal3Selection2 = 0x1499
    C149 = 0x1499
    LogicOutputSignal3OperatorSelection = 0x149A
    C150 = 0x149A
    InputTerminalResponseTime1 = 0x14A4
    C160 = 0x14A4
    InputTerminalResponseTime2 = 0x14A5
    C161 = 0x14A5
    InputTerminalResponseTime3 = 0x14A6
    C162 = 0x14A6
    InputTerminalResponseTime4 = 0x14A7
    C163 = 0x14A7
    InputTerminalResponseTime5 = 0x14A8
    C164 = 0x14A8
    InputTerminalResponseTime6 = 0x14A9
    C165 = 0x14A9
    InputTerminalResponseTime7 = 0x14AA
    C166 = 0x14AA
    MultiStepSpeedPositionDeterminationTime = 0x14AD
    C169 = 0x14AD

GroupC = IntelligentTerminalFunctions


class MonitoringFunctions(Register):
    """Intelligent terminal function group. See datasheet
    sections 3-3 (pp. 74-88) and B-4 (pp. 319-320 and 322-323)."""
    def contains(value:int):
        return Register.contains(MonitoringFunctions, value)
    # D group
    OutputFrequency = (0x1001, 2)
    D001 = (0x1001, 2)
    OutputCurrent = 0x1003
    D002 = 0x1003
    RotationDirection = 0x1004
    D003 = 0x1004
    PIDFeedbackValue = (0x1005, 2)
    D004 = (0x1005, 2)
    MultiFunctionInputs = 0x1007
    D005 = 0x1007
    MultiFunctionOutputs = 0x1008
    D006 = 0x1008
    ConvertedOutputFrequency = (0x1009, 2)
    D007 = (0x1009, 2)
    RealFrequency = (0x100B, 2)
    D008 = (0x100B, 2)
    TorqueReference = 0x100D
    D009 = 0x100D
    TorqueBias = 0x100E
    D010 = 0x100E
    OutputTorque = 0x1010
    D012 = 0x1010
    OutputVoltage = 0x1011
    D013 = 0x1011
    InputPower = 0x1012
    D014 = 0x1012
    WattHour = (0x1013, 2)
    D015 = (0x1013, 2)
    TotalRunTime = (0x1015, 2)
    D016 = (0x1015, 2)
    PowerOnTime = (0x1017, 2)
    D017 = (0x1017, 2)
    FinTemperature = 0x1019
    D018 = 0x1019
    LifeAssessment = 0x101D
    D022 = 0x101D
    ProgramCounter = 0x101E
    D023 = 0x101E
    ProgramNumber = 0x101F
    D024 = 0x101F
    DriveProgramming0 = (0x102E, 2)
    D025 = (0x102E, 2)
    DriveProgramming1 = (0x1030, 2)
    D026 = (0x1030, 2)
    DriveProgramming2 = (0x1032, 2)
    D027 = (0x1032, 2)
    PositionCommand = (0x1036, 2)
    D029 = (0x1036, 2)
    CurrentPosition = (0x1038, 2)
    D030 = (0x1038, 2)
    InverterMode = 0x1057
    D060 = 0x1057
    FrequencySource = 0x1059
    D062 = 0x1059
    RunSource = 0x105A
    D063 = 0x105A
    FaultFrequencyMonitor = 0x0011
    D080 = 0x0011
    FaultMonitor1 = 0x0012
    FaultMonitor1Factor = 0x0012
    D081 = 0x0012
    FaultMonitor1InverterStatus = 0x0013
    FaultMonitor1Frequency = (0x0014, 2)
    FaultMonitor1Current = 0x0016
    FaultMonitor1Voltage = 0x0017
    FaultMonitor1RunningTime = (0x0018, 2)
    FaultMonitor1PowerOnTime = (0x001A, 2)
    FaultMonitor2 = 0x001C
    FaultMonitor2Factor = 0x001C
    D082 = 0x001C
    FaultMonitor2InverterStatus = 0x001D
    FaultMonitor2Frequency = (0x001E, 2)
    FaultMonitor2Current = 0x0020
    FaultMonitor2Voltage = 0x0021
    FaultMonitor2RunningTime = (0x0022, 2)
    FaultMonitor2PowerOnTime = (0x0024, 2)
    FaultMonitor3 = 0x0026
    FaultMonitor3Factor = 0x0026
    D083 = 0x0026
    FaultMonitor3InverterStatus = 0x0027
    FaultMonitor3Frequency = (0x0028, 2)
    FaultMonitor3Current = 0x002A
    FaultMonitor3Voltage = 0x002B
    FaultMonitor3RunningTime = (0x002C, 2)
    FaultMonitor3PowerOnTime = (0x002E, 2)
    FaultMonitor4 = 0x0030
    FaultMonitor4Factor = 0x0030
    D084 = 0x0030
    FaultMonitor4InverterStatus = 0x0031
    FaultMonitor4Frequency = (0x0032, 2)
    FaultMonitor4Current = 0x0034
    FaultMonitor4Voltage = 0x0035
    FaultMonitor4RunningTime = (0x0036, 2)
    FaultMonitor4PowerOnTime = (0x0038, 2)
    FaultMonitor5 = 0x003A
    FaultMonitor5Factor = 0x003A
    D085 = 0x003A
    FaultMonitor5InverterStatus = 0x003B
    FaultMonitor5Frequency = (0x003C, 2)
    FaultMonitor5Current = 0x003E
    FaultMonitor5Voltage = 0x003F
    FaultMonitor5RunningTime = (0x0040, 2)
    FaultMonitor5PowerOnTime = (0x0042, 2)
    FaultMonitor6 = 0x0044
    FaultMonitor6Factor = 0x0044
    D086 = 0x0044
    FaultMonitor6InverterStatus = 0x0045
    FaultMonitor6Frequency = (0x0046, 2)
    FaultMonitor6Current = 0x0048
    FaultMonitor6Voltage = 0x0049
    FaultMonitor6RunningTime = (0x004A, 2)
    FaultMonitor6PowerOnTime = (0x004C, 2)
    WarningMonitor = 0x004E
    D090 = 0x004E
    DCVoltage = 0x1026
    D102 = 0x1026
    RegenerativeBrakingLoadRate = 0x1027
    D103 = 0x1027
    ElectronicThermalMonitor = 0x1028
    D104 = 0x1028
    AnalogInputO = 0x10A1
    D130 = 0x10A1
    AnalogInputOI = 0x10A2
    D131 = 0x10A2
    PulseTrainInput = 0x10A4
    D133 = 0x10A4
    PIDDeviation = 0x10A6
    D153 = 0x10A6
    PIDOutput = 0x10A8
    D155 = 0x10A8

GroupD = MonitoringFunctions


class MainProfileParameters(Register):
    """Main profile parameters group. See datasheet
    sections 3-4 (p. 89) and B-4 (pp. 319-320, 322-323 and 344)."""
    def contains(value:int):
        return Register.contains(MainProfileParameters, value)
    # F group
    OutputFrequency = (0x0001, 2)
    F001 = (0x0001, 2)
    AccelerationTime1 = (0x1103, 2)
    F002 = (0x1103, 2)
    DecelerationTime1 = (0x1105, 2)
    F003 = (0x1105, 2)
    OperatorRotationDirection = 0x1107
    F004 = 0x1107
    SecondAccelerationTime1 = (0x2103, 2)
    F202 = (0x2103, 2)
    SecondDecelerationTime1 = (0x2105, 2)
    F203 = (0x2105, 2)

GroupF = MainProfileParameters


class MotorConstantsFunctions(Register):
    """Motor constants function group. See datasheet
    sections 3-8 (pp. 172-178) and B-4 (pp. 337-338)."""
    def contains(value:int):
        return Register.contains(MotorConstantsFunctions, value)
    # H group
    AutoTuningSelection = 0x1501
    H001 = 0x1501
    MotorParameterSelection = 0x1502
    H002 = 0x1502
    MotorCapacitySelection = 0x1503
    H003 = 0x1503
    MotorPoleNumberSelection = 0x1504
    H004 = 0x1504
    SpeedResponse = 0x1506
    H005 = 0x1506
    StabilizationParameter = 0x1507
    H006 = 0x1507
    MotorParameterR1 = 0x1516
    H020 = 0x1516
    MotorParameterR2 = 0x1518
    H021 = 0x1518
    H022 = 0x151A
    MotorParameterIo = 0x151C
    H023 = 0x151C
    MotorParameterJ = (0x151D, 2)
    H024 = (0x151D, 2)
    AutoTuningParameterR1 = 0x1525
    H030 = 0x1525
    AutoTuningParameterR2 = 0x1527
    H031 = 0x1527
    H032 = 0x1529
    AutoTuningParameterIo = 0x152B
    H033 = 0x152B
    AutoTuningParameterJ = (0x152C, 2)
    H034 = (0x152C, 2)
    SlipCompensationPGain = 0x153D
    H050 = 0x153D
    SlipCompensationIGain = 0x153E
    H051 = 0x153E
    PMMotorCodeSelection = 0x1571
    H102 = 0x1571
    PMMotorCapacity = 0x1572
    H103 = 0x1572
    PMMotorPoleNumberSelection = 0x1573
    H104 = 0x1573
    PMRatedCurrent = 0x1574
    H105 = 0x1574
    PMParameterR = 0x1575
    H106 = 0x1575
    PMParameterLd = 0x1576
    H107 = 0x1576
    PMParameterLq = 0x1577
    H108 = 0x1577
    PMParameterKe = 0x1578
    H109 = 0x1578
    PMParameterJ = (0x1579, 2)
    H110 = (0x1579, 2)
    AutoTuningPMParameterR = 0x157B
    H111 = 0x157B
    AutoTuningPMParameterLd = 0x157C
    H112 = 0x157C
    AutoTuningPMParameterLq = 0x157D
    H113 = 0x157D
    PMSpeedResponse = 0x1581
    H116 = 0x1581
    PMStartingCurrent = 0x1582
    H117 = 0x1582
    PMStartingTime = 0x1583
    H118 = 0x1583
    PMStabilizationConstant = 0x1584
    H119 = 0x1584
    PMMinimumFrequency = 0x1586
    H121 = 0x1586
    PMNoLoadCurrent = 0x1587
    H122 = 0x1587
    PMStartingMethod = 0x1588
    H123 = 0x1588
    PMIMPE0VWait = 0x158A
    H131 = 0x158A
    PMIMPEDetectWait = 0x158B
    H132 = 0x158B
    PMIMPEDetect = 0x158C
    H133 = 0x158C
    PMIMPEVoltageGain = 0x158D
    H134 = 0x158D

GroupH = MotorConstantsFunctions


class OtherParameters(Register):
    """Other parameters group. See datasheet
    sections 3-9 (pp. 179-190) and B-4 (pp. 339-343)."""
    def contains(value:int):
        return Register.contains(OtherParameters, value)
    # P group
    OperationSelectionAtOption1Error = 0x1601
    P001 = 0x1601
    EATerminalFunction = 0x1603
    P003 = 0x1603
    PulseTrainInputModeForFeedback = 0x1604
    P004 = 0x1604
    EncoderPulses = 0x160B
    P011 = 0x160B
    SimplePositioning = 0x160C
    P012 = 0x160C
    CreepSpeed = 0x160F
    P015 = 0x160F
    PositioningRange = 0x1611
    P017 = 0x1611
    OverSpeedErrorDetectionLevel = 0x161A
    P026 = 0x161A
    SpeedDeviationErrorDetectionLevel = 0x161B
    P027 = 0x161B
    AccelerationDecelerationTimeInputType = 0x161F
    P031 = 0x161F
    TorqueReferenceInputSelection = 0x1621
    P033 = 0x1621
    TorqueReferenceSetting = 0x1622
    P034 = 0x1622
    TorqueBiasMode = 0x1624
    P036 = 0x1624
    TorqueBiasValue = 0x1625
    P037 = 0x1625
    TorqueBiasPolaritySelection = 0x1626
    P038 = 0x1626
    ForwardTorqueControlSpeedLimitValue = (0x1627, 2)
    P039 = (0x1627, 2)
    ReverseTorqueControlSpeedLimitValue = (0x1629, 2)
    P040 = (0x1629, 2)
    SpeedTorqueControlSwitchingTime = 0x162B
    P041 = 0x162B
    NetworkCommunicationWatchdogTimer = 0x162E
    P044 = 0x162E
    CommunicationErrorEffect = 0x162F
    P045 = 0x162F
    InstanceNumber = 0x1630
    P046 = 0x1630
    OperationSettingInIdleMode = 0x1632
    P048 = 0x1632
    PolaritySettingForRotationSpeed = 0x1633
    P049 = 0x1633
    PulseTrainFrequencyScale = 0x1639
    P055 = 0x1639
    PulseTrainFrequencyFilterTimeConstant = 0x163A
    P056 = 0x163A
    PulseTrainFrequencyBiasAmount = 0x163B
    P057 = 0x163B
    PulseTrainFrequencyLimit = 0x163C
    P058 = 0x163C
    PulseInputLowerCut = 0x163D
    P059 = 0x163D
    MultiStepPositionCommand0 = (0x163E, 2)
    P060 = (0x163E, 2)
    MultiStepPositionCommand1 = (0x1640, 2)
    P061 = (0x1640, 2)
    MultiStepPositionCommand2 = (0x1642, 2)
    P062 = (0x1642, 2)
    MultiStepPositionCommand3 = (0x1644, 2)
    P063 = (0x1644, 2)
    MultiStepPositionCommand4 = (0x1646, 2)
    P064 = (0x1646, 2)
    MultiStepPositionCommand5 = (0x1648, 2)
    P065 = (0x1648, 2)
    MultiStepPositionCommand6 = (0x164A, 2)
    P066 = (0x164A, 2)
    MultiStepPositionCommand7 = (0x164C, 2)
    P067 = (0x164C, 2)
    ZeroReturnMode = 0x164E
    P068 = 0x164E
    ZeroReturnDirection = 0x164F
    P069 = 0x164F
    LowSpeedZeroReturnFrequency = 0x1650
    P070 = 0x1650
    HighSpeedZeroReturnFrequency = 0x1651
    P071 = 0x1651
    ForwardPositionRangeSpecification = (0x1652, 2)
    P072 = (0x1652, 2)
    ReversePositionRangeSpecification = (0x1654, 2)
    P073 = (0x1654, 2)
    PositioningMode = 0x1657
    P075 = 0x1657
    EncoderDisconnectionTimeout = 0x1659
    P077 = 0x1659
    PositionRestartRange = 0x165C
    P080 = 0x165C
    SavePositionAtPowerOff = 0x165D
    P081 = 0x165D
    CurrentPositionAtPowerOff = 0x165E
    P082 = 0x165E
    PresetPosition = 0x1660
    P083 = 0x1660
    DriveProgramParameterU00 = 0x1666
    P100 = 0x1666
    DriveProgramParameterU01 = 0x1667
    P101 = 0x1667
    DriveProgramParameterU02 = 0x1668
    P102 = 0x1668
    DriveProgramParameterU03 = 0x1669
    P103 = 0x1669
    DriveProgramParameterU04 = 0x166A
    P104 = 0x166A
    DriveProgramParameterU05 = 0x166B
    P105 = 0x166B
    DriveProgramParameterU06 = 0x166C
    P106 = 0x166C
    DriveProgramParameterU07 = 0x166D
    P107 = 0x166D
    DriveProgramParameterU08 = 0x166E
    P108 = 0x166E
    DriveProgramParameterU09 = 0x166F
    P109 = 0x166F
    DriveProgramParameterU10 = 0x1670
    P110 = 0x1670
    DriveProgramParameterU11 = 0x1671
    P111 = 0x1671
    DriveProgramParameterU12 = 0x1672
    P112 = 0x1672
    DriveProgramParameterU13 = 0x1673
    P113 = 0x1673
    DriveProgramParameterU14 = 0x1674
    P114 = 0x1674
    DriveProgramParameterU15 = 0x1675
    P115 = 0x1675
    DriveProgramParameterU16 = 0x1676
    P116 = 0x1676
    DriveProgramParameterU17 = 0x1677
    P117 = 0x1677
    DriveProgramParameterU18 = 0x1678
    P118 = 0x1678
    DriveProgramParameterU19 = 0x1679
    P119 = 0x1679
    DriveProgramParameterU20 = 0x167A
    P120 = 0x167A
    DriveProgramParameterU21 = 0x167B
    P121 = 0x167B
    DriveProgramParameterU22 = 0x167C
    P122 = 0x167C
    DriveProgramParameterU23 = 0x167D
    P123 = 0x167D
    DriveProgramParameterU24 = 0x167E
    P124 = 0x167E
    DriveProgramParameterU25 = 0x167F
    P125 = 0x167F
    DriveProgramParameterU26 = 0x1680
    P126 = 0x1680
    DriveProgramParameterU27 = 0x1681
    P127 = 0x1681
    DriveProgramParameterU28 = 0x1682
    P128 = 0x1682
    DriveProgramParameterU29 = 0x1683
    P129 = 0x1683
    DriveProgramParameterU30 = 0x1684
    P130 = 0x1684
    DriveProgramParameterU31 = 0x1685
    P131 = 0x1685
    EzCOMMDataCount = 0x168E
    P140 = 0x168E
    EZCOMMDestination1Address = 0x168F
    P141 = 0x168F
    EZCOMMDestination1Register = 0x1690
    P142 = 0x1690
    EZCOMMSource1Register = 0x1691
    P143 = 0x1691
    EZCOMMDestination2Address = 0x1692
    P144 = 0x1692
    EZCOMMDestination2Register = 0x1693
    P145 = 0x1693
    EZCOMMSource2Register = 0x1694
    P146 = 0x1694
    EZCOMMDestination3Address = 0x1695
    P147 = 0x1695
    EZCOMMDestination3Register = 0x1696
    P148 = 0x1696
    EZCOMMSource3Register = 0x1697
    P149 = 0x1697
    EZCOMMDestination4Address = 0x1698
    P150 = 0x1698
    EZCOMMDestination4Register = 0x1699
    P151 = 0x1699
    EZCOMMSource4Register = 0x169A
    P152 = 0x169A
    EZCOMMDestination5Address = 0x169B
    P153 = 0x169B
    EZCOMMDestination5Register = 0x169C
    P154 = 0x169C
    EZCOMMSource5Register = 0x169D
    P155 = 0x169D
    OptionIFCommandWriteRegister1 = 0x16A2
    P160 = 0x16A2
    OptionIFCommandWriteRegister2 = 0x16A3
    P161 = 0x16A3
    OptionIFCommandWriteRegister3 = 0x16A4
    P162 = 0x16A4
    OptionIFCommandWriteRegister4 = 0x16A5
    P163 = 0x16A5
    OptionIFCommandWriteRegister5 = 0x16A6
    P164 = 0x16A6
    OptionIFCommandWriteRegister6 = 0x16A7
    P165 = 0x16A7
    OptionIFCommandWriteRegister7 = 0x16A8
    P166 = 0x16A8
    OptionIFCommandWriteRegister8 = 0x16A9
    P167 = 0x16A9
    OptionIFCommandWriteRegister9 = 0x16AA
    P168 = 0x16AA
    OptionIFCommandWriteRegister10 = 0x16AB
    P169 = 0x16AB
    OptionIFCommandReadRegister1 = 0x16AC
    P170 = 0x16AC
    OptionIFCommandReadRegister2 = 0x16AD
    P171 = 0x16AD
    OptionIFCommandReadRegister3 = 0x16AE
    P172 = 0x16AE
    OptionIFCommandReadRegister4 = 0x16AF
    P173 = 0x16AF
    OptionIFCommandReadRegister5 = 0x16B0
    P174 = 0x16B0
    OptionIFCommandReadRegister6 = 0x16B1
    P175 = 0x16B1
    OptionIFCommandReadRegister7 = 0x16B2
    P176 = 0x16B2
    OptionIFCommandReadRegister8 = 0x16B3
    P177 = 0x16B3
    OptionIFCommandReadRegister9 = 0x16B4
    P178 = 0x16B4
    OptionIFCommandReadRegister10 = 0x16B5
    P179 = 0x16B5
    ProfibusNodeAddress = 0x16B6
    P180 = 0x16B6
    ProfibusClearMode = 0x16B7
    P181 = 0x16B7
    ProfibusMapSelection = 0x16B8
    P182 = 0x16B8
    CANOpenNodeAddress = 0x16BB
    P185 = 0x16BB
    CANOpenCommunicationSpeed = 0x16BC
    P186 = 0x16BC
    CompoNetNodeAddress = 0x16C0
    P190 = 0x16C0
    DeviceNetNodeAddress = 0x16C2
    P192 = 0x16C2
    SerialCommunicationMode = 0x16C8
    P200 = 0x16C8
    ModbusExternalRegister1 = 0x16C9
    P201 = 0x16C9
    ModbusExternalRegister2 = 0x16CA
    P202 = 0x16CA
    ModbusExternalRegister3 = 0x16CB
    P203 = 0x16CB
    ModbusExternalRegister4 = 0x16CC
    P204 = 0x16CC
    ModbusExternalRegister5 = 0x16CD
    P205 = 0x16CD
    ModbusExternalRegister6 = 0x16CE
    P206 = 0x16CE
    ModbusExternalRegister7 = 0x16CF
    P207 = 0x16CF
    ModbusExternalRegister8 = 0x16D0
    P208 = 0x16D0
    ModbusExternalRegister9 = 0x16D1
    P209 = 0x16D1
    ModbusExternalRegister10 = 0x16D2
    P210 = 0x16D2
    ModbusRegisterFormat1 = 0x16D3
    P211 = 0x16D3
    ModbusRegisterFormat2 = 0x16D4
    P212 = 0x16D4
    ModbusRegisterFormat3 = 0x16D5
    P213 = 0x16D5
    ModbusRegisterFormat4 = 0x16D6
    P214 = 0x16D6
    ModbusRegisterFormat5 = 0x16D7
    P215 = 0x16D7
    ModbusRegisterFormat6 = 0x16D8
    P216 = 0x16D8
    ModbusRegisterFormat7 = 0x16D9
    P217 = 0x16D9
    ModbusRegisterFormat8 = 0x16DA
    P218 = 0x16DA
    ModbusRegisterFormat9 = 0x16DB
    P219 = 0x16DB
    ModbusRegisterFormat10 = 0x16DC
    P220 = 0x16DC
    ModbusRegisterScaling1 = 0x16DD
    P221 = 0x16DD
    ModbusRegisterScaling2 = 0x16DE
    P222 = 0x16DE
    ModbusRegisterScaling3 = 0x16DF
    P223 = 0x16DF
    ModbusRegisterScaling4 = 0x16E0
    P224 = 0x16E0
    ModbusRegisterScaling5 = 0x16E1
    P225 = 0x16E1
    ModbusRegisterScaling6 = 0x16E2
    P226 = 0x16E2
    ModbusRegisterScaling7 = 0x16E3
    P227 = 0x16E3
    ModbusRegisterScaling8 = 0x16E4
    P228 = 0x16E4
    ModbusRegisterScaling9 = 0x16E5
    P229 = 0x16E5
    ModbusRegisterScaling10 = 0x16E6
    P230 = 0x16E6
    ModbusInternalRegister1 = 0x16E7
    P301 = 0x16E7
    ModbusInternalRegister2 = 0x16E8
    P302 = 0x16E8
    ModbusInternalRegister3 = 0x16E9
    P303 = 0x16E9
    ModbusInternalRegister4 = 0x16EA
    P304 = 0x16EA
    ModbusInternalRegister5 = 0x16EB
    P305 = 0x16EB
    ModbusInternalRegister6 = 0x16EC
    P306 = 0x16EC
    ModbusInternalRegister7 = 0x16ED
    P307 = 0x16ED
    ModbusInternalRegister8 = 0x16EE
    P308 = 0x16EE
    ModbusInternalRegister9 = 0x16EF
    P309 = 0x16EF
    ModbusInternalRegister10 = 0x16F0
    P310 = 0x16F0
    Endianness = 0x16F1
    P400 = 0x16F1

GroupP = OtherParameters


class SecondMotorFunctions(Register):
    """Second motor function group. See datasheet
    sections 3-x and B-4 (pp. 344-346)."""
    def contains(value:int):
        return Register.contains(SecondMotorFunctions, value)
    # A group
    FrequencyReferenceSelection = 0x2201
    A201 = 0x2201
    RunCommandSelection = 0x2202
    A202 = 0x2202
    BaseFrequency = 0x2203
    A203 = 0x2203
    MaximumFrequency = 0x2204
    A204 = 0x2204
    MultiStepSpeedReference0 = (0x2216, 2)
    A220 = (0x2216, 2)
    TorqueBoostSelection = 0x223B
    A241 = 0x223B
    ManualTorqueBoostVoltage = 0x223C
    A242 = 0x223C
    ManualTorqueBoostFrequency = 0x223D
    A243 = 0x223D
    VFCharacteristicsSelection = 0x223E
    A244 = 0x223E
    OutputVoltageGain = 0x223F
    A245 = 0x223F
    AutomaticTorqueBoostVoltageCompensationGain = 0x2240
    A246 = 0x2240
    AutomaticTorqueBoostSlipCompensationGain = 0x2241
    A247 = 0x2241
    FrequencyUpperLimit = (0x224F, 2)
    A261 = (0x224F, 2)
    FrequencyLowerLimit = (0x2251, 2)
    A262 = (0x2251, 2)
    AVRSelection = 0x2269
    A281 = 0x2269
    AVRVoltageSelection = 0x226A
    A282 = 0x226A
    AccelerationTime2 = (0x2274, 2)
    A292 = (0x2274, 2)
    DecelerationTime2 = (0x2276, 2)
    A293 = (0x2276, 2)
    MethodToSwitchToAcc2Dec2 = 0x2278
    A294 = 0x2278
    Acc1ToAcc2FrequencyTransitionPoint = (0x2279, 2)
    A295 = (0x2279, 2)
    Dec1ToDec2FrequencyTransitionPoint = (0x227B, 2)
    A296 = (0x227B, 2)
    # B group
    ElectronicThermalLevel = 0x230C
    B212 = 0x230C
    ElectronicThermalCharacteristicsSelection = 0x230D
    B213 = 0x230D
    OverloadLimitSelection = 0x2316
    B221 = 0x2316
    OverloadLimitLevel = 0x2317
    B222 = 0x2317
    OverloadLimitParameter = 0x2318
    B223 = 0x2318
    # C group
    OverloadWarningLevel = 0x2429
    C241 = 0x2429
    # H group
    MotorParameterSelection = 0x2502
    H202 = 0x2502
    MotorCapacitySelection = 0x2503
    H203 = 0x2503
    MotorPoleNumberSelection = 0x2504
    H204 = 0x2504
    SpeedResponse = 0x2506
    H205 = 0x2506
    MotorParameterR1 = 0x2516
    H220 = 0x2516
    MotorParameterR2 = 0x2518
    H221 = 0x2518
    H222 = 0x251A
    MotorParameterIo = 0x251C
    H223 = 0x251C
    MotorParameterJ = (0x251D, 2)
    H224 = (0x251D, 2)
    AutoTuningParameterR1 = 0x2525
    H230 = 0x2525
    AutoTuningParameterR2 = 0x2527
    H231 = 0x2527
    H232 = 0x2529
    AutoTuningParameterIo = 0x252B
    H233 = 0x252B
    AutoTuningParameterJ = (0x252C, 2)
    H234 = (0x252C, 2)


class FaultMonitorData(enum.IntEnum):
    """Register offset for fault monitor data access. This is meant
    to be used with fault monitor 1 to 6 commands (D081 - D086) as listed
    in datasheet section B-4 pp. 319-320.
    Use MonitoringFunctions.D08y + FaultMonitorData.xxx to access xxx of
    fault monitor y."""
    Factor = 0x0000
    InverterStatus = 0x0001
    Frequency = 0x0002
    Current = 0x0004
    Voltage = 0x0005
    RunningTime = 0x0006
    PowerOnTime = 0x0008


class TripFactor(enum.IntEnum):
    """Codes identifying the reason of a trip event
    (datasheet section B-4 p. 421)."""
    NoFactor = 0
    OverCurrentAtConstantSpeed = 1
    OverCurrentDuringDeceleration = 2
    OverCurrentDuringAcceleration = 3
    OverCurrentInOtherCondition = 4
    OverloadProtection = 5
    BrakingResistorOverloadProtection = 6
    OvervoltageProtection = 7
    EEPROMError = 8
    UndervoltageProtection = 9
    CurrentDetectionError = 10
    CPUError = 11
    ExternalTrip = 12
    USPError = 13
    GroundFaultProtection = 14
    InputOvervoltageProtection = 15
    InverterThermalTrip = 21
    CPUErrorAlt = 22
    MainCircuitError = 25
    DriverError = 30
    ThermistorError = 35
    BrakingError = 36
    SafeStop = 37
    LowSpeedOverloadProtection = 38
    OperatorConnection = 40
    ModbusCommunicationError = 41
    InvalidInstruction = 43
    InvalidNestingCount = 44
    EasySequenceExecutionError = 45
    EasySequenceUserTrip0 = 50
    EasySequenceUserTrip1 = 51
    EasySequenceUserTrip2 = 52
    EasySequenceUserTrip3 = 53
    EasySequenceUserTrip4 = 54
    EasySequenceUserTrip5 = 55
    EasySequenceUserTrip6 = 56
    EasySequenceUserTrip7 = 57
    EasySequenceUserTrip8 = 58
    EasySequenceUserTrip9 = 59
    OptionError0 = 60
    OptionError1 = 61
    OptionError2 = 62
    OptionError3 = 63
    OptionError4 = 64
    OptionError5 = 65
    OptionError6 = 66
    OptionError7 = 67
    OptionError8 = 68
    OptionError9 = 69
    EncoderDisconnection = 80
    ExcessiveSpeed = 81
    PositionControlRangeTrip = 83


class InverterStatus(enum.IntEnum):
    """Codes identifying the status of the inverter
    (datasheet section B-4 p. 421)."""
    Resetting = 0
    Stopping = 1
    Decelerating = 2
    ConstantSpeedOperation = 3
    Accelerating = 4
    OperatingAtZeroFrequency = 5
    Starting = 6
    DCBreaking = 7
    OverloadRestricted = 8
