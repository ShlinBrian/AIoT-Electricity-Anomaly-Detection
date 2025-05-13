# Third Party Library
from sqlalchemy import VARCHAR, Column

# Local Module
from scheduler.model.base import BASE


class Sensor(BASE):
    __tablename__ = 'sensor'
    id = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR)