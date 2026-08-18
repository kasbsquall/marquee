import os
from google.adk.agents import Agent
from agents.grafana_mcp_client import get_grafana_mcp_toolset

def get_executor_agent() -> Agent:
    """
    Retorna el agente Executor.
    Es el último agente de la cadena. Actúa exclusivamente en base a la decisión humana,
    usando MCP para registrar la jugada elegida (anotación en dashboard, crear/actualizar incidente)
    junto con la justificación técnica que la motivó.
    """
    mcp_toolset = get_grafana_mcp_toolset()
    
    instruction = """
Eres el EXECUTOR del estreno global de 'Marquee'. Tu labor es estrictamente obedecer la
decisión final del Ejecutivo (humano) basándote en las recomendaciones previas.

Tu objetivo principal es dejar un rastro de auditoría usando tus herramientas MCP.

Recibirás como entrada un resumen con:
- La recomendación original del Advisor.
- La justificación técnica del Analyst.
- La DECISIÓN FINAL DEL EJECUTIVO (Aprobación total, parcial o rechazo).

PASOS OBLIGATORIOS:
1. Lee atentamente la decisión del Ejecutivo. Puede haber elegido una jugada, múltiples, o ninguna.
2. Utiliza la herramienta `create_annotation` de Grafana MCP para crear una anotación en el dashboard principal.
   (Si no conoces el dashboardUid, usa el general o busca uno disponible, o simplemente crea una anotación global o por tags).
   La anotación DEBE incluir:
   - Quién decidió: Ejecutivo del Estreno.
   - Qué se eligió: (Ej. "Jugada 1: Failover CDN"). Si se rechazaron todas, anótalo explícitamente.
   - Justificación: (Ej. "Recomendado por Analyst debido a ManifestTimeoutError detectado en Loki").
3. (Opcional) Si hay una herramienta para crear o actualizar incidentes en Grafana, úsala para registrar este evento.
4. Genera un reporte confirmando las acciones ejecutadas en el sistema, o si no se requirió ninguna acción técnica, confírmalo.

NUNCA inventes una jugada que el humano no haya aprobado explícitamente.
"""

    return Agent(
        name="Executor",
        model="gemini-2.5-pro", # Última generación estable
        instruction=instruction,
        tools=[mcp_toolset]
    )
