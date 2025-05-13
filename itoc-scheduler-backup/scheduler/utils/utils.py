import os
import time
import traceback
from datetime import datetime

import requests
from loguru import logger

from scheduler.config import COMMON


def send_request(request_func):
    """A Decorator for requests module to prevent some exceptions

    Arguments:
        request_func {callable} -- function with requests.get, requests.post
    """

    def wrapper(*args, **kwargs):
        count = 0
        while count < COMMON.http_req_retry_time:
            try:
                res = request_func(*args, **kwargs)
                status = res.status_code

                if status != 200:
                    logger.warning(f'REQ UNAVAILABLE: {status}')

                return res

            except requests.exceptions.Timeout as error:
                logger.warning(f'UNAVAILABLE: Connection Timeout {error}')
            except requests.exceptions.ConnectionError as error:
                logger.warning(f'UNAVAILABLE: Connection Error {error}')
            except ConnectionRefusedError as error:
                logger.warning(
                    f'UNAVAILABLE: Connection Refused Error {error}'
                )
            except requests.exceptions.MissingSchema:
                logger.warning(
                    f'UNAVAILABLE: URL Schema Error {traceback.format_exc()}'
                )
            finally:
                count += 1
                time.sleep(2)

    return wrapper


@send_request
def send_post_request(url, headers=None, data=None):
    return requests.post(url, headers=headers, data=data)


@send_request
def send_get_request(url, headers=None, data=None, params=None):
    return requests.get(url, headers=headers, data=data, params=params)


def func_logger(func):
    def wrapper(*args, **kwargs):
        pid = os.getpid()
        logger.info(f'[Process-{pid}]"{func.__name__}" Start')
        logger.info(f'[Process-{pid}] Args: {args}')
        logger.info(f'[Process-{pid}] Kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logger.info(f'[Process-{pid}]"{func.__name__}" End')
        return result

    return wrapper


def time2str(time_object: datetime):
    """DateTime to ISO format without microsecond"""
    return time_object.replace(microsecond=0).isoformat()


def str2time(time_object: str):
    """Convert String to DateTime"""
    return datetime.fromisoformat(time_object)


def ts2dt(timestamp: int):
    """Convert timestamp to DateTime Object"""
    return datetime.fromtimestamp(timestamp)


def convert_time_zone(time_object: datetime, from_tz, to_tz):
    """Convert DateTime's Time Zone"""
    return (
        time_object.replace(tzinfo=from_tz)
        .astimezone(to_tz)
        .replace(tzinfo=None)
    )
