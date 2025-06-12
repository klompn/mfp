
from mfp.pattern.pattern import ValuePattern
from mfp.pattern.component_pattern import *

class Risky(ValuePattern):
    def __init__(self):
        self.flag = [None]
        self.t = [1]

class RowGrainRisky(RowGrain):
    pass
class RowSpanRisky(RowSpan):
    pass
class RowComboRisky(RowCombo):
    pass
class ColumnGrainRisky(ColumnGrain):
    pass
class ColumnSpanRisky(ColumnSpan):
    pass
class ColumnComboRisky(ColumnCombo):
    pass
class BankGrainRisky(BankGrain):
    pass
class BankSpanRisky(BankSpan):
    pass
class BankComboRisky(BankCombo):
    pass