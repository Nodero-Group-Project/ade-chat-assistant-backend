import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SMOKING_INTENTS = [
    "find_smoking_status_overview",
    "find_daily_smoking_rate",
    "find_smoking_prevalence_trends",
    "find_smoking_by_age",
    "find_smoking_by_sex",
    "find_smoking_by_ethnicity",
    "find_smoking_by_region",
    "find_smoking_by_deprivation_index",
    "find_smoking_by_occupation",
    "find_smoking_by_income",
    "find_smoking_by_education_level",
    "find_youth_smoking_statistics",
    "find_smoking_during_pregnancy",
    "find_secondhand_smoke_exposure",
    "general_smoking_query",
]

CLASSIFICATION_PROMPT = """
You are an intent classification model for a dataset search system.

Given the user query, classify it as exactly one of these intents:
{intents}

Extract any entities mentioned in the query, such as location, time period,
topic, or metric.

Return only valid JSON in this exact format:
{{
  "intent": "<one of the intents above>",
  "confidence": <float between 0 and 1>,
  "entities": {{
    "location": "",
    "time": "",
    "topic": "",
    "metric": ""
  }}
}}
"""


def classify_intent(user_query: str) -> dict:
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="hidden",
        messages=[
            {
                "role": "system",
                "content": CLASSIFICATION_PROMPT.format(intents=SMOKING_INTENTS),
            },
            {"role": "user", "content": user_query},
        ],
    )

    raw_text = completion.choices[0].message.content.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError:
        return {
            "intent": "general_smoking_query",
            "confidence": 0.0,
            "entities": {},
        }

    if result.get("intent") not in SMOKING_INTENTS:
        result["intent"] = "general_smoking_query"

    result.setdefault("confidence", 0.0)
    result.setdefault("entities", {})
    return result
