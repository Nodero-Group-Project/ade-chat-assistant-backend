import db
from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime
from fastapi import HTTPException
import os
import llm_query

app = FastAPI()
REPORT_DIR = "exports"

@app.get("/report")
async def report(question: str):

    sql_command = llm_query.query_llm(question)
    print(sql_command)

    data = db.executeQuery(sql_command)

    # data = db.executeQuery("select * from cigarette_smoking where cen23_geo_008 = '9999' and cen23_cig_002 = '01' and cen23_eth_004 = '12913' and cen23_age_008 = '2'")

    if not data:
        return {}

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".csv"
    file_path = os.path.join(REPORT_DIR, filename)

    db.write_csv(data,file_path)

    return {
        "data":data,
        "csvFile":filename
    }

@app.get("/download")
async def download(filename: str):
    file_path = os.path.join(REPORT_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="text/csv"
    )