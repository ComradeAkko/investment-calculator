# Design.md
### by ComradeAkko

## Classes
```
class Data:
    def __init__(self, otherData):
        self.assets = 0
        self.cagr = 0
        self.taxes = 0
        self.comissions = 0
        self.pl = 0

class sLot:
    def __init__(self, price, quantity, date)
        self.price = price
        self.quantity = quantity
        self.date = date

class nLot:
    def __init__(self, amount, rate, date)
        self.amount = amount
        self.rate = rate
        self.date = date
```
    

# investCalc()

```
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
```

# isActive(strat)
```
If strat == MT || strat == GX:
    return True
Else if strat == (PMT || DMT || GPM || GDM):
    return False
```

# cagr(bb, eb, n)
```
return eb^(1/n)/bb - 1
```

# BHdata()
```
Buy as many quantities of stock that can be bought + comission at 200th day
record past price
get most recent price
data = Data()
data.pl = (current price - past price) * quantity
data.comissions = 5
data.assets = cash + sLot*quantity
data.taxes = 0
data.cagr = cagr()

return data
```

# MTdata()
```
set initial date to the 200th period
slot = sLot()
nlot = nLot()
sQueue = queue(sLots)

For initial period:
    cash -= comission
    data.comission += comission

    data.cash -= current price*quantity

    slot.price = current price
    slot.quantity = quantity
    slot.date = current date
    sQueue.in = slot

For every remaining period:
    if any of the nLots have reached 6months since their last payment/buying:
        pay the yield into cash

    if there are any stock splits:
        go through queue and split the stocks

    if there are any dividends put into cash
        put into cash for every sLot

        if cash is enough to buy:
            cash -= comission
            data.comission += comission

            newLot = sLot()
            newLot.price = current price
            newLot.quantity = quantity
            newLot.date = current date
    
    If current period is above or equal to 200sma:
        If current money == nothing || bonds:
            cash -= comission
            data.comission += comission

            data.cash -= current price*quantity

            slot.price = current price
            slot.quantity = quantity
            slot.date = current date
            sQueue.in = slot
    Else:
        If current money == nothing:
            nlot.amount = money
            nlot.rate = current rate
            nlot.date = current date

        Else if current money == stock:
            cash -= commission
            data.commission += comission
            
            For every sLot in sQueue:
                sales = current price*quantity
                If current price is high than sLot.price:
                    If current date - sLot.date is less than a year:
                        taxes = sales*tax bracket
                    
                    Else:
                        taxes = sales * LTCGT

                    total taxes += taxes
                    sales -= taxes
                
                cash += sales
            nlot = nLot()
            
            nlot.amount = money
            nlot.rate = current rate
            nlot.date = current date

            add nlot to nList

data.assets = cash + every sLot(quantity*current price) + every nLot
data.cagr = cagr()

return data
```