import os
import yfinance as yf
import pandas as pd
import time
import csv

period = "1mo"

url = "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average"
# url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

tables = pd.read_html(url)
ticker_table = tables[2]
print(ticker_table)
tickers = ticker_table["Symbol"].tolist()
out_dir = os.getenv("OUT_DIR", "/tmp")
#
with open("/tmp/dji_data.csv", "w", newline="") as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(["ticker", "date", "open", "high", "low", "close", "volume"])

    for ticker in tickers:
        try:
            h = yf.Ticker(ticker).history(period=period)
            h.reset_index(inplace=True)

            for _, row in h.iterrows():
                csvwriter.writerow(
                    [
                        ticker,
                        row["Date"].strftime("%Y-%m-%d"),
                        row["Open"],
                        row["High"],
                        row["Low"],
                        row["Close"],
                        row["Volume"],
                    ]
                )

            print(f"Inserted data for {ticker}")
            time.sleep(0.2)  # To avoid hitting rate limits
        except Exception as e:
            print(f"Error processing {ticker}: {e}")

print("Done")
