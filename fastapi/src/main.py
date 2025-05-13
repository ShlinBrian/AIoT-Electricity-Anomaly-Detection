from typing import Optional
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put('')

# # If you want to change the port from "8000 -> 9000"
# if __name__ == "__main__": 
#     uvicorn.run(app, host = "127.0.0.1", port=9000)