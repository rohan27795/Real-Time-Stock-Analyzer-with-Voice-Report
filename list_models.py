import requests
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("EURI_API_KEY")

url = "https://api.euron.one/api/v1/euri/models"
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json"
}

try:
    print(f"Listing models from: {url}")
    r = requests.get(url, headers=headers, timeout=5)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
