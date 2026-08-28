"""
This is a simple test script to connect to groq API server and get a response.
"""

from groq import Groq
from dotenv import load_dotenv
import os
from prompts import cigarette_smoking,household_income,telecommunication_system,education,activity_limitations
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Query the LLM to convert a user query into an API URL
def query_llm(user_query: str, dataset: dict):

    prompt = ""

    # select an appropriate prompt depends on selected dataset
    match dataset["id"]:
        case "CEN23_HAD_020":
            prompt = cigarette_smoking.prompt()
        case "CEN23_HOU_001":
            prompt = household_income.prompt()
        case "CEN23_FHH_017":
            prompt = telecommunication_system.prompt()
        case "CEN23_EDU_003":
            prompt = education.prompt()
        case "CEN23_HAD_014":
            prompt = activity_limitations.prompt()

    print(prompt)

    # Ask the LLM to create an URL for the selected dataset
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="hidden",
        max_completion_tokens=4096,
        messages=[
            {
                "role": "system",  # Define role of message sender (user, system, etc)
                "content": prompt  # Enter prompt here
            }
            ,
            {
                "role": "user", # Define role of message sender (user, system, etc)
                "content": user_query, # Enter prompt here
            }
        ]
        
    )

    result = completion.choices[0].message.content.strip()

    # if LLM generates URL
    if result.startswith("API_URL"):
        return {
            "success": True,
            "URL": result.replace("API_URL:", "")
        }
    else:
        # if LLM generates ERROR
        if result.startswith("ERROR"):
            return {
                "success": False,
                "message":result.replace("ERROR:", "")
            }
        else:
            # here is where the LLM generate nothing. Neither URL nor ERROR
            # because of token limitation, or any other unknown reason.
            return {
                "success": False,
                "message":"No data found. Please try again later."
            }