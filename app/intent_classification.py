"""
Dataset selection module.
"""

import json
import os
from groq import Groq
from app.datasets import datasets
from app.llm_usage import log_usage

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Picking one of a handful of datasets is simple, so the smaller model is enough
MODEL = "openai/gpt-oss-20b"

# One compact line per dataset; the description already contains everything in the name
DATASET_LINES = "\n".join(f"{dataset['id']}: {dataset['description']}" for dataset in datasets())

# Built once and kept identical between requests so Groq can cache the prefix
SYSTEM_PROMPT = f"""Select the dataset that can answer the user's question.

Datasets:
{DATASET_LINES}

A dataset only matches if it covers the requested topic, measures, time period and location/demographic.
Never invent dataset IDs. If no dataset can answer the question, use null.

Return ONLY JSON: {{"dataset_id": "<ID or null>", "confidence": <0.0-1.0>}}"""


# Analyze the user query and select the best dataset
def analyse_query(user_query: str) -> dict:

    # Send the user query and candidate datasets to the LLM
    completion = client.chat.completions.create(
        model=MODEL,
        reasoning_format="hidden",
        reasoning_effort="low",
        response_format={"type": "json_object"},
        max_completion_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    usage = log_usage("analyse_query", MODEL, completion)

    # Extract the LLMs response
    content = (completion.choices[0].message.content or "").strip()

    # Error handling for JSON parsing
    try:
        # Convert the JSON text into a Python dictionary
        result = json.loads(content)
    except json.JSONDecodeError as error:
        return {
            "error": "Failed to parse JSON from LLM response.",
            "parse_error": str(error),
            "finish_reason": completion.choices[0].finish_reason,
            "raw_content": content,
            "selected_dataset_id": None,
            "selection_confidence": 0.0,
            "usage": usage,
        }

    # Get the IDs of valid datasets form datasets.py
    valid_dataset_ids = {dataset["id"] for dataset in datasets()}
    dataset_id = result.get("dataset_id")

    # Ignore datasets that do not exist in datasets.py
    if dataset_id in valid_dataset_ids:
        analysis = {
            "selected_dataset_id": dataset_id,
            "selection_confidence": float(result.get("confidence", 0.0)),
        }
    else:
        # No suitable dataset was found
        analysis = {
            "selected_dataset_id": None,
            "selection_confidence": 0.0,
        }

    analysis["usage"] = usage

    print(analysis)

    return analysis

if __name__ == "__main__":
    query = "" # Enter in a user query here, need to connect to front end
    analyse_result = analyse_query(query)
    print(json.dumps(analyse_result, indent=2))
