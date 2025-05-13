# all pydantic model
from ctypes.wintypes import DOUBLE
from datetime import datetime
from optparse import Option
from tokenize import Double
from typing import List, Optional
from pydantic import BaseModel

class SmartMeter(BaseModel):
    id: Optional[str]
    time: Optional[datetime]
    energy: Optional[float]

    class Config():
        orm_mode = True

class SmartMeterlst(BaseModel):
    data: list

class SmartMeterPer(BaseModel):
    time: Optional[str]
    pc1: Optional[float]
    pc2: Optional[float]
    pc3: Optional[float]

class Sensor(BaseModel):
    id: Optional[str]
    name: Optional[str]
    class Config():
        orm_mode = True    

class SMdata(BaseModel):
    time: Optional[list]
    pc1: Optional[list]
    pc2: Optional[list]
    pc3: Optional[list]


class StrategyData(BaseModel):
     Time: Optional[datetime]
     Type: Optional[str]
     Solution: Optional[str]

class StrategyDatalist(BaseModel):
    data: Optional[list]

