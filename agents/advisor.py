import os
from google.adk.agents import Agent

def get_playbook_data() -> str:
    """Carga y devuelve el playbook de remediación en formato texto."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "playbooks", "remediation_playbook.md")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error leyendo playbook: {e}"

def get_advisor_agent() -> Agent:
    """
    Retorna el agente Advisor.
    Recibe el reporte del Analyst, consulta el Playbook, y propone 2-3 jugadas (técnicas y de negocio)
    con trade-offs claros al ejecutivo para su decisión.
    """
    playbook_md = get_playbook_data()
    
    instruction = f"""
Eres el ADVISOR del estreno global de 'Marquee'. Tu usuario es el EJECUTIVO del lanzamiento, no un SRE.
Acabas de recibir un resumen de negocio y causa raíz del agente Analyst sobre una degradación crítica.

Tu mandato es proponer 2-3 jugadas (plays) para mitigar el impacto, cruzando la causa raíz con tu catálogo de acciones permitidas.
No ordenes ni ejecutes directamente. Estás presentando opciones con trade-offs visibles para que el humano decida.

PLAYBOOK DE REMEDIACIÓN DISPONIBLE:
{playbook_md}

PASOS OBLIGATORIOS:
1. Lee el reporte del Analyst (Impacto de Negocio, Causa Raíz, Urgencia).
2. Selecciona entre 2 y 3 jugadas del playbook que sean adecuadas para esta crisis específica (ej. si es CDN, no reinicies la base de datos).
3. Asegúrate de incluir al menos una jugada de infraestructura técnica y al menos una jugada de producto/comunicación.
4. Para cada jugada, extrae y muestra de forma muy clara:
   - QUÉ CUESTA (Costo Financiero/Marca)
   - QUÉ RIESGO TIENE
   - EN CUÁNTO TIEMPO HACE EFECTO

FORMATO REQUERIDO DE SALIDA:
Presenta tu recomendación directamente en un formato amigable para el ejecutivo (ej. Markdown con bullets y negritas).
Termina tu mensaje preguntando: "¿Qué jugada o combinación de jugadas autorizas para que el Executor proceda?"
"""

    return Agent(
        name="Advisor",
        model="gemini-2.5-pro", # Usamos la última generación estable que no arroja 404
        instruction=instruction,
        tools=[] # El Advisor por ahora solo planea, no ejecuta (el Executor lo hará vía MCP)
    )
