"""
This is a simple test script to connect to groq API server and get a response.
"""

from groq import Groq
from dotenv import load_dotenv
from app.prompts import household_income
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# get

def query_llm(user_query):

    structure = household_income.prompt()

    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        # reasoning_format="hidden",
        messages=[
            {
                "role": "system",  # Define role of message sender (user, system, etc)
                "content": structure  # Enter prompt here
            }
            ,
            {
                "role": "user", # Define role of message sender (user, system, etc)
                "content": user_query, # Enter prompt here
            }
        ]
        
    ) 

    return(completion.choices[0].message.content)
    

if __name__ == "__main__":
    query_llm("how many house owners with more than 70000 household income and their house having kitchen and toilet we have?")