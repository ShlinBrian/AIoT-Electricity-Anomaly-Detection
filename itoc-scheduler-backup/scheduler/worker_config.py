# Standard Library
from typing import List

# Local Module
from scheduler.meter_checker.main import smart_meter_checker
from scheduler.alg_trigger.main import trigger_detection
from scheduler.utils.config_class import Executor, Job
from scheduler.notification.mail_prod import mail_report
from scheduler.schedule_trigger import every_minute_at

# fmt: off
JOBS: List[Job] = [
    Job(
        name='smart-meter-checker',
        enable=True,  # ?????
        trigger_type=every_minute_at,
        trigger_time=['00', '10', '20', '30', '40', '50'],  # trigger per 10 minute ?????
        execute=Executor(
            func=smart_meter_checker,  # function you want to trigger
            kwargs={}
        ),
        notify=None  # No need notify
    ),
    Job(
        name='alg-trigger',
        enable=False,
        trigger_type=every_minute_at,
        trigger_time=['00'],
        execute=Executor(
            func=trigger_detection,
            kwargs={}
        ),
        notify=Executor(
            func=mail_report,
            kwargs={
                'recipient': [
                    'ktchen@netdb.csie.ncku.edu.tw '
                ]
            }
        )
    ),
]
# fmt: on
