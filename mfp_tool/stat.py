from mfp.types import MfpError, MfpSlot
import mfp.server as server
from multiprocessing import Pool
from mfp.pattern.risky_pattern import *

import mfp_tool.retry as fmt
import os

import datetime
form_date = "%Y-%m-%d %H:%M:%S"

def indicator_header():
    header = []
    header.extend(Risky().header())
    header.extend(RowGrain().header())
    header.extend(RowGrainRisky().header())
    header.extend(RowSpan().header())
    header.extend(RowSpanRisky().header())
    header.extend(RowCombo().header())
    header.extend(RowComboRisky().header())

    header.extend(ColumnGrain().header())
    header.extend(ColumnGrainRisky().header())
    header.extend(ColumnSpan().header())
    header.extend(ColumnSpanRisky().header())
    header.extend(ColumnCombo().header())
    header.extend(ColumnComboRisky().header())

    header.extend(BankGrain().header())
    header.extend(BankGrainRisky().header())
    header.extend(BankSpan().header())
    header.extend(BankSpanRisky().header())
    header.extend(BankCombo().header())
    header.extend(BankComboRisky().header())
    return header

def stat(args):
    pathlist = list(filter(lambda path: not os.path.isdir(path), map(lambda filename: args.path + filename, os.listdir(args.path))))
    indicator_args = zip(pathlist, [fmt.parse] * len(pathlist))
    with Pool(args.cpu) as p:
        result = p.map(indicator, indicator_args)

    header =  "Time,Server,Model,UE Time,Socket,Imc,Channel,Slot," + ",".join(indicator_header()) + "\n"
    os.write(args.output, header.encode())

    for res in result:
        for hostname in res:
            for index, slot in res[hostname]["slots"].items():
                dimm = MfpSlot(index)
                line = "{},{},{},{},{},{},{},{},{}\n" \
                    .format(datetime.datetime.fromtimestamp(slot["timestamp"]).strftime(form_date), hostname, slot["pn"], int(slot["ue_time"]), dimm.slot.socket, dimm.slot.imc, dimm.slot.channel, dimm.slot.slot, ','.join(list(map(lambda x: str(int(x)) if x > 0 else '0', slot["indicator"]))))
                os.write(args.output, line.encode())


def indicator(args):
    (log_path, parser) = args
    servers = parser(log_path)

    for hostname in servers:
        s = server.Server()
        for index in servers[hostname]["slots"]:
            pn = servers[hostname]["slots"][index]["pn"]
            slot = MfpSlot(index)
            s.update_slot(slot, None, pn)

        errors = servers[hostname]["errors"]

        s.error(errors)
        servers[hostname].pop("errors", None)

        # enumerate each slot
        for index in servers[hostname]["slots"]:
            if index in s.slot:
                slot = s.slot[index]
                servers[hostname]["slots"][index]["indicator"] = slot.indicator(lambda x: x if x else 0)
                servers[hostname]["slots"][index]["timestamp"] = slot.timestamp
            else:
                servers[hostname]["slots"][index]["indicator"] = [0] * 1441
                servers[hostname]["slots"][index]["timestamp"] = 0
    return servers

