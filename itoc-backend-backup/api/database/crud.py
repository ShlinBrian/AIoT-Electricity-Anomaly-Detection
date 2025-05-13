from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status
from loguru import logger
from datetime import timedelta

def get_sensor_by_id(db:Session, sensor_id:str):
    sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Sensor with the id {sensor_id} is not available")
    return sensor

def get_all_smart_by_id(db:Session, sensor_id:str):
    smart = db.query(models.SmartMeter).filter(models.SmartMeter.id == sensor_id).all()
    return smart

def create_smart(db:Session, request:schemas.SmartMeter):
    new_smart = models.SmartMeter(id=request.id, time=request.time, energy=request.energy)
    db.add(new_smart)
    db.commit()
    db.refresh(new_smart)
    return new_smart

def get_all_smart_data(db:Session):
    # 會不會不同時取，導致數量不同？
    lst = db.query(models.SmartMeter).order_by(models.SmartMeter.time).all()
    s1 = list(filter(lambda x: x.id == 'c1bba7de-9fc1-475c-83ad-38b6941437d6', lst))
    s2 = list(filter(lambda x: x.id == '61695484-f603-478f-ba6f-6b26d7cc1e8e', lst))
    s3 = list(filter(lambda x: x.id == 'b0cab870-7bab-11ec-90d6-0242ac120003', lst))
    # logger.debug(f"{len(s1)=}{len(s2)=}{len(s3)=}")

    # smart1 = db.query(models.SmartMeter).filter(models.SmartMeter.id == "c1bba7de-9fc1-475c-83ad-38b6941437d6").all()
    # smart2 = db.query(models.SmartMeter).filter(models.SmartMeter.id == "61695484-f603-478f-ba6f-6b26d7cc1e8e").all()
    # smart3 = db.query(models.SmartMeter).filter(models.SmartMeter.id == "b0cab870-7bab-11ec-90d6-0242ac120003").all()
    ct = int(len(lst)/3)
    # logger.debug(f'{ct=}')

    smdata = schemas.SMdata(time=[],pc1=[],pc2=[],pc3=[])
    for i in range(ct):
        # logger.debug(f'{i=}')
        # logger.debug(f'{s1=}')
        # logger.debug(f'{s2=}')
        # logger.debug(f'{s3=}')
        smdata.time.append((s1[i].time + timedelta(hours=8)).strftime("%b %d %H:%M:%S"))
        smdata.pc1.append(s1[i].energy)
        smdata.pc2.append(s2[i].energy)
        smdata.pc3.append(s3[i].energy)
    return smdata

    # smartmeterlst = schemas.SmartMeterlst(data=[])
    # for i in range(ct):
    #     logger.debug(f'{i=}')
    #     logger.debug(f'{s1=}')
    #     logger.debug(f'{s2=}')
    #     logger.debug(f'{s3=}')
    #     smartmeterper = schemas.SmartMeterPer()
    #     smartmeterper.time = s1[i].time
    #     smartmeterper.pc1 = s1[i].energy
    #     smartmeterper.pc2 = s2[i].energy
    #     smartmeterper.pc3 = s3[i].energy
    #     smartmeterlst.data.append(smartmeterper)
    # return smartmeterlst

def get_all_strategy(db:Session):
    lst = db.query(models.Strategy).order_by(models.Strategy.timestamp.desc()).all()
    strategydatalist = schemas.StrategyDatalist(data=[])
    for s in lst:
        # logger.debug(f'{s.timestamp=}{s.type=}{s.solution=}')
        strategydata = schemas.StrategyData(Time=s.timestamp.strftime('%Y-%m-%d %H:%M:%S'),Type=s.type,Solution=s.solution)
        strategydatalist.data.append(strategydata)
    return strategydatalist