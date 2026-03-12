import unifier_client
import os
print(f"Module file: {unifier_client.__file__}")
print(f"Current working directory: {os.getcwd()}")

import json
try:
    print("\nCalling get_data_elements...")
    res = unifier_client.get_data_elements(filter_options={"data_definition": "Decimal Amount"})
    print(f"Status: {res.get('status')}")
    # We want to see the ACTUAL URL requested if possible, but requests doesn't show it easily without a hook.
    # Let's check the code object
    import inspect
    print(f"Source of get_data_elements:\n{inspect.getsource(unifier_client.get_data_elements)}")
except Exception as e:
    print(f"Error: {e}")
