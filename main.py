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
data = response.json()
print(data)