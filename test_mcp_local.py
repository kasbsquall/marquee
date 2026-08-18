import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def main():
    token = os.getenv("GRAFANA_SERVICE_ACCOUNT_TOKEN")
    grafana_url = os.getenv("GRAFANA_URL")

    try:
        from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
        from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
        from mcp.client.stdio import StdioServerParameters
    except ImportError as e:
        print(f"Failed to import ADK: {e}")
        return

    print("Testing Local Stdio MCP endpoint...")
    try:
        env = os.environ.copy()
        env["GRAFANA_URL"] = grafana_url
        env["GRAFANA_SERVICE_ACCOUNT_TOKEN"] = token
        
        toolset = McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="mcp-grafana",
                    args=[],
                    env=env
                )
            ),
        )
        print("McpToolset initialized")
        if hasattr(toolset, 'get_tools'):
            tools = await toolset.get_tools() if asyncio.iscoroutinefunction(toolset.get_tools) else toolset.get_tools()
            print(f"Success! Local Stdio MCP found {len(tools)} tools.")
            if tools:
                print(f"First 5 tools: {[t.name for t in tools[:5]]}")
        return
    except Exception as e:
        print(f"Local MCP failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
