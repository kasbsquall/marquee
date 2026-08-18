import asyncio
from dotenv import load_dotenv
from google import genai
from google.genai import types

from telemetry.otel_exporter import setup_telemetry
from telemetry.ai_instrumentation import trace_gemini_call

async def main():
    load_dotenv()
    
    # Inicializar exportadores de OpenTelemetry (para enviar traces a Grafana)
    tracer, meter, logger = setup_telemetry()
    client = genai.Client()
    
    print("Enviando un prompt a Gemini envuelto en AI Observability...")
    
    # Usar el wrapper creado
    @trace_gemini_call("DemoAgent")
    async def _call_llm(agent, instr, p_text):
        return await client.aio.models.generate_content(
            model="gemini-2.5-pro",
            contents=p_text,
            config=types.GenerateContentConfig(system_instruction=instr)
        )
    
    res = await _call_llm("DemoAgent", "Eres un agente de prueba", "Responde 'AI Observability en línea'")
    print(f"Respuesta: {res.text}")
    
    print("Esperando 5s para que los spans se envíen a Grafana OTLP...")
    await asyncio.sleep(5)
    print("Hecho.")

if __name__ == "__main__":
    asyncio.run(main())
