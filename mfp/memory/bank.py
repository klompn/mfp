
from mfp.types import MfpError
from .col import Col
from .row import Row
from .stat import Stat
from mfp.util.grain import Grain
from mfp.util.basic import Basic

import typing

class Bank:
    def __init__(self):

        self.row_basic = Basic(32, 512)
        self.col_basic = Basic(64, 32768)

        self.rows = {}
        self.cols = {}
        self.cells = {}
        self.grain = Grain(86400, 60)
        self.last_risky = -1

    def error(self, err: typing.Tuple[int, MfpError], stat: Stat):
        (t, e) = err
        row = e.cell.row
        col = e.cell.col

        # Column Statistic
        if col not in self.cols:
            self.cols[col] = Col()
        self.cols[col].error(err, stat)

        # Row Statistic
        if row not in self.rows:
            self.rows[row] = Row()
        self.rows[row].error(err, stat)

        stat.bank.row_basic = self.row_basic.observe(t, e.cell.col)
        stat.bank.col_basic = self.col_basic.observe(t, e.cell.row)
        if e.risky:
            self.last_risky = t
        stat.bank.last_risky = self.last_risky
