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

completion = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {
            "role": "user", # Define role of message sender (user, system, etc)
            "content": "Explain why fast inference is critical for reasoning models" # Enter prompt here
        }
    ]
)
print(completion.choices[0].message.content)