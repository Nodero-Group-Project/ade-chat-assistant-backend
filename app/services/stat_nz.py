import json
import urllib.request
import urllib.error
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("STAT_NZ_API_KEY")

def get(url: str):
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
