"""
Main application file for the FastAPI server.
This file defines the API endpoints and handles incoming requests.
"""

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

# Report endpoint
@app.get("/report")
async def report(question: str):
    # Receive the user's question and analyse its intent
    analysis = analyse_query(question)
    
    # Stop if no suitable dataset was selected
    if not analysis["selected_dataset_id"]:
        return {
            "question": question,
            "analysis": analysis,
            "data": [],
            "csvFile": None,
        }
        
    # Get the selected dataset using the ID returned by the LLM
    selected_dataset_id = analysis["selected_dataset_id"]
    
    # Find the complete dataset information from datasets.py
    selected_dataset = next(
        dataset
        for dataset in datasets()
        if dataset["id"] == selected_dataset_id
    )
    # Generate a query for the selected dataset
    query_result = llm_query.query_llm(
        user_query=question,
        dataset=selected_dataset,
        analysis=analysis
    )
    # Return the analysis, selected dataset, and generated query to the frontend
    return {
        "question": question,
        "analysis": analysis,
        "selected_dataset": selected_dataset,
        "query_result": query_result,
    }
    
    sql_command = llm_query.query_llm(question, classification)
    print(sql_command)

    data = db.executeQuery(sql_command)

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