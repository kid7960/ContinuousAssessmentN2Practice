"""
This file holds all the functions related to getting the weather and news information
"""

import json
import requests
from notification import news_event, weather_event


def get_api_keys() -> tuple:
    """
    This function gets the news api key from the config file.
    """
    with open('config.json') as config_file:
        api_keys = json.load(config_file)
        weather_api_key = api_keys['openweathermap_api']
        news_api_key = api_keys['news_api']
    return weather_api_key, news_api_key


def news(news_api_key) -> tuple:
    """
    This function gets the latest news from newsapi.org using the api key got from
    the get_news_api function. The function also returns the description and url of the article.
    """
    top_news_title = []  # storing title of news
    top_news_content = []   # storing description of news
    top_news_url = []   # storing url of news
    news1 = requests.get(
        "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={}".
        format(news_api_key))   # request news data from newsapi.org using api key
    page1 = news1.json()    # turn news1 into a json obj
    article1 = page1["articles"]
    for i in article1:  # loop through the articles
        title = i["title"]  # get the title of the article
        content = i["description"]  # get the description of the news article
        url = "Full article can be found here: " + i["url"]  # get the url of article
        top_news_title.append(title)
        top_news_content.append(content)
        top_news_url.append(url)
        news_event(i["title"])  # add news title to notification

    return top_news_title, top_news_content, top_news_url


def weather(weather_api_key) -> tuple:
    """
    This function gets the weather date using the api key from the get_openweather_api.
    """
    temp1 = requests.get(
        "http://api.openweathermap.org/data/2.5/weather?q=Exeter,uk,&units=metric&appid={}".
        format(weather_api_key))    # get weather information from openweathermap.org
    json_obj = temp1.json()  # convert temp1 into a json obj
    temperature = json_obj['main']['temp']  # get the temperature
    wind_speed = json_obj['wind']['speed']  # get the wind speed
    description = json_obj['weather'][0]['description']  # get the weather description
    weather_event(temperature)
    return temperature, wind_speed, description
