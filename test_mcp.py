import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    token = os.getenv("GRAFANA_SERVICE_ACCOUNT_TOKEN")
    grafana_url = os.getenv("GRAFANA_URL")

    try:
        from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
        from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
    except ImportError as e:
        print(f"Failed to import ADK: {e}")
        return

    print("Testing Hosted MCP endpoint...")
    try:
        toolset = McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://mcp.grafana.com/mcp",
                headers={
                    "X-Grafana-URL": grafana_url,
                    "Authorization": f"Bearer {token}",
                },
            ),
        )
        print("McpToolset initialized")
        print("Toolset dict:", dir(toolset))
        if hasattr(toolset, 'get_tools'):
            tools = await toolset.get_tools() if asyncio.iscoroutinefunction(toolset.get_tools) else toolset.get_tools()
            print(f"Success! Hosted MCP found {len(tools)} tools.")
        elif hasattr(toolset, 'tools'):
            tools = toolset.tools
            if callable(tools):
                tools = tools()
            print(f"Success! Hosted MCP found {len(tools)} tools.")
        return
    except Exception as e:
        print(f"Hosted MCP failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
