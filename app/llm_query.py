"""
This is a simple test script to connect to groq API server and get a response.
"""

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# get

def query_llm(user_query):
    db_structure = "on a postgres database there is table called cigarette_smoking "
    db_structure += "ONLY write a SQL query to answer the the users questions, DO NOT RETURN ANYTHING ELSE"

    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="hidden",
        messages=[
            {
                "role": "system",  # Define role of message sender (user, system, etc)
                "content": db_structure  # Enter prompt here
            }
            ,
            {
                "role": "user", # Define role of message sender (user, system, etc)
                "content": user_query, # Enter prompt here
            }
        ]
        
    ) 
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)
    

if __name__ == "__main__":
    query_llm("What is the average age of cigarette smokers in the database?")