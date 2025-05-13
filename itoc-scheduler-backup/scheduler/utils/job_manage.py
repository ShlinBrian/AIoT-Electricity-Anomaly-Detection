# Standard Library
from threading import Thread

# Third Party Library
from loguru import logger

# Local Module
from scheduler.config import COMMON
from scheduler.utils.config_class import Executor


class Handler:
    """Execution handler"""

    def __init__(self, execution: Executor, notification: Executor):
        """Constructor

        Arguments:
            execution {Callable} -- Execution algorithm
            notification {Callable} -- Response notification
        """
        self.execution = execution
        self.notification = notification

    def execute_task(self):
        results = self.execution.func(**self.execution.kwargs)
        if COMMON.log_level != 'DEBUG' and self.notification and results:
            self.notification.func(results, **self.notification.kwargs)


class Worker:
    """Repeated Timer for scheduling a execution event"""

    def __init__(self, name, handler: Handler, trigger_type, trigger_time):
        """Constructor

        Arguments:
            handler {Handler} -- execution handler
            trigger_time {schedule.Job} -- schedule job
        """
        logger.debug(f'Start Job: {name}')

        trigger_type(trigger_time).do(self.wrapper, handler.execute_task)
        logger.info(f'{name} trigger {trigger_type.__name__} {trigger_time}\n')

    @staticmethod
    def wrapper(job_func):
        """multi-threading creating

        Arguments:
            job_func {Callable} -- function to be execute
        """
        job_thread = Thread(target=job_func)
        job_thread.start()
