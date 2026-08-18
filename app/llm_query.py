"""
This is a simple test script to connect to groq API server and get a response.
"""

from groq import Groq
from dotenv import load_dotenv
import api_structure
import os
import json

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Query the LLM to convert a user query into an API URL
def query_llm(user_query: str, dataset: dict, analysis: dict) -> str:
    
    # Build a prompt using the user's question and selected dataset
    prompt = f"""
    Convert the user query into a query for the selected dataset.
    
    User query: {user_query}
    
    Selected dataset: {json.dumps(dataset, indent=2)}
    
    Intent and extracted entities: {json.dumps(analysis, indent=2)}
    
    Return only the API URL
    """

    # Ask the LLM to create a query for the selected dataset
    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="hidden",
        max_completion_tokens=1024,
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
    # Return the generated API URL or query
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content.strip())