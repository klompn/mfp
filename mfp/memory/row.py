
from mfp.types import MfpError
from mfp.util.basic import Basic
from .stat import Stat
import typing

class Row:
    def __init__(self):
        self.basic = Basic(32, 512)
        self.last_risky = -1

    def error(self, err: typing.Tuple[int, MfpError], stat: Stat):
        (t, e) = err
        stat.row.basic = self.basic.observe(t, e.cell.col)
        if e.risky:
            self.last_risky = t
        stat.row.last_risky = self.last_risky