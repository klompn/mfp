
from ctypes import cdll
from mfp.types import MfpError
import datetime
import re
import sys
import os

form_date = "%Y-%m-%d %H:%M:%S"
retry_re = re.compile(
    "^([0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})[^#]*###[^#]*###[^#]*#([^#]*)#([^#]*)#.* CPU_SrcID#([0-9]+)_MC#([0-9]+)_Chan#([0-9]+)_DIMM#([0-9]+) .* rank:(?:0x)?([0-9]|1[0-5]) bg:(?:0x)?([0-7]) ba:(?:0x)?([0-3]) row:(?:0x)?([0-9a-f]{1,5}) col:(?:0x)?([0-9a-f]{1,2}|[1-3][0-9a-f][0-9a-f]) retry_rd_err_log\\[([0-9a-f]*) ([0-9a-f]*) ([0-9a-f]*) ([0-9a-f]*) ([0-9a-f]*)\\] correrrcnt\\[([0-9a-f ]*)\\]")

def parse(log_file_path) -> dict:
    with open(log_file_path, "r") as f:
        servers = {}
        invalid_mode = set()
        pn = ""
        err_cnt = 0
        libretry = cdll.LoadLibrary(os.path.dirname(__file__) + "/libretry.so")
            
        for log_line in f:
            m = retry_re.search(log_line)
            if m is None:
                continue
            
            hostname = log_file_path

            if hostname not in servers:
                servers[hostname] = {"errors": [], "slots": {}}

            error_time = datetime.datetime.strptime(m.group(1), form_date).timestamp()
            sn = m.group(2).strip()
            pn = m.group(3).strip()

            r154 = int(m.group(13), 16)
            r148 = int(m.group(14), 16)
            r150 = int(m.group(15), 16)
            r15c = int(m.group(16), 16)
            r114 = int(m.group(17), 16)

            error_item = MfpError(0, libretry.read(4, r154, r148, r150, r15c, r114))
            error_item.cell.socket = int(m.group(4))
            error_item.cell.imc = int(m.group(5))
            error_item.cell.channel = int(m.group(6))
            error_item.cell.slot = int(m.group(7))

            slot = error_item.value

            if slot not in invalid_mode and libretry.read(3, r154, r148, r150, r15c, r114) > 3:
                sys.stderr.write("host: {} socket: {} imc: {} channel: {} slot: {}, only SDDC Mode is supported\n".format(hostname, m.group(4), m.group(5), m.group(6), m.group(7)))
                invalid_mode.add(slot)
                continue

            error_item.cell.device = libretry.read(1, r154, r148, r150, r15c, r114)
            error_item.cell.rank = int(m.group(8))
            error_item.cell.bank_group = int(m.group(9))
            error_item.cell.bank = int(m.group(10))
            error_item.cell.row = int(m.group(11), 16)
            error_item.cell.col = int(m.group(12), 16)

            if slot not in servers[hostname]["slots"]:
                servers[hostname]["slots"][slot] = {"ue": -1, "ue_time": 0}
            servers[hostname]["slots"][slot]["pn"] = pn

            if libretry.read(2, r154, r148, r150, r15c, r114) == 1:
                if err_cnt == 0:
                    return {}
                servers[hostname]["slots"][slot]["ue_time"] = error_time
                break
            err_cnt += 1
            if libretry.read(0, r154, r148, r150, r15c, r114) != 0:
                servers[hostname]["errors"].append((error_time, error_item,))
        return servers
    return {}