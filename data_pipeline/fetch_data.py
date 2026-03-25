import yfinance as yf

def fetch_stock_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="6mo")

    data.reset_index(inplace=True)
    return data