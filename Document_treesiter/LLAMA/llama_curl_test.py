import os
import requests
from dotenv import load_dotenv

load_dotenv()

LLAMA_API_KEY = os.getenv("LLAMA-90B_API_KEY")
if not LLAMA_API_KEY:
    print("Error: API key not found.")
    exit()

LLAMA_URL = "https://api.llama.ai/v1/generateContent"
headers = {
    "Authorization": f"Bearer {LLAMA_API_KEY}",
    "Content-Type": "application/json"
}

payload = {"contents": [{"parts": [{"text": "Test request"}]}]}

try:
    response = requests.post(LLAMA_URL, json=payload, headers=headers)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except requests.exceptions.RequestException as e:
    print("API Request Error:", str(e))
