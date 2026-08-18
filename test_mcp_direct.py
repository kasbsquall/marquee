import asyncio
import os
import json
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

from dotenv import load_dotenv

async def run():
    load_dotenv()
    env = os.environ.copy()
    server_params = StdioServerParameters(command="mcp-grafana", args=[], env=env)
    
    print("Conectando al MCP de Grafana...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Conectado.\n")
            
            print("Listando métricas disponibles en Grafana...")
            res_metrics = await session.call_tool("list_prometheus_metric_names", arguments={"datasourceUid": "grafanacloud-prom"})
            if res_metrics and res_metrics.content:
                metrics_text = res_metrics.content[0].text
                print(metrics_text[:500] + "...\n")
                
            queries = {
                "Manifest Latency (São Paulo)": 'avg_over_time(premiere_manifest_latency_sum{region="latam-saopaulo"}[5m]) / avg_over_time(premiere_manifest_latency_count{region="latam-saopaulo"}[5m])',
                "Startup Failures (São Paulo)": 'increase(premiere_startup_failures_total{region="latam-saopaulo"}[5m])',
                "Active Viewers (São Paulo)": 'premiere_active_viewers{region="latam-saopaulo"}'
            }
            
            for name, query in queries.items():
                print(f"--- Consultando: {name} ---")
                print(f"PromQL: {query}")
                try:
                    res = await session.call_tool("query_prometheus", arguments={"expr": query, "datasourceUid": "grafanacloud-prom", "endTime": "now", "queryType": "instant"})
                    
                    if res and res.content:
                        for content in res.content:
                            if hasattr(content, 'text'):
                                # Tratar de formatear el JSON para que sea legible
                                try:
                                    data = json.loads(content.text)
                                    print(json.dumps(data, indent=2))
                                except:
                                    print(content.text)
                    else:
                        print("Sin datos.")
                except Exception as e:
                    print(f"Error en query: {e}")
                print("\n")

if __name__ == "__main__":
    asyncio.run(run())
