# Third Party Library
from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

# Local Module
from utils.base import Base


class SmartMeter(Base):
    __tablename__ = 'smart_meter'
    id = Column(VARCHAR, ForeignKey('sensor.id'), primary_key=True)
    time = Column(TIMESTAMP, primary_key=True)
    energy = Column(DOUBLE_PRECISION)
