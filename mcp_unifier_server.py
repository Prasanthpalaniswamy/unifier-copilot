from fastmcp import FastMCP
from unifier_client import get_projects, get_data_elements, get_data_definitions, create_data_elements
import os
from dotenv import load_dotenv
from pathlib import Path
import os


# DATABASE_URL = os.environ.get("DATABASE_URL")
# BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)
# load_dotenv(BASE_DIR / ".env")
 
# UNIFIER_USERNAME = os.environ.get("UNIFIER_USERNAME")
# UNIFIER_PASSWORD = os.environ.get("UNIFIER_PASSWORD")


# BASE_DIR = Path(__file__).resolve().parent
# # .parent
# print(BASE_DIR)
# load_dotenv(BASE_DIR / ".env")    
# UNIFIER_USERNAME = os.environ.get("UNIFIER_USERNAME")
# UNIFIER_PASSWORD = os.environ.get("UNIFIER_PASSWORD")


# os.environ["UNIFIER_USERNAME"] = "intuser"
# os.environ["UNIFIER_PASSWORD"] = "intuser@123"
# print("Environment Variables after setting:")
# print("UNIFIER_USERNAME:", os.getenv("UNIFIER_USERNAME"))
# print("UNIFIER_PASSWORD:", os.getenv("UNIFIER_PASSWORD"))

# print("Environment Variables:")
# print("UNIFIER_USERNAME:", os.getenv("UNIFIER_USERNAME"))
# print("UNIFIER_PASSWORD:", os.getenv("UNIFIER_PASSWORD"))

# , get_project_cost, get_rfis

# print("Getting Projects")
mcp = FastMCP("unifier-gemini")


@mcp.tool()
def list_projects(shell_type: str = "Projects"):
    """Return list of projects from Unifier"""
    print("Environment Variables in list_projects:")

    return get_projects(shell_type=shell_type)


@mcp.tool()
def list_data_elements(
    data_element: str = None,
    data_definition: str = None,
    form_label: str = None,
    description: str = None,
    tooltip: str = None
):
    """
    Return list of custom data elements from Unifier. 
    Filters (case-insensitive) can be applied for data_element name, definition, label, description, or tooltip.
    """
    filter_options = {}
    if data_element: filter_options["data_element"] = data_element
    if data_definition: filter_options["data_definition"] = data_definition
    if form_label: filter_options["form_label"] = form_label
    if description: filter_options["description"] = description
    if tooltip: filter_options["tooltip"] = tooltip

    return get_data_elements(filter_options=filter_options if filter_options else None)


@mcp.tool()
def list_data_definitions(
    df_type: str = None,
    name: str = None,
    data_source: str = None
):
    """
    Return list of data definitions from Unifier.
    df_type: Possible values are Basic, Cost Codes, Data Picker (case-insensitive).
    name: Name of the Data definition.
    data_source: Data source of the data picker (only for Data Picker type).
    """
    filter_options = {}
    if name: filter_options["name"] = name
    if data_source: filter_options["data_source"] = data_source

    return get_data_definitions(df_type=df_type, filter_options=filter_options if filter_options else None)


@mcp.tool()
def create_data_element(
    data_element: str,
    data_definition: str,
    form_label: str,
    description: str = None,
    tooltip: str = None,
    decimal_format: str = "2",
    height: str = None,
    no_of_lines: str = None,
    hide_currency_symbol: str = "No"
):
    """
    Create a new custom data element in Unifier.
    data_element: Unique name (e.g., 'sampleDE').
    data_definition: Field definition to use (e.g., 'Decimal Amount').
    form_label: Label name.
    decimal_format: For 'Decimal Amount' (default '2').
    height: For 'Image Picker' or 'SYS Rich Text'.
    no_of_lines: For 'textarea'.
    hide_currency_symbol: For 'SYS Numeric Query Based' (Yes/No).
    """
    element_data = {
        "data_element": data_element,
        "data_definition": data_definition,
        "form_label": form_label
    }
    if description: element_data["description"] = description
    if tooltip: element_data["tooltip"] = tooltip
    
    # Conditional fields based on data_definition
    if data_definition == "Decimal Amount":
        element_data["decimal_format"] = decimal_format
    elif data_definition in ["Image Picker", "SYS Rich Text"]:
        if height: element_data["height"] = height
    elif data_definition == "textarea":
        if no_of_lines: element_data["no_of_lines"] = no_of_lines
    elif data_definition == "SYS Numeric Query Based":
        element_data["hide_currency_symbol"] = hide_currency_symbol

    return create_data_elements([element_data])



if __name__ == "__main__":
    mcp.run()



    # @mcp.tool()
# def project_cost(project_id: str):
#     """Return cost information for a project"""
#     return get_project_cost(project_id)


# @mcp.tool()
# def project_rfis(project_id: str):
#     """Return open RFIs for a project"""
#     return get_rfis(project_id)