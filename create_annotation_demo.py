import asyncio
import os
import json
from dotenv import load_dotenv
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def run():
    load_dotenv()
    env = os.environ.copy()
    server_params = StdioServerParameters(command="mcp-grafana", args=[], env=env)
    
    print("Conectando al MCP de Grafana...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Conectado.\n")
            
            # Simulamos el payload que el Executor generaría tras la aprobación
            decision_text = (
                "EJECUCIÓN DE REMEDIACIÓN APROBADA\n"
                "- Ejecutado por: Ejecutivo del Estreno\n"
                "- Jugada Elegida: Jugada 1 (Conmutar a CDN de Respaldo)\n"
                "- Justificación Analyst: Logs confirmaron ManifestTimeoutError continuo en la CDN primaria de São Paulo, "
                "arriesgando mercado #2."
            )
            
            print("--- Creando Anotación en Grafana ---")
            print(decision_text)
            
            try:
                # El dashboardUid lo podríamos sacar buscando dashboards, pero podemos crear una anotación general (sin dashboardUid) 
                # o taggeada si mcp-grafana lo permite.
                res = await session.call_tool("create_annotation", arguments={
                    "text": decision_text,
                    "tags": ["marquee-premiere", "incident", "latam-saopaulo", "resolved"]
                })
                
                if res and res.content:
                    for content in res.content:
                        if hasattr(content, 'text'):
                            print("\n[Respuesta MCP]:")
                            print(content.text)
                else:
                    print("Anotación creada (sin respuesta).")
            except Exception as e:
                print(f"Error creando anotación: {e}")

if __name__ == "__main__":
    asyncio.run(run())
