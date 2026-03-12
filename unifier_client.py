import os
import json
import requests
from pathlib import Path
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# -------------------------------
# Load environment variables once
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# BASE_URL = os.getenv("UNIFIER_BASE_URL", "http://169.224.230.179:7001/ws/rest/service/v1")
BASE_URL = os.getenv("UNIFIER_BASE_URL")
USERNAME = os.getenv("UNIFIER_USERNAME")
PASSWORD = os.getenv("UNIFIER_PASSWORD")

# -------------------------------
# Global session + token cache
# -------------------------------
SESSION = requests.Session()
TOKEN = None


# -------------------------------
# Authentication
# -------------------------------
def get_token(force_refresh=False):
    global TOKEN
    
    if force_refresh:
        TOKEN = None

    if TOKEN:
        return TOKEN

    if not USERNAME or not PASSWORD:
        raise ValueError("UNIFIER_USERNAME and UNIFIER_PASSWORD must be set")

    url = f"{BASE_URL}/login"

    response = SESSION.get(
        url,
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        timeout=30
    )

    response.raise_for_status()

    data = response.json()
    TOKEN = data.get("token")

    if not TOKEN:
        raise ValueError("Token not found in login response")

    return TOKEN


# -------------------------------
# Helper request function
# -------------------------------
def unifier_get(endpoint, params=None):
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    url = f"{BASE_URL}{endpoint}"

    response = SESSION.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code == 401:
        # Token might be expired, refresh and retry once
        token = get_token(force_refresh=True)
        headers["Authorization"] = f"Bearer {token}"
        response = SESSION.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

    response.raise_for_status()

    return response.json()


def unifier_post(endpoint, data):
    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{endpoint}"

    response = SESSION.post(
        url,
        headers=headers,
        json=data,
        timeout=30
    )

    if response.status_code == 401:
        # Token might be expired, refresh and retry once
        token = get_token(force_refresh=True)
        headers["Authorization"] = f"Bearer {token}"
        response = SESSION.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

    response.raise_for_status()

    return response.json()


# -------------------------------
# Unifier API Wrappers
# -------------------------------
def get_projects(shell_type="Projects"):
    options = {
        "filter": {
            "shell_type": shell_type
        }
    }

    params = {
        "options": json.dumps(options)
    }

    return unifier_get("/admin/shell", params=params)


def get_project_cost(project_id):
    return unifier_get(f"/projects/{project_id}/cost")


def get_rfis(project_id):
    return unifier_get(f"/projects/{project_id}/rfis")


def get_data_elements(filter_options=None):
    """
    Fetch data elements from Unifier.
    filter_options: dict containing data_element, data_definition, form_label, description, tooltip
    """
    params = {}
    if filter_options:
        params["filter"] = json.dumps(filter_options)

    return unifier_get("/ds/data-elements", params=params)


def get_data_definitions(df_type=None, filter_options=None):
    """
    Fetch data definitions from Unifier.
    df_type: Basic, Cost Codes, Data Picker
    filter_options: dict containing name, data_source
    """
    params = {}
    if df_type:
        params["type"] = df_type
    if filter_options:
        params["filter"] = json.dumps(filter_options)

    return unifier_get("/ds/data-def", params=params)


def create_data_elements(elements_list):
    """
    Create custom data elements in Unifier.
    elements_list: list of dicts containing data_element, data_definition, form_label, etc.
    """
    data = {
        "data": elements_list
    }
    return unifier_post("/ds/data-elements", data=data)

