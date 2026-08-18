import asyncio
import os
import time
import subprocess
from dotenv import load_dotenv
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

# Imports de nuestros módulos (usamos sus instrucciones para mantener consistencia)
from agents.watcher import get_watcher_agent
from agents.analyst import get_analyst_agent
from agents.advisor import get_advisor_agent
from agents.executor import get_executor_agent

from google import genai
from google.genai import types

# Simulación de la ejecución ADK usando llamadas manuales a la API para evitar deadlocks de Windows
async def run_pipeline():
    load_dotenv()
    client = genai.Client()
    
    print("> [1] Simulador omitido (ya ejecutó en background previamente)...")
    
    env = os.environ.copy()
    server_params = StdioServerParameters(command="mcp-grafana", args=[], env=env)
    
    print("\n> Conectando al túnel MCP de Grafana...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Helper para ejecutar llamadas a modelo con soporte manual de MCP tools
            async def ask_agent_with_mcp(agent_name, instruction, prompt_text):
                print(f"\n[Agente: {agent_name}] Analizando...")
                # Por simplicidad de la demo manual, inyectaremos el contexto crudo si el LLM no puede hacer el tool call directo,
                # pero intentaremos dejar que el LLM pida las tools.
                # Como el loop de tools manual es complejo, usaremos las tools que extrajimos antes para inyectar contexto
                # simulando lo que el runner ADK hace bajo el capó.
                
                # Para el Watcher, extraemos las métricas reales
                if agent_name == "Watcher":
                    res = await session.call_tool("query_prometheus", arguments={"expr": 'avg_over_time(premiere_manifest_latency_sum{region="latam-saopaulo"}[5m]) / avg_over_time(premiere_manifest_latency_count{region="latam-saopaulo"}[5m])', "datasourceUid": "grafanacloud-prom", "queryType": "instant"})
                    res2 = await session.call_tool("query_prometheus", arguments={"expr": 'increase(premiere_startup_failures_total{region="latam-saopaulo"}[5m])', "datasourceUid": "grafanacloud-prom", "queryType": "instant"})
                    lat = res.content[0].text if res.content else "No data"
                    fail = res2.content[0].text if res2.content else "No data"
                    prompt_text += f"\n\n[MCP Context Injected]\nLatencia (5m): {lat}\nFallos (5m): {fail}"
                
                # Para el Analyst, extraemos los logs reales
                if agent_name == "Analyst":
                    res = await session.call_tool("query_loki_logs", arguments={"logql": '{job="marquee-premiere"} |= "ManifestTimeoutError"', "datasourceUid": "grafanacloud-logs", "limit": 5})
                    logs = res.content[0].text if res.content else "No logs"
                    prompt_text += f"\n\n[MCP Context Injected]\nLogs de Loki: {logs}"

                response = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=prompt_text,
                    config=types.GenerateContentConfig(system_instruction=instruction)
                )
                
                # Para el Executor, usamos la respuesta para ejecutar la anotación real
                if agent_name == "Executor":
                    print("Ejecutando tool create_annotation vía MCP basado en la orden del Executor...")
                    try:
                        await session.call_tool("create_annotation", arguments={
                            "text": "DECISIÓN EJECUTIVA: Jugada 1 (Failover CDN). Justificación: " + response.text[:100] + "...",
                            "tags": ["incident", "marquee", "latam-saopaulo"]
                        })
                        print("✅ Anotación creada en Grafana exitosamente.")
                    except Exception as e:
                        print(f"Error creando anotación (ignorando para demo): {e}")

                print(response.text)
                return response.text

            watcher_agent = get_watcher_agent()
            analyst_agent = get_analyst_agent()
            advisor_agent = get_advisor_agent()
            executor_agent = get_executor_agent()

            print("\n> [2] Fase WATCHER (Monitoreo Técnico)")
            watcher_out = await ask_agent_with_mcp("Watcher", watcher_agent.instruction, "Analiza el estado actual de la región latam-saopaulo en Grafana.")

            print("\n> [3] Fase ANALYST (Impacto de Negocio y Causa Raíz)")
            analyst_out = await ask_agent_with_mcp("Analyst", analyst_agent.instruction, watcher_out)

            print("\n> [4] Fase ADVISOR (Propuesta de Jugadas)")
            advisor_out = await ask_agent_with_mcp("Advisor", advisor_agent.instruction, analyst_out)

            print("\n> [5] APROBACIÓN HUMANA SIMULADA")
            decision = "AUTORIZADO: Apruebo únicamente la JUGADA 1 (Conmutar CDN). No envíen notificaciones push a los usuarios."
            print(f"Ejecutivo dice: {decision}")

            print("\n> [6] Fase EXECUTOR (Acción y Auditoría)")
            executor_prompt = f"RECOMENDACIÓN DEL ADVISOR:\n{advisor_out}\n\nDECISIÓN DEL EJECUTIVO:\n{decision}\n\nProcede a anotar la decisión en el sistema usando MCP."
            executor_out = await ask_agent_with_mcp("Executor", executor_agent.instruction, executor_prompt)

    print("\n> Pipeline completado.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())
