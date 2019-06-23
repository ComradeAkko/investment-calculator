#priceExtractor by Jiro Mizuno

import urllib

base = "http://ichart.finance.yahoo.com/table.csv?s="

def concatURL(ticker):
    return base + ticker