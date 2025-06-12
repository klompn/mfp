
from mfp.types import MfpError
from mfp.util.basic import Basic
from .stat import Stat
import typing

class Col:
    def __init__(self):
        self.basic = Basic(64, 32768)
        self.last_risky = -1

    def error(self, err: typing.Tuple[int, MfpError], stat: Stat):
        (t, e) = err
        stat.col.basic = self.basic.observe(t, e.cell.row)
        if e.risky:
            self.last_risky = t
        stat.col.last_risky = self.last_risky