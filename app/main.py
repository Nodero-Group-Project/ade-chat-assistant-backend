from app.datasets import datasets
from app import db
from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime
from fastapi import HTTPException
import os
from app import llm_query
from app.intent_classification import analyse_query

app = FastAPI()
REPORT_DIR = "exports"

@app.get("/report")
async def report(question: str):
    analysis = analyse_query(question)
    
    if not analysis["selected_dataset_id"]:
        return {
            "question": question,
            "analysis": analysis,
            "data": [],
            "csvFile": None,
        }
    selected_dataset_id = analysis["selected_dataset_id"]
    
    selected_dataset = next(
        dataset
        for dataset in datasets()
        if dataset["id"] == selected_dataset_id
    )
    query_result = llm_query.query_llm(
        user_query=question,
        dataset=selected_dataset,
        analysis=analysis
    )
    
    return {
        "question": question,
        "analysis": analysis,
        "selected_dataset": selected_dataset,
        "query_result": query_result,
    }
    
    sql_command = llm_query.query_llm(question, classification)
    print(sql_command)

    data = db.executeQuery(sql_command)

    # data = db.executeQuery("select * from cigarette_smoking where cen23_geo_008 = '9999' and cen23_cig_002 = '01' and cen23_eth_004 = '12913' and cen23_age_008 = '2'")

    if not data:
        return {
            "classification": classification,
            "data": [],
            "csvFile": None,
        }

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".csv"
    file_path = os.path.join(REPORT_DIR, filename)

    db.write_csv(data,file_path)

    return {
        "classification": classification,
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