import sys
import os
import json
from pathlib import Path

# Add the project directory to sys.path
project_dir = r"C:\devworks\PythonDEV\AI_Initiatives\unifier-copilot"
sys.path.append(project_dir)

from unifier_client import get_projects, get_data_elements, get_data_definitions

def main():
    results = {}
    
    # 1. Get Top 5 Projects
    try:
        projects_res = get_projects("Projects")
        if isinstance(projects_res, dict) and "data" in projects_res:
            results["projects"] = projects_res["data"][:5]
        else:
            results["projects_error"] = f"Unexpected response format: {type(projects_res)}"
    except Exception as e:
        results["projects_error"] = str(e)
        
    # 2. Get Stats for Functionalities
    try:
        de_res = get_data_elements()
        dd_res = get_data_definitions()
        
        results["functionalities"] = {
            "projects": "Supported (list_projects)",
            "data_elements": f"Supported (list_data_elements) - Count: {len(de_res.get('data', [])) if isinstance(de_res, dict) else 'Unknown'}",
            "data_definitions": f"Supported (list_data_definitions) - Count: {len(dd_res.get('data', [])) if isinstance(dd_res, dict) else 'Unknown'}",
            "creation": "Supported (create_data_element)"
        }
    except Exception as e:
        results["functionalities_error"] = str(e)
        
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
