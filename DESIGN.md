# Design.md
### by ComradeAkko

## Classes
class Data:
    def __init__(self, otherData):
        self.cash = 0
        self.cagr = 0
        self.taxes = 0
        self.comissions = 0
        self.pl = 0

class Lot:
    def __init__(self, price, quantity, date)
        self.price = price
        self.quantity = quantity
        self.date = date
    

# investCalc()

data = Data()

If stock and bond data exists:
    If stock data is more than 200 days enabling actual calculations:
        If strat == MT:
            MTdata = MT()
            BHdata = BH()
            printResults(BHdata, MTdata)

        Else if strat == GX:
            GXdata = GX()
            BHdata = BH()
            printResults(BHdata, MTdata)

        Else If strat == DMT:
            DMTdata = DMT()
            DCAdata = DCA()
            printResults(DCAdata, DMTdata)

        Else If strat == PMT:
            PMTdata = PMT()
            DCAdata = DCA()
            printResults(DCAdata, PMTdata)

        Else If strat == GPM:
            GPMdata = GPM()
            DCAdata = DCA()
            printResults(DCAdata, GMPdata)

        Else If strat == GDM:
            GDMdata = GDM()
            DCAdata = DCA()
            printResults(DCAdata, GDMdata)

        Else:
            print error concerning non-existing strat
    Else:
        print error concerning not enough data

Else:
    If stock data does not exist:
        Run getStockData

    If stock data is not more than 200 days worth
        print error concerning not enough data for long term stock stuff
    
    if bond data does not exist:
        Run getBondData
    
    run investCalc()


# isActive(strat)
If strat == MT || strat == GX:
    return True
Else if strat == (PMT || DMT || GPM || GDM):
    return False

# cagr(bb, eb, n)
return eb^(1/n)/bb - 1

# BHdata()
Buy as many quantities of stock that can be bought + comission at 200th day
record past price
get most recent price
data = Data()
data.pl = (current price - past price) * quantity
data.comissions = 5
data.cash = is how much cash that is left
data.taxes = 0
data.cagr = cagr()

# MTdata()
set initial date to the 200th period
For every remaining period:
    If current period is above buy all possible 