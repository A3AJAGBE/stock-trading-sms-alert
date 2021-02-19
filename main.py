import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

# Twilio configs
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Stock Config
STOCK_NAME = "AAPL"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_PARAMETER = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "outputsize": "compact",
    "apikey": os.environ.get("STOCK_API")
}

stock_response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMETER)
stock_response.raise_for_status()
data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# Previous day closing price
previous_day_data = data_list[0]
p_closing_price = previous_day_data["4. close"]

# Get the closing price for 2-days back (Day before yesterday)
before_yesterday_data = data_list[1]
by_closing_price = before_yesterday_data["4. close"]

# Get the difference and percentage
difference = float(p_closing_price) - float(by_closing_price)
percentage = abs(round((difference / float(p_closing_price)) * 100))
up_down = None

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# If percentage is greater than 1 get the articles relating to the company
if percentage >= 1:
    # News Config
    COMPANY_NAME = "Apple Inc"
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    NEWS_PARAMETER = {
        "qInTitle": COMPANY_NAME,
        "apiKey": os.environ.get("NEWS_API")
    }

    news_response = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETER)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    top3_articles = news_data[:3]

    # Get article headline and description
    article_list = [f"{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {article['title']}\n Desc: {article['description']}" for article in top3_articles]

    # Send each article to the user
    for article in article_list:
        message = client.messages.create(
            body=f"{article} From: A3AJAGBE TRADING ALERT",
            from_=os.environ.get('TWILIO_NUMBER'),
            to=os.environ.get('MY_NUMBER')
        )


