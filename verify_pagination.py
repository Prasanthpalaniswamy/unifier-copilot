import sys
import os
import json
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from unifier_client import get_data_elements

def verify_pagination():
    try:
        print("--- TESTING PAGINATION: LIMIT 5, OFFSET 0 ---")
        res1 = get_data_elements(limit=5, offset=0)
        data1 = res1.get("data", [])
        print(f"Count: {len(data1)}")
        print(f"Pagination Info: {res1.get('pagination')}")
        
        if len(data1) > 0:
            print(f"First element: {data1[0].get('data_element')}")

        print("\n--- TESTING PAGINATION: LIMIT 5, OFFSET 1 ---")
        res2 = get_data_elements(limit=5, offset=1)
        data2 = res2.get("data", [])
        print(f"Count: {len(data2)}")
        print(f"Pagination Info: {res2.get('pagination')}")
        
        if len(data2) > 0:
            print(f"First element: {data2[0].get('data_element')}")

        print("\n--- RESULTS ---")
        if len(data1) == 5 and len(data2) == 5:
            if data1[0].get('data_element') != data2[0].get('data_element'):
                print("SUCCESS: Pagination (offset) is working!")
            else:
                print("ERROR: Offset 1 did not change the result set.")
        else:
            print(f"ERROR: Expected 5 items, got {len(data1)} and {len(data2)}")

    except Exception as e:
        print(f"Verification Failed: {e}")

if __name__ == "__main__":
    verify_pagination()
