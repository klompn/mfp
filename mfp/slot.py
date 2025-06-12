
from .types import MfpError
from .const import *
from mfp.pattern.risky_pattern import *
import mfp.memory as memory
import typing


MIN_CE_COUNT = 16


class Slot:
    def __init__(self):
        self.timestamp = None
        self.risky_count = 0
        self.device = {}

        # export pattern
        self.risky = Risky()
        self.row_grain = RowGrain()
        self.row_grain_risky = RowGrainRisky()
        self.row_span = RowSpan()
        self.row_span_risky = RowSpanRisky()
        self.row_combo = RowCombo()
        self.row_combo_risky = RowComboRisky()
        self.col_grain = ColumnGrain()
        self.col_grain_risky = ColumnGrainRisky()
        self.col_span = ColumnSpan()
        self.col_span_risky = ColumnSpanRisky()
        self.col_combo = ColumnCombo()
        self.col_combo_risky = ColumnComboRisky()
        self.bank_grain = BankGrain()
        self.bank_grain_risky = BankGrainRisky()
        self.bank_span = BankSpan()
        self.bank_span_risky = BankSpanRisky()
        self.bank_combo = BankCombo()
        self.bank_combo_risky = BankComboRisky()

    def error(self, err: typing.Tuple[int, MfpError]):
        (t, e) = err
        device = e.value & MASK_DEVICE

        if device not in self.device:
            self.device[device] = memory.Device()
        
        stat = memory.Stat()
        self.device[device].error(err, stat)
        
        if e.risky:
            self.risky_count += 1

        self.risky.check(t, self.risky_count)
        self.row_grain.check(t, stat.row.basic.grain)
        self.row_span.check(t, stat.row.basic.span)
        self.row_combo.check(t, (stat.row.basic.grain, stat.row.basic.span))
        if stat.row.last_risky != -1 and t - stat.row.last_risky <= 86400:
            self.row_grain_risky.check(t, stat.row.basic.grain)
            self.row_span_risky.check(t, stat.row.basic.span)
            self.row_combo_risky.check(t, (stat.row.basic.grain, stat.row.basic.span))
        self.col_grain.check(t, stat.col.basic.grain)
        self.col_span.check(t, stat.col.basic.span)
        self.col_combo.check(t, (stat.col.basic.grain, stat.col.basic.span))
        if stat.col.last_risky != -1 and t - stat.col.last_risky <= 86400:
            self.col_grain_risky.check(t, stat.col.basic.grain)
            self.col_span_risky.check(t, stat.col.basic.span)
            self.col_combo_risky.check(t, (stat.col.basic.grain, stat.col.basic.span))
        self.bank_grain.check(t, (stat.bank.row_basic.grain, stat.bank.col_basic.grain))
        self.bank_span.check(t, (stat.bank.row_basic.span, stat.bank.col_basic.span))
        self.bank_combo.check(t, (stat.bank.row_basic.grain, stat.bank.row_basic.span, stat.bank.col_basic.grain, stat.bank.col_basic.span))
        if stat.bank.last_risky != -1 and t - stat.bank.last_risky <= 86400:
            self.bank_grain_risky.check(t, (stat.bank.row_basic.grain, stat.bank.col_basic.grain))
            self.bank_span_risky.check(t, (stat.bank.row_basic.span, stat.bank.col_basic.span))
            self.bank_combo_risky.check(t, (stat.bank.row_basic.grain, stat.bank.row_basic.span, stat.bank.col_basic.grain, stat.bank.col_basic.span))

        self.timestamp = t

    def indicator(self, cast):
        ret = []
        ret.extend(map(cast, self.risky.result()))
        ret.extend(map(cast, self.row_grain.result()))
        ret.extend(map(cast, self.row_grain_risky.result()))
        ret.extend(map(cast, self.row_span.result()))
        ret.extend(map(cast, self.row_span_risky.result()))
        ret.extend(map(cast, self.row_combo.result()))
        ret.extend(map(cast, self.row_combo_risky.result()))

        ret.extend(map(cast, self.col_grain.result()))
        ret.extend(map(cast, self.col_grain_risky.result()))
        ret.extend(map(cast, self.col_span.result()))
        ret.extend(map(cast, self.col_span_risky.result()))
        ret.extend(map(cast, self.col_combo.result()))
        ret.extend(map(cast, self.col_combo_risky.result()))

        ret.extend(map(cast, self.bank_grain.result()))
        ret.extend(map(cast, self.bank_grain_risky.result()))
        ret.extend(map(cast, self.bank_span.result()))
        ret.extend(map(cast, self.bank_span_risky.result()))
        ret.extend(map(cast, self.bank_combo.result()))
        ret.extend(map(cast, self.bank_combo_risky.result()))
        return ret