import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from unifier_client import unifier_get

def test_pagination():
    try:
        print("--- TESTING WITHOUT LIMIT ---")
        res_all = unifier_get("/ds/data-elements")
        all_count = len(res_all.get("data", []))
        print(f"Total elements: {all_count}")

        print("\n--- TESTING WITH LIMIT: 5 ---")
        options = {"limit": 5}
        params = {"options": json.dumps(options)}
        res_lim = unifier_get("/ds/data-elements", params=params)
        lim_count = len(res_lim.get("data", []))
        print(f"Elements returned: {lim_count}")
        
        if lim_count == 5:
            print("\nRESULT: API supports 'limit' in options!")
        else:
            print(f"\nRESULT: API ignored limit. Returned {lim_count} instead of 5.")

        print("\n--- TESTING WITH FILTER FOR SPECIFIC ELEMENT ---")
        # Trying a standard filter to verify what works
        filter_opts = {"data_element": "PP_test001"}
        params_f = {"filter": json.dumps(filter_opts)}
        res_f = unifier_get("/ds/data-elements", params=params_f)
        print(f"Filter result count: {len(res_f.get('data', []))}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_pagination()
