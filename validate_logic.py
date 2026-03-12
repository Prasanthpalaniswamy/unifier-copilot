from unifier_client import create_data_elements
import json

def mock_unifier_post(endpoint, data):
    print(f"POST to {endpoint} with data:")
    print(json.dumps(data, indent=2))
    return {"status": 200, "message": "Success (Mock)"}

# Temporarily override unifier_client.unifier_post for testing
import unifier_client
unifier_client.unifier_post = mock_unifier_post

def create_data_element_logic(
    data_element: str,
    data_definition: str,
    form_label: str,
    decimal_format: str = "2"
):
    element_data = {
        "data_element": data_element,
        "data_definition": data_definition,
        "form_label": form_label
    }
    
    if data_definition == "Decimal Amount":
        element_data["decimal_format"] = decimal_format

    return create_data_elements([element_data])

print("--- Test 1: No decimal_format mentioned ---")
create_data_element_logic("test_de_default", "Decimal Amount", "Default Test")

print("\n--- Test 2: User mentions decimal_format='5' ---")
create_data_element_logic("test_de_explicit", "Decimal Amount", "Explicit Test", decimal_format="5")
