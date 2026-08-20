"""
This is a simple test script to connect to groq API server and get a response.
"""

from groq import Groq
from dotenv import load_dotenv
from app.prompts import education_structure
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# get

def query_llm(user_query):

    structure = education_structure.prompt()

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
    print(query_llm("how many people can get certificated more than bachelor in each year?"))