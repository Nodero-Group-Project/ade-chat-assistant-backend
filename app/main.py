from db import executeQuery
from fastapi import FastAPI

app = FastAPI()

@app.get("/sampleData")
async def hello():
    data = executeQuery("SELECT * FROM cigarette_smoking limit 5")

    return data