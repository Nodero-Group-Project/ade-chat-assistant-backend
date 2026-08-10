from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

intents = [
"find_....statistics",
"find....statistics",
"find...._statistics"
]

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

SMOKING_INTENTS = [
    # --- Core smoking status ---
    "find_smoking_status_overview",       # regular smoker / ex-smoker / never smoked, general split
    "find_daily_smoking_rate",
    "find_smoking_prevalence_trends",     # change over time / historical trend

    # --- Demographic breakdowns ---
    "find_smoking_by_age",
    "find_smoking_by_sex",
    "find_smoking_by_ethnicity",
    "find_smoking_by_region",             # regional council / territorial authority
    "find_smoking_by_deprivation_index",  # NZDep / socioeconomic deprivation
    "find_smoking_by_occupation",
    "find_smoking_by_income",
    "find_smoking_by_education_level",

    # --- Specific population groups ---
    "find_youth_smoking_statistics",
    "find_smoking_during_pregnancy",
    "find_secondhand_smoke_exposure",

    # --- Fallback ---
    "general_smoking_query"
]


prompt = """
You are a intent classification model for a dataset search system

Classify to one of the following intents: {SMOKING_INTENTS}

Return in the format...
"""

def classify_intent(user_query, intents):
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="hidden",
        messages=[
            {
                "role": "system",
                "content": prompt.format(intents=intents)
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
    )
    print(completion.choices[0].message.content)
