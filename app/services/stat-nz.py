import urllib.request
import urllib.error
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("STAT_NZ_API_KEY")

def get(url: str):
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        # 'accept-encoding': 'identity',
        # 'Cache-Control': 'no-cache',
        'user-agent':'Nodero'
    }

    print(headers)

    request = urllib.request.Request(
        url=url,
        headers=headers,
        method="GET"
    )

    try:
        with urllib.request.urlopen(request) as response:
            return response.read()

    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
        print("Response:")
        print(e.read().decode("utf-8"))
        return {"error": "can not retrieve data."}

    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        return {"error": "can not retrieve data."}

if __name__ == "__main__":
    print(get("https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_HOU_001,1.0/2023.9999.3+6.5+6+7.001?dimensionAtObservation=AllDimensions&format=jsondata"))