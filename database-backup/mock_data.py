from time import time
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
from dateutil.rrule import rrule, MONTHLY
from datetime import datetime
import uuid, random
###########
from tables.strategy.strategy_model import Strategy
###########

ENGINE: Engine = create_engine('postgresql://nighteen_gale:password@localhost:5435/itoc')
session: Session = sessionmaker(bind=ENGINE)()

df = pd.read_csv('simulate_dataset.csv')
df = df.drop(['Unnamed: 0'], axis=1)
dfval = df.values  
dflst = dfval.tolist()  # nested list
random.shuffle(dflst)
mock_data = []
classdict = {
    'type-A':{'type':'學長帶女友來偷電', 'solution':'拔插頭'},
    'type-B':{'type':'學長煮火鍋', 'solution':'一起吃'},
    'type-C':{'type':'學長吃雞', 'solution':'拔插頭'},
    'type-D':{'type':'學長Train module', 'solution':'拔插頭'},
    'type-E':{'type':'學長挖礦', 'solution':'拔插頭'}
    }

start_date = datetime(2016, 1, 1)
timestamplst = list(rrule(freq=MONTHLY, count=50, dtstart=start_date))

for i in range(len(dflst)):
    templst = dflst[i]
    uid = uuid.uuid4()
    temptype = classdict[f'{dflst[i][-1]}']['type']
    tempsolution = classdict[f'{dflst[i][-1]}']['solution']
    pat=templst[:-1]
    pat=[round((x/10.0),2) for x in pat]
    CurrentS = Strategy(schedule_id=uid, pattern=pat, type=temptype, solution=tempsolution, timestamp=timestamplst[i])
    mock_data.append(CurrentS)

session.bulk_save_objects(mock_data)
session.commit()
session.close()