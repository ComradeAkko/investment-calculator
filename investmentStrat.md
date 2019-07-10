# Investment strategies
### by ComradeAkko

The following are the investment strategies that can be used with the function `investCalc()`. Static strategies are ones where the only capital used is the initial capital. Active strategies include monthly payments. 

## Static Strategies
### Buy and Hold (BH):
After an initial investment, the shares are held for the entirety of its period.

### Regular Momentum Trading (MT):
After an intial investment, the shares are held as long as the price is above its 200-day moving average. If the price is below its 200-day moving average, it is sold and transferred to bonds.

## Golden-Cross Momentum Trading (GX):
After an initial investment, shares are held when the price is above both its 200-day and 50-day moving average. If the 50-day moving average crosses below the 200-day moving average, the shares are sold and transferred to bonds.

## Active Strategies
### Dollar-cost Averaging (DCA):
After the initial lump-sum investment, every month on a specific day, as many shares as many are allowed are bought regardless of whether prices are high or low. Shares are never sold.

### Parallel Momentum Trading (PMT):
After the intial lump-sum investment, every month on a specific day, shares are bought as long as the current price is higher than the 200-day moving average. If the current price drops below the 200-day moving average, the shares are sold and transferred to bonds. Subsequent investment income will be directed to bonds (**parallel** with current investments) until the price of the shares rises above the 200-day moving average again.

### Divergent Momentum Trading (DMT):
After the initial lump-sum investment, every month on a specific day, shares are bought as long as the current price is higher than the 200-day moving average. If the current price drops below the 200-day moving average, the shares are sold and transferred to bonds. Subsequent investment income will be directed to stocks (**divergent** with current investmenets) until the price of the shares rises above the 200-day moving average again.

### Golden-Cross Parallel Momentum Trading (GPM)
A combination of PMT and using both 200-day and 50-day moving averages.

### Golden-Cross Divergent Momentum Trading (GDM)
A combination of DMT and using both 200-day and 50-day moving averages.