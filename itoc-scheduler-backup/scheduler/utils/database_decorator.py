# Third Party Library
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import sessionmaker

# Local Module
from scheduler.config import DB_ENGINE


def database(schedule):
    def wrapper(**kwargs):
        try:
            session = sessionmaker(bind=DB_ENGINE)()
            kwargs['session'] = session
            report = schedule(**kwargs)
            if report:
                return report
            return None

        except DBAPIError:
            session.rollback()

        finally:
            session.close()

    return wrapper
