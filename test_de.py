from unifier_client import get_data_elements
import json

try:
    print("Fetching all data elements...")
    result = get_data_elements()
    print(f"Success! Found {len(result.get('data', []))} data elements.")
    
    print("\nFetching Decimal Amount data elements...")
    result_filter = get_data_elements(filter_options={"data_definition": "Decimal Amount"})
    print(f"Success! Found {len(result_filter.get('data', []))} Decimal Amount data elements.")
    if result_filter.get('data'):
        print(f"First element: {result_filter['data'][0].get('data_element')}")

except Exception as e:
    print(f"Error: {e}")
