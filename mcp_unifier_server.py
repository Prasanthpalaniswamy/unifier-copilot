import os
import sys
import builtins
from fastmcp import FastMCP
from unifier_client import get_projects, get_data_elements, get_data_definitions, create_data_elements, get_users, get_bp_records
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from datetime import datetime
load_dotenv()
# Save the original print and stdout
_original_stdout = sys.stdout
_original_print = builtins.print
# Override print to always go to stderr
def silent_print(*args, **kwargs):
    kwargs['file'] = sys.stderr
    _original_print(*args, **kwargs)
builtins.print = silent_print
sys.stdout = sys.stderr
mcp = FastMCP("unifier-gemini")
@mcp.tool()
def list_projects(shell_type: str = "Projects", limit: int = 50, offset: int = 0):
    """Return list of projects from Unifier"""
    return get_projects(shell_type=shell_type, limit=limit, offset=offset)
@mcp.tool()
def list_data_elements(
    data_element: str = None,
    data_definition: str = None,
    form_label: str = None,
    description: str = None,
    tooltip: str = None,
    limit: int = 50,
    offset: int = 0
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
    return get_data_elements(filter_options=filter_options if filter_options else None, limit=limit, offset=offset)
@mcp.tool()
def list_data_definitions(
    df_type: str = None,
    name: str = None,
    data_source: str = None,
    limit: int = 50,
    offset: int = 0
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
    return get_data_definitions(df_type=df_type, filter_options=filter_options if filter_options else None, limit=limit, offset=offset)
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
    
    if data_definition == "Decimal Amount":
        element_data["decimal_format"] = decimal_format
    elif data_definition in ["Image Picker", "SYS Rich Text"]:
        if height: element_data["height"] = height
    elif data_definition == "textarea":
        if no_of_lines: element_data["no_of_lines"] = no_of_lines
    elif data_definition == "SYS Numeric Query Based":
        element_data["hide_currency_symbol"] = hide_currency_symbol
    return create_data_elements([element_data])
@mcp.tool()
def bulk_create_data_elements_from_excel(file_path: str) -> str:
    """
    Read data elements from an Excel file and create them in Unifier in bulk.
    Generates an 'api_response.xlsx' report in the same directory as the input file.
    
    file_path: Absolute path to the Excel file containing the 'DataElementCR_Inp' sheet.
    """
    try:
        df = pd.read_excel(file_path, sheet_name='DataElementCR_Inp', dtype=str)
        # Replace NaN with empty strings (equivalent to the legacy script's np.nan replacement)
        df = df.fillna('')
        data_records = df.to_dict(orient='records')   
        if not data_records:
            return "No data found in sheet 'DataElementCR_Inp'."

        # Call existing API client
        result = create_data_elements(data_records)
        
        # Parse response for report generation
        messages = result.get("message", [])
        if not messages:
            return "API call succeeded but no detail messages returned to export."

        records = [
            {
                "Data_Element_Name": msg.get("data_element", ""),
                "Integration_Message": msg.get("message", ""),
                "status_code": msg.get("status", "")
            }
            for msg in messages
        ]
        out_df = pd.DataFrame(records)
        input_dir = os.path.dirname(file_path)
        output_file = os.path.normpath(os.path.join(input_dir, "api_response.xlsx"))
        
        try:
            # Check if file is locked
            with open(output_file, "a"):
                pass
            out_df.to_excel(output_file, index=False)
            report_msg = f"Excel report saved successfully to: {output_file}"
        except PermissionError:
            fallback_name = f"api_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            fallback = os.path.normpath(os.path.join(input_dir, fallback_name))
            out_df.to_excel(fallback, index=False)
            report_msg = f"Target file was locked. Saved fallback report to: {fallback}"
        return f"Bulk creation executed. Processed {len(data_records)} records. {report_msg}"
    except Exception as e:
        return f"Error executing bulk creation: {str(e)}"
@mcp.tool()
def list_users(
    filter_condition: str = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Return list of users from Unifier. 
    This uses the POST /admin/user/get endpoint.
    filter_condition: Criteria to filter users (e.g., 'uuu_user_status=1' for active users).
    """
    return get_users(filter_condition=filter_condition, limit=limit, offset=offset)
@mcp.tool()
def list_bp_records(
    bpname: str,
    project_number: str = None,
    record_fields: str = None,
    filter_condition: str = None,
    filter_criteria: str = None,
    fetch_lineitems: bool = False,
    limit: int = 50,
    offset: int = 0
):
    """
    Fetch a list of Business Process (BP) records from a specific project or company level.
    bpname: The name of the BP (e.g., 'Vendors').
    project_number: The project number. If empty, fetches company level BP records.
    record_fields: Semicolon separated list of data element names to return.
    filter_condition: Simple string filter (e.g., 'status=Active').
    filter_criteria: Advanced JSON string for filtering.
    fetch_lineitems: True to return line item details, False defaults to 'no'.
    """
    options = {}
    options["lineitem"] = "yes" if fetch_lineitems else "no"
    
    if record_fields:
        options["record_fields"] = record_fields
    if filter_condition:
        options["filter_condition"] = filter_condition
    if filter_criteria:
        import json
        try:
            options["filter_criteria"] = json.loads(filter_criteria)
        except json.JSONDecodeError:
            options["filter_criteria"] = filter_criteria # Pass as string if parsed fails, let API decide
    return get_bp_records(bpname=bpname, project_number=project_number, options=options, limit=limit, offset=offset)
# if __name__ == "__main__":
#     # Restore the original stdout for the MCP protocol just before running
#     sys.stdout = _original_stdout
#     mcp.run(transport='stdio')
# if __name__ == "__main__":
#     port = os.environ.get("PORT")
#     if port:
#         print(f"Running in HTTP mode on port {port}", file=sys.stderr)
#         mcp.run(transport="http", host="0.0.0.0", port=int(port))
#     else:
#         print("Running in STDIO mode (local development)", file=sys.stderr)
#         # Restore stdout only for MCP stdio transport
#         sys.stdout = _original_stdout
#         mcp.run(transport="stdio")

if __name__ == "__main__":
    print("Running in STDIO mode", file=sys.stderr)
    sys.stdout = _original_stdout
    mcp.run(transport="stdio")