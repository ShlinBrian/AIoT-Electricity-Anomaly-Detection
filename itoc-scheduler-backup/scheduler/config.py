# Standard Library
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

# Third Party Library
import redis
import schedule
import sqlalchemy
from pytz import timezone
from pytz.tzinfo import DstTzInfo

STATISTIC_TIME_FORMAT = '%H:%M'


@dataclass
class SmartMeterConfig:
    notify_tz: DstTzInfo
    meter_check_interval: int
    meter_count_threshold: int
    meter_type: str
    meter_id: List[str]


@dataclass
class CommonConfig:
    log_level: str
    api_host: str
    mail_account: str
    mail_password: str
    smtp_host: str
    smtp_port: int
    http_req_retry_time: int


@dataclass
class DataURLConfig:
    meta_meter: str
    meter_data: str
    missing_data: str


@dataclass
class TimeDelta:
    start: timedelta
    end: timedelta

    def __init__(self, start=0, end=0):
        self.start = timedelta(days=start)
        self.end = timedelta(days=end)


@dataclass
class Time:
    start: datetime
    end: datetime

    def __init__(self, start='00:00', end='00:00'):
        self.start = datetime.strptime(start, STATISTIC_TIME_FORMAT)
        self.end = datetime.strptime(end, STATISTIC_TIME_FORMAT)


@dataclass
class StatisticConfig:
    day_delta: TimeDelta
    time: Time
    notify_tz: DstTzInfo
    report_gw_id: List[str]

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        day_delta=TimeDelta(),
        time=Time(),
        notify_tz='Asia/Taipei',
        report_gw_id=None,
        field='UDC Server',
    ):
        self.day_delta = day_delta
        self.time = time
        self.notify_tz = timezone(notify_tz)
        self.report_gw_id = report_gw_id
        self.field = field

    # pylint: enable=too-many-arguments


@dataclass
class MachineConfig:
    machine_id: str
    machine_host: str


SCHEDULE = schedule

COMMON = CommonConfig(
    str(os.environ.get('LOG_LEVEL', 'INFO')),
    str(os.environ.get('API_HOST', 'http://0.0.0.0:60500')),
    str(os.environ.get('MAIL_ACCOUNT')),
    str(os.environ.get('MAIL_PASSWORD')),
    str(os.environ.get('SMTP_HOST', 'smtp.gmail.com')),
    int(str(os.environ.get('SMTP_PORT', '465'))),
    int(str(os.environ.get('HTTP_REQ_RETRY_TIME', 3))),
)

DATA_URL = DataURLConfig(
    COMMON.api_host + '/meta/meter',
    COMMON.api_host + '/data/meter',
    COMMON.api_host + '/data/missing-data',
)

SMART_METER = SmartMeterConfig(
    timezone(str(os.environ.get('NOTIFY_TZ', 'Asia/Taipei'))),
    int(os.environ.get('METER_CHECK_INTERVAL', 30)),
    int(os.environ.get('METER_COUNT_THRESHOLD', 30)),
    str(os.environ.get('METER_TYPE')),
    str(os.environ.get('METER_ID')).split(','),
)

# Add MachineConfig instance in the list
REDIS = redis.StrictRedis.from_url(
    os.environ.get("REDIS_URL", "redis://:password@localhost:6379/1")
)

# Build connection to database
DB_ENGINE = sqlalchemy.create_engine(
    os.environ.get(
        'DB_URL', 'postgresql://nighteen_gale:password@localhost:5433/itoc'
    )
)

