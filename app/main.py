"""
Main application file for the FastAPI server.
This file defines the API endpoints and handles incoming requests.
"""

import datasets
from services import stat_nz
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi import HTTPException
import os
import llm_query
from intent_classification import analyse_query

app = FastAPI()
REPORT_DIR = "exports"

# Report endpoint
@app.get("/report")
async def report(q: str):
    # Receive the user's question and analyse its intent
    analysis = analyse_query(q)
    
    # Stop if no suitable dataset was selected
    if not analysis["selected_dataset_id"]:
        return {
            "success": False,
            "question": q,
            "selected_dataset": "",
            "message": "Unsupported question. Please ask me about something real!"
        }
        
    # Get the selected dataset using the ID returned by the LLM
    selected_dataset_id = analysis["selected_dataset_id"]
    
    # Find the complete dataset information from datasets.py
    selected_dataset = next(
        dataset
        for dataset in datasets.datasets()
        if dataset["id"] == selected_dataset_id
    )
    # Generate a query for the selected dataset
    query_result = llm_query.query_llm(
        user_query=q,
        dataset=selected_dataset,
        analysis=analysis
    )

    # if LLN can translate the question to URL
    if query_result["success"]:
        # get data from stat NZ
        # statNZ api needs format=jsondata to return data in json format
        statistic_data = stat_nz.get(query_result["URL"]+"&format=jsondata")
        if statistic_data:
            return{
                "success": True,
                "question": q,
                "selected_dataset": selected_dataset,  # Selected dataset information to be passed on for retrieval
                "data": statistic_data
            }
        else:
            return{
                "success": False,
                "question": q,
                "selected_dataset": selected_dataset,
                "message": "No data retrieved. Please try again later."
            }
    else:
        return {
            "success": False,
            "question": q,
            "selected_dataset": selected_dataset,
            "message": query_result["message"]
        }



    # Return the analysis, selected dataset, and generated query to the frontend
    # return {
    #     "question": q,
    #     "analysis": analysis,
    #     "selected_dataset": selected_dataset, # Selected dataset information to be passed on for retrieval
    #     "query_result": query_result,
    # }

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