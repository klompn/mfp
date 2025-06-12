
import ctypes

class MfpErrorBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("socket", ctypes.c_uint64, 3),
        ("imc", ctypes.c_uint64, 2),
        ("channel", ctypes.c_uint64, 2),
        ("slot", ctypes.c_uint64, 2),
        ("rank", ctypes.c_uint64, 4),
        ("device", ctypes.c_uint64, 6),
        ("bank_group", ctypes.c_uint64, 3),
        ("bank", ctypes.c_uint64, 2),
        ("row", ctypes.c_uint64, 20),
        ("col", ctypes.c_uint64, 10),
        ("error_type", ctypes.c_uint64, 1),
        ("reserved", ctypes.c_uint64, 9),
    ]


class MfpError(ctypes.Union):
    _fields_ = [
        ("cell", MfpErrorBits),
        ("value", ctypes.c_uint64),
    ]

    def __init__(self, v = 0, risky: int = 0):
        self.value = v
        if risky == 0:
            self.risky = False
        else:
            self.risky = True


class MfpSlotBits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("socket", ctypes.c_uint64, 3),
        ("imc", ctypes.c_uint64, 2),
        ("channel", ctypes.c_uint64, 2),
        ("slot", ctypes.c_uint64, 2),
        ("reserved", ctypes.c_uint64, 7),
    ]

class MfpSlot(ctypes.Union):
    _fields_ = [
        ("slot", MfpSlotBits),
        ("value", ctypes.c_uint16),
    ]

    def __init__(self, v):
        self.value = v