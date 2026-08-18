import os
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp.client.stdio import StdioServerParameters

def get_grafana_mcp_toolset() -> McpToolset:
    """
    Crea y retorna el Toolset MCP para conectar los agentes con Grafana Cloud.
    Utiliza el servidor local `mcp-grafana` y le pasa las credenciales de Service Account.
    """
    grafana_url = os.getenv("GRAFANA_URL")
    token = os.getenv("GRAFANA_SERVICE_ACCOUNT_TOKEN")
    
    if not grafana_url or not token:
        raise ValueError("Faltan variables GRAFANA_URL o GRAFANA_SERVICE_ACCOUNT_TOKEN en el entorno.")
        
    env = os.environ.copy()
    env["GRAFANA_URL"] = grafana_url
    env["GRAFANA_SERVICE_ACCOUNT_TOKEN"] = token

    return McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="mcp-grafana",
                args=[],
                env=env
            )
        )
    )
