"""
Main application file for the FastAPI server.
This file defines the API endpoints and handles incoming requests.
"""

from app.datasets import datasets
from app.models.Intent import Intent
from app.models.Dataset import Dataset
from app.services import stat_nz
from fastapi import FastAPI
from app.llm_query import query_llm
from app.intent_classification import analyse_query
from fastapi.middleware.cors import CORSMiddleware
from app.db import intent_get_all, intent_insert, intent_exists, intent_delete, dataset_get_all, dataset_insert,dataset_exists,dataset_delete,dataset_update

web = FastAPI()

# please replace * in allow_origins with the frontend URL
web.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin
    allow_methods=["*"],
    allow_headers=["*"],
)

REPORT_DIR = "exports"

# Report endpoint
@web.get("/report")
async def report(q: str):
    # Receive the user's question and analyse its intent
    analysis = analyse_query(q)

    # Do not retrieve data when the selected dataset is not a strong match.
    if analysis.get("selection_confidence", 0.0) < 0.5:
        return {
            "success": False,
            "question": q,
            "selected_dataset": "",
            "message": "Unfortunately we can't provide any data for your question."
        }

    # Get the selected dataset using the ID returned by the LLM
    selected_dataset_id = analysis["selected_dataset_id"]

    # Find the complete dataset information from datasets.py
    selected_dataset = next(
        dataset
        for dataset in datasets()
        if dataset["id"] == selected_dataset_id
    )

    # Try to generate a valid StatNZ URL for user question.
    query_result = query_llm(
        user_query=q,
        dataset=selected_dataset
    )

    # if LLN can translate the question to URL
    if query_result["success"]:

        # get data from stat NZ
        # statNZ api needs "format=jsondata" to return data in json format
        statistic_data = stat_nz.get(query_result["URL"]+"&format=jsondata")

        # if we get data from StatNZ
        if statistic_data:
            return{
                "success": True,
                "question": q,
                "selected_dataset": selected_dataset,  # Selected dataset information to be passed on for retrieval
                "data": statistic_data
            }
        else:
            # if statNZ doesn't return data
            return{
                "success": False,
                "question": q,
                "selected_dataset": selected_dataset,
                "message": "No data retrieved. Please try again later."
            }
    else:
        # if LLM couldn't find any URL we return the reason
        return {
            "success": False,
            "question": q,
            "selected_dataset": selected_dataset,
            "message": query_result["message"]
        }


@web.get("/intent")
async def intent_get():
    intents = intent_get_all()

    return [
        {
            "Description": intent.Description
        }
        for intent in intents
    ]

@web.post("/intent")
async def intent_add(intent: Intent):
    if intent_exists(intent.Description):
        return {
            "success": False,
            "message": 'The intent already exists.'
        }

    intent_insert(intent.Description)

    return {
        "success": True,
        "message": 'The intent added successfully.'
    }

@web.delete("/intent")
async def intent_remove(description: str):
    deleted = intent_delete(description)

    if not deleted:
        return {
            "success": False,
            "message": "Cannot remove the intent."
        }
    else:
        return {
            "success": True,
            "message": "Intent removed successfully."
        }

@web.get("/dataset")
async def dataset_get():
    datasets = dataset_get_all()

    return [
        {
            "Id":dataset.Id,
            "Name":dataset.Name,
            "Description": dataset.Description,
            "Skill":dataset.Skill
        }
        for dataset in datasets
    ]

@web.post("/dataset")
async def dataset_add(dataset: Dataset):
    if dataset_exists(dataset.Id):
        return {
            "success": False,
            "message": 'The dataset already exists.'
        }

    dataset_insert(dataset.Id,dataset.Name,dataset.Description,dataset.Skill)

    return {
        "success": True,
        "message": 'The dataset added successfully.'
    }

@web.delete("/dataset")
async def dataset_remove(id: str):
    deleted = dataset_delete(id)

    if not deleted:
        return {
            "success": False,
            "message": "Cannot remove the dataset."
        }
    else:
        return {
            "success": True,
            "message": "Dataset removed successfully."
        }

@web.put("/dataset")
async def dataset_edit(dataset: Dataset):
    updated = dataset_update(dataset.Id,dataset.Name,dataset.Description,dataset.Skill)

    if not updated:
        return {
            "success": False,
            "message": "Cannot edit the dataset."
        }
    else:
        return {
            "success": True,
            "message": "Dataset updated successfully."
        }
