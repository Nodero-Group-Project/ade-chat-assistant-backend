import json
import urllib.request
import urllib.error
from dotenv import load_dotenv
import os


def get(url: str):
    api_key = os.getenv("STAT_NZ_API_KEY")
    
    if not api_key:
        print("STAT_NZ_API_KEY is not set - check .env file and that load_dotenv() has been called")
        return None
    
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'user-agent':'Nodero'
    }

    request = urllib.request.Request(
        url=url,
        headers=headers,
        method="GET"
    )

    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        print("Response:")
        print(e.read().decode("utf-8"))
        return None

    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        return None
