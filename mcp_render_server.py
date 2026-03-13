import os
from mcp_unifier_server import mcp

port = int(os.environ.get("PORT", 10000))

print(f"Starting MCP HTTP server on port {port}")

mcp.run(
    transport="http",
    host="0.0.0.0",
    port=port
)