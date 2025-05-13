from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from database import models, schemas, crud, session


app = FastAPI()

# for CORS
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:9080",
    "http://10.8.2.130:9080",
    "http://10.8.2.127",
    "https://a6web.dev.ccstech.me"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Time --------------------------------------------------------------------------------------
@app.get("/hi")
def get_hi():
    return {"Hi": "hi"}
    
@app.get("/time")
def get_time():
    return {"time": f"{time.localtime()}"}


# DB --------------------------------------------------------------------------------------
get_db = session.get_db

@app.get("/get_sensor_by_id/{sensor_id}")  
def get_sensor(sensor_id:str, db:Session=Depends(get_db)):  
    return crud.get_sensor_by_id(db, sensor_id)
    
@app.get("/get_smart_by_id/{sensor_id}")  
def get_smart(sensor_id:str, db:Session=Depends(get_db)):  
    return crud.get_all_smart_by_id(db, sensor_id)

@app.post('/create_smart')
def create_smart(request:schemas.SmartMeter, db:Session=Depends(get_db)):
    return crud.create_smart(db,request)

@app.get("/all_data_in_smart")
def get_all_smart(db:Session=Depends(get_db)):
    return crud.get_all_smart_data(db)

@app.get("/all_stragedy")
def get_all_stragedy(db:Session=Depends(get_db)):
    return crud.get_all_strategy(db)