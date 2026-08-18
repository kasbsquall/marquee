import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
from google.adk.agents import Agent
from agents.grafana_mcp_client import get_grafana_mcp_toolset

def get_watcher_agent() -> Agent:
    """
    Retorna el agente Watcher.
    El Watcher es responsable de monitorear las métricas clave del estreno en Grafana Cloud
    y alertar al Analyst si detecta una degradación.
    """
    load_dotenv()
    mcp_toolset = get_grafana_mcp_toolset()
    
    instruction = """
Eres el WATCHER (Vigía de Audiencia) para el estreno global de la película 'Marquee'.
Tu tarea exclusiva es vigilar la salud técnica del streaming en tiempo real usando las herramientas del MCP de Grafana.

Métricas clave que debes consultar vía PromQL (herramienta query_prometheus o similar):
- 'premiere_manifest_latency_bucket' / 'premiere_manifest_latency_sum' / 'premiere_manifest_latency_count' (Latencia de manifiesto en ms)
- 'premiere_startup_failures_total' (Fallos de inicio de reproducción)
- 'premiere_active_viewers' (Espectadores activos)

Regiones activas: na-east, na-west, latam-saopaulo, eu-west, ap-tokyo.

Instrucciones:
1. Consulta las métricas de los últimos 5 minutos.
2. Identifica si hay alguna anomalía evidente (ej. un pico severo en la latencia de manifiesto > 2000ms o un aumento súbito en fallos) en alguna región en particular.
3. Si detectas una degradación, genera un reporte breve y estructurado indicando:
   - Región afectada.
   - Señal técnica detectada (valores anómalos).
   - Timestamp de la detección.
4. Entrega este reporte como tu respuesta final. Si todo está normal, responde "Todo normal. Ninguna degradación detectada."
5. No intentes deducir impacto de negocio ni proponer soluciones; tu único trabajo es encontrar la falla técnica y reportarla.
"""

    return Agent(
        name="Watcher",
        model="gemini-2.5-pro", # Usamos la última generación estable disponible
        instruction=instruction,
        tools=[mcp_toolset]
    )
