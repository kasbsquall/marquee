import asyncio
import os
import sys

# Asegurar que el path incluye la raíz para poder importar agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part
from agents.watcher import get_watcher_agent

async def main():
    print("Inicializando agente Watcher...")
    agent = get_watcher_agent()
    runner = InMemoryRunner(agent)
    
    content = Content(role="user", parts=[Part.from_text(text="Verifica el estado actual del estreno en Grafana, revisando las métricas de los últimos 5 minutos.")])
        
    print("\n[Iniciando consulta al MCP de Grafana vía Watcher...]")
    print("-" * 50)
    
    try:
        if hasattr(runner, 'session_service'):
            await runner.session_service.create_session(app_name=runner.app_name, user_id="demo_user", session_id="demo_session")
        
        generator = runner.run(user_id="demo_user", session_id="demo_session", new_message=content)
        if hasattr(generator, "__aiter__"):
            async for event in generator:
                if hasattr(event, "text") and event.text:
                    print(event.text, end="", flush=True)
                elif hasattr(event, "tool_calls") and event.tool_calls:
                    for tc in event.tool_calls:
                        print(f"\n[Tool Call] {getattr(tc, 'name', tc)}: {getattr(tc, 'args', getattr(tc, 'arguments', ''))}")
        else:
            for event in generator:
                if hasattr(event, "text") and event.text:
                    print(event.text, end="", flush=True)
                elif hasattr(event, "tool_calls") and event.tool_calls:
                    for tc in event.tool_calls:
                        print(f"\n[Tool Call] {getattr(tc, 'name', tc)}: {getattr(tc, 'args', getattr(tc, 'arguments', ''))}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nError durante la ejecución del runner: {e}")
        
    print("\n" + "-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
