"""
This file holds all the functions related to notifications.
"""
import datetime
import pyttsx3

NOTIFICATION_LIST = []  # notifications all collected into a list


def weather_event(new_temp: int):
    """
    This function adds a string to the NOTIFICATION_LIST telling
    the user the current temperature in Exeter.
    """
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    # current time
    weather_message = now + " Temperature now is: " + str(new_temp) + "°C"
    NOTIFICATION_LIST.insert(0, weather_message)
    # insert weather message into notification list
    # so the order would not get messed up


def alarm_event():
    """
    This function adds a string to the NOTIFICATION_LIST when
    as an alarm message. Each time the schedule goes off this
    function gets executed. Function also reads out the alarm
    message as a text-to-speech notification.
    """
    now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    alarm_message = "WAKE UP! This is your alarm for: " + now
    NOTIFICATION_LIST.insert(0, alarm_message)
    engine = pyttsx3.init()  # using pyttsx3 for voice notifications
    engine.say(alarm_message)
    # engine saying alarm_message out loud
    engine.runAndWait()


def news_event(breaking_news: str):
    """
    This function adds a string to NOTIFICATION_LIST when
    there is a change in BBC top news.
    """
    if not any(breaking_news in s for s in NOTIFICATION_LIST):
        # this if checks if there is a similar news title in the notification list
        # this ensures that the function will not notify the user of the same news titles
        now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        news_message = now + " BREAKING NEWS! " + breaking_news
        NOTIFICATION_LIST.insert(0, news_message)


def get_notifications() -> list:
    """
    This function simply returns the notification list
    """
    return NOTIFICATION_LIST
