"""
This python file holds all the functions related to alarms.
"""

import time
import sched
import datetime
from notification import alarm_event

# list that holds all the alarms
ALARM_LIST = []


def clock() -> str:
    """
    This function get the current time in the form of hours and minutes.
    """
    current_time = time.strftime("%Y-%m-%d %H:%M")
    current_time = str(current_time)  # convert current_time from time to string
    return current_time


def alarm_difference(alarm):
    """
    This function gets the difference between the time.now and the date+time
    entered by the user when setting up an alarm. This function is essential
    to be able to set up an alarm. Since the sched module is only compatible
    with the time variables the function also converts from datetime to time.
    """
    alarm = datetime.datetime.strptime(alarm, "%Y-%m-%dT%H:%M")
    # converts the date+time entered by the user to datetime
    now = datetime.datetime.now()
    alarm_ts = time.mktime(alarm.timetuple())
    # converts the alarm datetime to a time object
    now_ts = time.mktime(now.timetuple())
    difference = abs(alarm_ts - now_ts)
    # find difference by subtraction
    return difference


def set_alarm(difference: time):
    """
    This function sets up an alarm using sched module.
    The delay is found is the alarm_difference function.
    """
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(difference, 1, alarm_event, )
    # set up schedule with the delay got from the alarm_difference function
    scheduler.run()
    # run the scheduler so alarm goes of at the desired time


def cancel_alarm():
    """
    This function cancels the alarms already set.
    This function is designed to be set off by pressing a button.
    """
    s = sched.scheduler(time.time, time.sleep)
    if not s.empty():  # make sure queue is not empty else cancel() raise error
        ALARM_LIST.clear()  # clears the alarm list
        map(s.cancel, s.queue)  # remove the event from the queue
        return "Alarms canceled!"
    else:
        return "There are no alarms set to cancel!"
