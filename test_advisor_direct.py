import os
import yaml
from dotenv import load_dotenv
from google import genai
from google.genai import types

def run_advisor():
    load_dotenv()
    
    # Cargar Playbook
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "playbooks", "remediation_playbook.md")
    with open(config_path, "r", encoding="utf-8") as f:
        playbook_md = f.read()

    # Iniciar cliente Gemini
    client = genai.Client()
    
    # Prompt del sistema (Instrucción)
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

    analyst_report = """
**Resumen de Negocio y Causa Raíz**

*   **IMPACTO DE NEGOCIO:** Caída en nuestro mercado #2 (Latin America - São Paulo), arriesgando $40,000 por minuto. La naturaleza de este mercado como "emergente de mayor crecimiento" implica un riesgo adicional de pérdida de usuarios a largo plazo.

*   **CAUSA RAÍZ (LOGS/TRAZAS):** Los logs de la infraestructura confirman un error crítico y recurrente de `ManifestTimeoutError` proveniente de la CDN que sirve a la región `latam-saopaulo`. Esto indica que la red de distribución de contenido no está entregando el manifiesto de video a tiempo, causando que la reproducción falle para un alto volumen de usuarios antes de que pueda comenzar.

*   **URGENCIA:** Alta.
"""

    print("Ejecutando Advisor con el reporte de Analyst...")
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=analyst_report,
        config=types.GenerateContentConfig(
            system_instruction=instruction,
        )
    )
    
    print("\n" + "="*50)
    print(response.text)
    print("="*50 + "\n")

if __name__ == "__main__":
    run_advisor()
