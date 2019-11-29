"""
This module is a program that simulates a smart system more specifically a smart alarm system
capable of setting alarms,showing notifications and showing accurate news and weather information.
This system will run on flask web framework.
"""

import logging
from flask import Flask, render_template, request
from news_weather import get_api_keys, weather, news
from alarm import clock, ALARM_LIST, set_alarm, alarm_difference, cancel_alarm
from notification import get_notifications

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="logfile.log",
                    level=logging.DEBUG,
                    format=LOG_FORMAT)
LOGGER = logging.getLogger()
APP = Flask(__name__)
WEATHER_API_KEY = get_api_keys()[0]
NEWS_API_KEY = get_api_keys()[1]


@APP.route('/')
def home() -> render_template:
    """
    This function generates the home page of the smart system.
    On this page the user can check the exact time and notifications.
    """
    LOGGER.info("executing home() @APP.route('/')")
    now = clock()
    LOGGER.debug("# getting current time as string in format hh:mm")
    LOGGER.debug("# getting api key for news")
    news(NEWS_API_KEY)
    LOGGER.debug("# getting top news using api key from BBC")
    LOGGER.debug("# getting api key for weather")
    weather(WEATHER_API_KEY)
    LOGGER.debug("# getting current weather description")
    notification_list = get_notifications()
    LOGGER.debug("# getting the notification list")
    return render_template('Home.html', now=now, notification_list=notification_list)


@APP.route('/news')
def news__weather_page() -> render_template:
    """
    This function generates the news page of the smart system.
    On this page the user can check the news and the weather. The system
    will provide detailed description of the weather as well as the news.
    """
    LOGGER.info("executing news_weather_page() @APP.route('/news')")
    LOGGER.debug("# getting api key for weather")
    LOGGER.debug("# getting api key for news")
    weather_tuple_obj = weather(WEATHER_API_KEY)
    LOGGER.debug("# assigning weather()func returns to weather_tuple_obj")
    temperature = weather_tuple_obj[0]
    LOGGER.debug("# getting temperature from weather_tuple_obj")
    wind_speed = weather_tuple_obj[1]
    LOGGER.debug("# getting wind speed from weather_tuple_obj")
    description = weather_tuple_obj[2]
    LOGGER.debug("# getting description of weather from weather_tuple_obj")
    news_tuple_obj = news(NEWS_API_KEY)
    LOGGER.debug("# assigning news() func returns to news_tuple_obj")
    top_news_title = news_tuple_obj[0]
    LOGGER.debug("# getting news titles from news()")
    top_news_content = news_tuple_obj[1]
    LOGGER.debug("# getting news content from news()")
    top_news_url = news_tuple_obj[2]
    LOGGER.debug("# getting news url from news()")
    return render_template('News.html', top_news_title=top_news_title, top_news_url=top_news_url,
                           top_news_content=top_news_content, temperature=temperature,
                           description=description, wind_speed=wind_speed)


@APP.route('/setalarm')
def set_alarm_page() -> render_template:
    """
    This function generates the page where the user can set the alarms.
    """
    LOGGER.info("executing set_alarm_page() @APP.route('/setalarm')")
    alarm = request.args.get("alarm")
    LOGGER.debug("# getting the alarm information from user")z
    notification = get_notifications()
    LOGGER.debug("# getting notifications /setalarm")
    if alarm:  # if there is input from user to set alarm
        ALARM_LIST.APPend(alarm)  # adds alarm information to alarm list
        set_alarm(alarm_difference(alarm))  # sets up an alarm
    LOGGER.debug("# setting alarm using sched module")
    return render_template('Set_alarm.html', notification=notification)


@APP.route('/alarmlist')
def alarmlist_page() -> render_template:
    """
    This function generates the alarmlist page where user can view all the alarms set.
    User can also cancel these alarms by pressing the APPropriate button.
    """
    LOGGER.info("executing alarmlist_page() @APP.route('/alarmlist')")
    notification = get_notifications()
    LOGGER.debug("# getting notifications for /alarmlist")
    return render_template('Alarm_list.html', alarm_list=ALARM_LIST, notification=notification)


@APP.route('/cancelalarm')
def cancelalarm_page() -> render_template:
    """
    This function generates a page after the user has pressed the button to cancel
    the alarms set. This page gives confirmation that the alarms has been cancelled.
    """
    LOGGER.info("executing cancelalarm_page() @APP.route('/cancelalarm')")
    cancel_message = cancel_alarm()
    LOGGER.debug("# cancelling alarm in queue")
    return render_template('Cancel__alarm.html', cancel_message=cancel_message)


if __name__ == "__main__":
    APP.run(debug=True)
