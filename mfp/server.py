
from .types import MfpError, MfpSlot
from .const import MASK_SLOT
from .slot import Slot
import typing


class Server:
    def __init__(self):
        self.slot = {}
        self.sn_pn = {}
        self.timestamp = 0

    def error(self, errs: typing.List[typing.Tuple[int, MfpError]]):
        errs = list(filter(lambda x: x[0] >= self.timestamp, errs))
        errs.sort(key=lambda x: x[0])
        for err in errs:
            (t, e) = err
            slot = e.value & MASK_SLOT
            if slot not in self.slot:
                self.slot[slot] = Slot()
            self.slot[slot].error(err)
            self.timestamp = t
    
    def update_slot(self, slot: MfpSlot, sn: str, pn: str):
        idx = slot.value
        if idx not in self.sn_pn:
            old_sn, old_pn = None, None
        else:
            (old_sn, old_pn) = self.sn_pn[idx]
        if (old_sn is not None and old_sn != sn) or (old_pn is not None and old_pn != pn):
            # clean old slot data if the sn or pn get changed
            self.slot.pop(idx)
        self.sn_pn[idx] = (sn, pn)