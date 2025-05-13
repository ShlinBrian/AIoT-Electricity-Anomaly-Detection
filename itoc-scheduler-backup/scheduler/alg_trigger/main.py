# import sys
from loguru import logger
import pandas as pd
from datetime import datetime

# sys.path.append('/home/ktchen/Documents/itoc/iotc-scheduler/')
from scheduler.utils.database_decorator import database
from scheduler.model.meter_model import SmartMeter
from algo.detection import detection
from scheduler.notification.mail_prod import MailReport
from scheduler.notification.mail_template.settlement_calculation import (
    generate_report,
)
from algo.knn import knn

@database
def trigger_detection(**kwargs):
    logger.info('[TRIGGER DETECTION] Service Start')
    session = kwargs['session']

    rows = session.query(SmartMeter).order_by(SmartMeter.time.desc()).limit(300)

    data = {}
    data['Timestamp'] = [
        row.time for row in list(
            filter(lambda x: x.id == 'c1bba7de-9fc1-475c-83ad-38b6941437d6', rows)
        )
    ][:90]

    data['PowerConsumption1'] = [
        row.energy for row in list(
            filter(lambda x: x.id == 'c1bba7de-9fc1-475c-83ad-38b6941437d6', rows)
        )
    ][:90]

    data['PowerConsumption2'] = [
        row.energy for row in list(
            filter(lambda x: x.id == 'b0cab870-7bab-11ec-90d6-0242ac120003', rows)
        )
    ][:90]

    data['PowerConsumption3'] = [
        row.energy for row in list(
            filter(lambda x: x.id == '61695484-f603-478f-ba6f-6b26d7cc1e8e', rows)
        )
    ][:90]

    df = pd.DataFrame(data)
    result = detection(df)
    logger.info(f'[TRIGGER DETECTION] Detection Result {result}')

    anomalies = []
    if result[0]:
        nearest1 = knn(df['PowerConsumption1'])
        anomalies.append(
            {
                'meter': 'PowerConsumption1',
                'type': nearest1.type,
                'solution': nearest1.solution,
                'pattern': nearest1.pattern,
                'ptc': 'Power1'
            }
        )

    if result[1]:
        nearest2 = knn(df['PowerConsumption2'])
        anomalies.append(
            {
                'meter': 'PowerConsumption2',
                'type': nearest2.type,
                'solution': nearest2.solution,
                'pattern': nearest2.pattern,
                'ptc': 'Power2'
            }
        )

    if result[2]:
        nearest3 = knn(df['PowerConsumption3'])
        anomalies.append(
            {
                'meter': 'PowerConsumption3s',
                'type': nearest3.type,
                'solution': nearest3.solution,
                'pattern': nearest3.pattern,
                'ptc': 'Power3'
            }
        )

    report = generate_report(anomalies)
    logger.info('[METER CHECKER] Service End')

    return report


# def generate_report(meters):
#     contents = ""
#     logger.info('[MACHINE CHECKER] Generate report')
#     if len(meters) != 0:
#         # contents = '\n'.join(
#         #     [
#         #         f'Checking Time: {datetime.now().strftime("%b %d %Y %H:%M:%S")}',
#         #         f'Anomalous Meters: {meters}',
#         #         f'Probable Cause: TBD',
#         #         f'recommended  Solution: TBD',
#         #     ]
#         # )
#         contents = generate_report()
#     # return MailReport(
#     #     '[ITOC Server] Anomaly Warning', 'plain', contents
#     # )
#     return MailReport(
#         subject='[ITOC Server] Anomaly Warning',
#         subtype='html',
#         content=contents,
#         image=[
#             "scheduler/notification/mail_template/picture/formula.png",
#         ],
#     )

# trigger_detection()
