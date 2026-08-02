from db import executeQuery
from fastapi import FastAPI

app = FastAPI()

@app.get("/sampleData")
async def hello():
    data = executeQuery("select * from cigarette_smoking where cen23_geo_008 = '9999' and cen23_cig_002 = '01' and cen23_eth_004 = '12913' and cen23_age_008 = '2'")

    return data