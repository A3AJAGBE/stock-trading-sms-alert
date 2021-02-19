import os
import requests
from dotenv import load_dotenv
load_dotenv()

# Stock Config
STOCK_NAME = "AAPL"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_PARAMETER = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": os.environ.get("STOCK_API")
}

response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETER)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# Previous day closing price
previous_day_data = data_list[0]
p_closing_price = previous_day_data["4. close"]
print(p_closing_price)
