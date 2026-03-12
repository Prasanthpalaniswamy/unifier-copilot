import os
import requests
import json
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

BASE_URL = os.getenv("UNIFIER_BASE_URL")
USERNAME = os.getenv("UNIFIER_USERNAME")
PASSWORD = os.getenv("UNIFIER_PASSWORD")

def get_token():
    url = f"{BASE_URL}/login"
    response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), timeout=30)
    return response.json().get("token")

token = get_token()
headers = {"Authorization": f"Bearer {token}"}
url = f"{BASE_URL}/ds/data-elements"

filter_obj = {"data_definition": "Decimal Amount"}

# Test 1: ?filter=JSON
print("Test 1: Using ?filter=...")
res1 = requests.get(url, headers=headers, params={"filter": json.dumps(filter_obj)}, timeout=30)
data1 = res1.json().get("data", [])
print(f"Result count: {len(data1)}")
if data1: 
    print(f"First element: {data1[0].get('data_element')} - Def: {data1[0].get('data_definition')}")

# Test 2: ?options={"filter": ...}
print("\nTest 2: Using ?options=...")
res2 = requests.get(url, headers=headers, params={"options": json.dumps({"filter": filter_obj})}, timeout=30)
data2 = res2.json().get("data", [])
print(f"Result count: {len(data2)}")
if data2: 
    print(f"First element: {data2[0].get('data_element')} - Def: {data2[0].get('data_definition')}")
