"""
Intent classification and dataset selection module.
"""

import json
import os
from dotenv import load_dotenv
from groq import Groq
from app.datasets import datasets, intents

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# Analyze the user query and classify it into an intent and select the best dataset
def analyse_query(user_query: str) -> dict:
    
    # Load candidate datasets and valid intents
    candidate_datasets = datasets()
    valid_intents = intents()
    
    # Create a prompt containing the user query and dataset information
    system_prompt = f"""
    You are a query analysis and dataset selection model.
    
    Analyse the raw user query and select the best candidate dataset,
    
    Valid intents:
    {json.dumps(valid_intents)}

    Candidate datasets:
    {json.dumps(candidate_datasets)}
    
    Your tasks are:
    
    1. Identify the user's intent.
    2. Extract important entities and requirements.
    3. Score every candidate dataset from 0.0 to 1.0 based on how well it matches the user's intent and requirements.
    4. Rank the datasets by score from best to worst.
    5. Select the best dataset with the highest score and return its ID.
    
    Score each dataset using:
    -Topic match
    -Meaning match
    -Whether the dataset contains the required entities
    -Whether it contains the requested measures or metrics
    -Whether it covers the requested time period
    -Whether it covers the requested location or demographic group
    
    DO NOT invent dataset IDs
    Only use UDs from the candidate dataset list provided.
    A dataset should recieve a low score if it cannot answer the user's query or if it is missing important entities or metrics.
    
    Return ONLY valid JSON in this exact format:
    
    {{
        "intent": "one valid intent",
  "confidence": 0.0,
  "entities": {{
    "location": "",
    "time": "",
    "topic": "",
    "metric": "",
    "demographic": "",
    "required_dimensions": []
  }},
  "ranked_datasets": [
    {{
      "dataset_id": "one candidate dataset ID",
      "score": 0.0,
      "reason": "short explanation"
    }}
  ],
  "selected_dataset_id": "best candidate dataset ID",
  "selection_confidence": 0.0
    }}
    """
    
    # Send the user query and candidate datasets to the LLM
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="parsed",
        max_completion_tokens=4096,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": user_query},
        ],
    )


    # Extract the LLMs response
    message = completion.choices[0].message
    content = (message.content or "").strip()

    # Models sometimes wrap an otherwise valid JSON response in Markdown.
    # Remove any Markdown formatting before attempting to parse the JSON.
    if content.startswith("```json"):
        content = content[len("```json"):].strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    # Error handling for JSON parsing
    try:
        # Convert the JSON text into a Python dictionary
        result = json.loads(content)
    except json.JSONDecodeError as error:
        finish_reason = completion.choices[0].finish_reason
        return {
            "error": "Failed to parse JSON from LLM response.",
            "parse_error": str(error),
            "finish_reason": finish_reason,
            "raw_content": content,
        }
    
    valid_intents = set(intents())
    
    # Get the IDs of valid datasets form datasets.py
    valid_dataset_ids = {dataset["id"] for dataset in datasets()}
    
    result.setdefault("confidence", 0.0)
    result.setdefault("entities", {})
    result.setdefault("ranked_datasets", [])
    result.setdefault("selection_confidence", 0.0)
    
    # Keep only dataset rankings with valid dataset IDs
    valid_rankings = []
    
    
    # Check each candidate returned by the LLM
    for candidate in result.get("ranked_datasets", []):
        dataset_id = candidate.get("dataset_id")
        score = candidate.get("score", 0.0)
        reason = candidate.get("reason", "")
        
        # Ignore datasets that do no exist in datasets.py
        if dataset_id in valid_dataset_ids:
            valid_rankings.append({
                "dataset_id": dataset_id,
                "score": score,
                "reason": reason
            })
    
    # Sort datasets from highest score to lowest score
    valid_rankings.sort(key=lambda x: x["score"], reverse=True)
    
    # Store the validated rankings in the result
    result["ranked_datasets"] = valid_rankings
    
    
    # Select the highest scoreing valid dataset
    if valid_rankings:
        best_dataset = valid_rankings[0]
        result["selected_dataset_id"] = best_dataset["dataset_id"]
        result["selection_confidence"] = best_dataset["score"]
    else:
        # No suitable dataset was found
        result["selected_dataset_id"] = None
        result["selection_confidence"] = 0.0
    
    return result

if __name__ == "__main__":
    query = "" # Enter in a user query here, need to connect to front end
    result = analyse_query(query)
    print(json.dumps(result, indent=2))