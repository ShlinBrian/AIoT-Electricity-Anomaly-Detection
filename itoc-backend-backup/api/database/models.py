from sqlalchemy import (
    ARRAY,
    INT,
    VARCHAR,
    TIMESTAMP,
    Column,
    FLOAT,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SmartMeter(Base):
    __tablename__ = "smart_meter"
    id = Column(VARCHAR, ForeignKey("sensor.id"), primary_key=True)
    time = Column(TIMESTAMP, primary_key=True)
    energy = Column(DOUBLE_PRECISION)

class Sensor(Base):
    __tablename__ = "sensor"
    id = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR)

class Strategy(Base):
    __tablename__ = 'strategy'
    schedule_id = Column(UUID(as_uuid=True), unique=True, primary_key=True)
    pattern = Column(ARRAY(FLOAT), nullable=False)
    type = Column(VARCHAR, nullable=True)
    solution = Column(VARCHAR, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)