class RowStat:
    basic = None
    last_risky = -1

class ColStat:
    basic = None
    last_risky = -1

class BankStat:
    row_basic, col_basic = None, None
    last_risky = -1

class Stat:
    row = RowStat()
    col = ColStat()
    bank = BankStat()