# Local Module
from scheduler.config import SCHEDULE


def per_x_seconds(second: int):
    return SCHEDULE.every(second).seconds


def every_minute_at(second: int):
    return SCHEDULE.every().minute.at(f':{second}')


def every_hour_at(minute: str):
    return SCHEDULE.every().hour.at(f':{minute}')


def every_day_at(trigger_time: str):
    return SCHEDULE.every().day.at(trigger_time)
