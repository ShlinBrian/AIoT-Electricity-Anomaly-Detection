# Third Party Library
from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Column,
    FLOAT,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID

# Local Module
from utils.base import Base


class Strategy(Base):
    __tablename__ = 'strategy'
    schedule_id = Column(UUID(as_uuid=True), unique=True, primary_key=True)
    pattern = Column(ARRAY(FLOAT), nullable=False)
    type = Column(VARCHAR, nullable=True)
    solution = Column(VARCHAR, nullable=True)
    timestamp = Column(TIMESTAMP, nullable=False)
