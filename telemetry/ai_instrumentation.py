import functools
from opentelemetry import trace

# Obtener el tracer configurado en otel_exporter.py
tracer = trace.get_tracer("marquee.ai_tracer")

def trace_gemini_call(agent_name: str):
    """
    Decorador asíncrono para envolver llamadas al modelo Gemini (google.genai).
    Inyecta métricas gen_ai.* compatibles con Grafana AI Observability.
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(agent, instruction, prompt_text, *args, **kwargs):
            # El nombre de la operación suele ser chat.completions para IA generativa
            with tracer.start_as_current_span(f"chat.completions {agent_name}") as span:
                # Atributos obligatorios para Grafana AI Observability
                span.set_attribute("gen_ai.system", "gemini")
                span.set_attribute("gen_ai.request.model", "gemini-2.5-pro")
                span.set_attribute("gen_ai.operation.name", "chat")
                span.set_attribute("agent.name", agent_name)
                
                # Opcional pero espectacular para demos: registrar el prompt
                # (En producción esto puede omitirse por PII, pero en hackathon suma puntos)
                span.set_attribute("gen_ai.prompt", f"INSTRUCTION:\n{instruction}\n\nPROMPT:\n{prompt_text}")
                
                try:
                    # Ejecutar la llamada real al LLM (esperamos que devuelva la respuesta cruda de client.models.generate_content)
                    response = await func(agent, instruction, prompt_text, *args, **kwargs)
                    
                    # Registrar tokens y respuesta si la llamada fue exitosa
                    if response and hasattr(response, "text"):
                        span.set_attribute("gen_ai.completion", response.text)
                        
                    if response and hasattr(response, "usage_metadata"):
                        usage = response.usage_metadata
                        if usage:
                            if hasattr(usage, "prompt_token_count"):
                                span.set_attribute("gen_ai.usage.input_tokens", usage.prompt_token_count)
                            if hasattr(usage, "candidates_token_count"):
                                span.set_attribute("gen_ai.usage.output_tokens", usage.candidates_token_count)
                    
                    return response
                except Exception as e:
                    span.record_exception(e)
                    span.set_attribute("error", True)
                    raise
        return wrapper
    return decorator
