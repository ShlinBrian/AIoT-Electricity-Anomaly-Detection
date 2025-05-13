import requests
import subprocess
import json
# import sys
from loguru import logger
from datetime import datetime, timedelta

# sys.path.append('/home/ktchen/Documents/itoc/iotc-scheduler/')
from scheduler.utils.database_decorator import database
from scheduler.config import REDIS
from scheduler.model.meter_model import SmartMeter
from scheduler.model.sensor_model import Sensor


@database
def smart_meter_checker(**kwargs):
    logger.info(f'[METER CHECKER] Service Start')
    session = kwargs['session']
    accessToken = json.loads(
        subprocess.check_output(
            ["az", "account", "get-access-token", "--resource", "https://apps.azureiotcentral.com"]
        )
    )['accessToken']

    body = {
        "query": "SELECT TOP 6 $ts, powerConsumption1, powerConsumption2, powerConsumption3 FROM dtmi:modelDefinition:careerhack022:ez33;1 ORDER BY $ts DESC"
    }

    result = requests.post(
        'https://careerhack02-2.azureiotcentral.com/api/query?api-version=1.1-preview',
        headers={'Authorization': f"Bearer {accessToken}"},
        json=body
    ).content

    elect_data = json.loads(result)['results']

    last_time = REDIS.get('last_time')
    REDIS.set('last_time', elect_data[0]['$ts'].split('.')[0], )
    REDIS.expire('last_time', timedelta(minutes=1))
    if last_time:
        elect_data = list(
            filter(
                lambda x: datetime.fromisoformat(x['$ts'].split('.')[0]) > datetime.fromisoformat(last_time.decode('utf-8')),
                elect_data
            )
        )
    if elect_data:
        insert_data = []
        for data in elect_data:
            insert_data.extend(
                [
                    SmartMeter(
                        id=session.query(Sensor.id).filter(Sensor.name == 'powerConsumption1').first().id,
                        time=datetime.fromisoformat(data['$ts'].split('.')[0]),
                        energy=data['powerConsumption1']
                    ),
                    SmartMeter(
                        id=session.query(Sensor.id).filter(Sensor.name == 'powerConsumption2').first().id,
                        time=datetime.fromisoformat(data['$ts'].split('.')[0]),
                        energy=data['powerConsumption2']
                    ),
                    SmartMeter(
                        id=session.query(Sensor.id).filter(Sensor.name == 'powerConsumption3').first().id,
                        time=datetime.fromisoformat(data['$ts'].split('.')[0]),
                        energy=data['powerConsumption3']
                    )
                ]
            )
        session.bulk_save_objects(insert_data)
        session.commit()
        logger.info(f'[METER CHECKER] Service End')
# smart_meter_checker()
