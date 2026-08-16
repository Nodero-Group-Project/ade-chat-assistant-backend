"""
This is a simple test script to connect to groq API server and get a response.
"""

from groq import Groq
from dotenv import load_dotenv
import api_structure
import os
import re

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# get

def query_llm(user_query):

    structure = api_structure.cigarette_smoking()

    completion = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        reasoning_format="parsed",
        max_completion_tokens=1024,
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

    message = completion.choices[0].message
    content = message.content or ""
    
    # If the content is empty, check if there is reasoning information available
    response_text = content
    reasoning = getattr(message, "reasoning", None)
    # If reasoning is available, extract the text from it
    if not response_text and reasoning:
        response_text = reasoning

    url_match = re.search(
        r"https://api\.data\.stats\.govt\.nz/rest/data/\S+",
        response_text,
    )
    # If a URL is found, return it after stripping any trailing punctuation
    if url_match:
        return url_match.group(0).rstrip("`.,\")'")

    # If the response starts with "ERROR:", return the error message
    if response_text.strip().startswith("ERROR:"):
        return response_text.strip()

    raise RuntimeError(
        "The LLM returned no Stats NZ URL. "
        f"Raw response: {response_text!r}"
    )
    

if __name__ == "__main__":
    try:
        result = query_llm("how many young Asian smokers exists in each year?")
        print(result)
    except Exception as error:
        print(f"LLM query failed: {error}")