import os
import random
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
# Third Party Library
from sqlalchemy.orm import sessionmaker

# Local Module
import uuid
from datetime import datetime
from scheduler.config import DB_ENGINE
from scheduler.model.stratergy_model import Strategy
import matplotlib.pyplot as plt


def knn(anomaly):
    session = sessionmaker(bind=DB_ENGINE)()
    records = session.query(Strategy).all()

    patterns = [record.pattern for record in records]
    label = [record.type for record in records]

    model = KNeighborsClassifier(n_neighbors=5, weights='distance', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=1)
    model.fit(patterns, label)

    dist, nearests = model.kneighbors(X=anomaly, n_neighbors=None, return_distance= True)

    idx = nearests[0][0]

    nearest = records[idx]

    new_strategy = Strategy(
        schedule_id=uuid.uuid4(),
        pattern=nearest.pattern,
        timestamp=datetime.now()
    )

    plt.plot([i for i in range(90)],nearest,label='History Anomaly')
    plt.plot([i for i in range(90)],anomaly,label='New Anomaly')
    plt.savefig(f"{os.environ.get('IMG_PATH')}{new_strategy.schedule_id}.png")

    session.add(new_strategy)
    session.commit()
    session.close()

    return nearest
