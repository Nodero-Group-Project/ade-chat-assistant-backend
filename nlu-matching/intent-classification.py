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




prompt = """
You are a intent classification model for a dataset search system

Classify to one of the following intents: {intents}

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
