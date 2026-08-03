# This script attempts to query the Stats NZ API 

# Imports
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env.local file
load_dotenv(".env.local")
subscription_key = os.getenv("subscription_key")
key_name = os.getenv("key_name")

# API endpoint for 2023 census housing data
url = "https://api.data.stats.govt.nz/rest/data/STATSNZ,CEN23_HOU_002,1.0/2023...?dimensionAtObservation=AllDimensions"

# Set the request headers with the subscription key and accept XML response
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key, "Accept": "application/xml"
}

# Make the GET request to the Stats NZ API
response = requests.get(url, headers=headers)
body = response.text

# Print the response status code and content type
print("status:", response.status_code)
print("content-type:", response.headers.get("content-type"))
with open("stats_response.sdmx.xml", "w", encoding="utf-8") as f:
    f.write(body)

# File is very large so dont open it



