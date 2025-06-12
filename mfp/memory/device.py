from typing import Tuple
from mfp.const import *
from mfp.types import *
from .bank import Bank
from .stat import Stat

class DeviceStat:
    def __init__(self, fault_bank):
        self.fault_bank = fault_bank

class Device:
    def __init__(self):
        self.fault_bank = 0
        self.bank = {}

    def error(self, err: Tuple[int, MfpError], stat: Stat):
        (t, e) = err

        bank = (e.value & MASK_BANK) >> 19
        if bank not in self.bank:
            self.bank[bank] = Bank()

        self.bank[bank].error(err, stat)