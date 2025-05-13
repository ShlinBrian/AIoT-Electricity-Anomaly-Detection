# Standard Library
from time import sleep

# Third Party Library
from loguru import logger

# Local Module
from scheduler.config import COMMON, SCHEDULE
from scheduler.utils.job_manage import Handler, Worker
from scheduler.worker_config import JOBS


def generate_workers():
    for job in JOBS:
        logger.info(f'JOB - {job} {"Enable" if job.enable else "Disable"}')
        if job.enable:
            job_handler = Handler(
                execution=job.execute, notification=job.notify
            )
            for trigger_time in job.trigger_time:
                Worker(
                    f'{job.name}', job_handler, job.trigger_type, trigger_time
                )


def main():
    logger.info(f'DEBUG_MODE: {COMMON.log_level}')
    generate_workers()

    while 1:
        # due to global schedule object sharing, start schedule would start all worker
        sleep(1)
        SCHEDULE.run_pending()


if __name__ == '__main__':
    main()
