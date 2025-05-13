# Third Party Library
from sqlalchemy import VARCHAR, Column

# Local Module
from utils.base import Base


class Sensor(Base):
    __tablename__ = 'sensor'
    id = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR)