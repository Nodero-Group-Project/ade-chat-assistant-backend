# This is a simple test script to check if I could connect to a local LLM API server and get a response.
import requests

# Make a POST request to the API server with a sample prompt and model
r = requests.post(
    "http://localhost:11434/api/generate", # default port 
    json={
        "model": "qwen2.5:7b-instruct",
        "prompt": "Hello, how are you?", # Enter your prompt here
        "stream": False
    },
    timeout=120
)
print(r.status_code, r.text)