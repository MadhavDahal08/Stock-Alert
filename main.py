import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


load_dotenv()
STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
my_twilio_number = os.getenv("my_twilio_number")

stock_price_api = "https://www.alphavantage.co/query"
news_api_url = 'https://newsapi.org/v2/everything'


stock_price_api_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}
news_api_parameters = {
    "qInTitle": COMPANY_NAME,
    "apiKey": NEWS_API_KEY
}

# When STOCK price increase/decreases by 5% between yesterday and

#Calculate Percentage change in stock price
def get_percentage_fluctuation():
    response = requests.get(url=stock_price_api, params=stock_price_api_parameters)
    response.raise_for_status()
    list_data = list(response.json()["Time Series (Daily)"].values())
    date_1_data = list_data[0]["4. close"]
    date_2_data = list_data[1]["4. close"]
    diff = float(date_2_data) - float(date_1_data)
    percentage_change = (abs(diff) / float(date_2_data)) * 100
    return [percentage_change,diff]

#Generate message by extracting the news related to stock
def generate_msg(symbol, percent):
    news_response = requests.get(news_api_url, params=news_api_parameters)
    news_response.raise_for_status()
    articles= news_response.json()["articles"]
    three_articles = articles[:3]

    for article in three_articles:
        title = article["title"]
        description = article["description"]
    msg = f"""{STOCK}: sign{percentage_change}%
    Headline: {title}
    Brief: {description}
    """
    return msg


if get_percentage_fluctuation()[0] >= 5:
    sign: str
    percentage_change = get_percentage_fluctuation()[0]
    diff = get_percentage_fluctuation()[1]
    if diff > 0:
        sign = "🔺"
    else:
        sign = "🔻"
    news_response = requests.get(news_api_url, params=news_api_parameters)
    news_response.raise_for_status()
    articles = news_response.json()["articles"]
    three_articles = articles[:3]

    for article in three_articles:
        title = article["title"]
        description = article["description"]
        msg = f"""{STOCK}: sign{percentage_change}%
        Headline: {title}
        Brief: {description}
        """
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=msg,
            from_='+18144731588',
            to='+9779860911131'
        )