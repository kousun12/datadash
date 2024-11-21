import yfinance as yf
import pandas as pd
import duckdb
import time

period = "1mo"

# url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

tables = pd.read_html(url)
sp500_table = tables[0]
tickers = sp500_table["Symbol"].tolist()

con = duckdb.connect("sp500_data.db")
con.execute(
    """
    CREATE TABLE IF NOT EXISTS stock_data (
        ticker STRING,
        date DATE,
        open DOUBLE,
        high DOUBLE,
        low DOUBLE,
        close DOUBLE,
        volume BIGINT
    )
"""
)

for ticker in tickers:
    try:
        h = yf.Ticker(ticker).history(period=period)
        h.reset_index(inplace=True)
        h["ticker"] = ticker
        con.execute(
            """
            INSERT INTO stock_data 
            SELECT ticker, Date, Open, High, Low, Close, Volume 
            FROM h
        """
        )
        print(f"Inserted data for {ticker}")
        time.sleep(1)  # To avoid hitting rate limits
    except Exception as e:
        print(f"Error processing {ticker}: {e}")

con.commit()
con.close()

print("Done")
