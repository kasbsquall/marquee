import os
import base64
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# Para logs
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

def setup_telemetry():
    """
    Configura y devuelve el tracer, meter y logger usando OTLP sobre HTTP.
    Usa el gateway OTLP de Grafana Cloud configurado en las variables de entorno.
    """
    endpoint = os.getenv("OTLP_ENDPOINT")
    if not endpoint:
        raise ValueError("OTLP_ENDPOINT no está configurado en el entorno.")
        
    username = os.getenv("OTLP_INSTANCE_ID") or os.getenv("OTLP_USERNAME")
    password = os.getenv("GRAFANA_WRITE_TOKEN") or os.getenv("OTLP_PASSWORD")
    
    if not username or not password:
        raise ValueError("Credenciales OTLP incompletas en el entorno.")

    # Grafana Cloud OTLP usa basic auth
    auth_str = f"{username}:{password}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}"
    }

    resource = Resource.create({
        SERVICE_NAME: "marquee-premiere",
        "service.version": "1.0.0",
        "deployment.environment": "production"
    })

    # --- TRACES ---
    tracer_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces", headers=headers)
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(tracer_provider)
    tracer = trace.get_tracer("marquee.tracer")

    # --- METRICS ---
    metric_exporter = OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics", headers=headers)
    # Enviamos métricas cada 5 segundos para que la demo sea ágil
    reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)
    meter = metrics.get_meter("marquee.meter")

    # --- LOGS ---
    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint=f"{endpoint}/v1/logs", headers=headers)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)

    # Conectar logging estándar de Python a OpenTelemetry
    logger = logging.getLogger("marquee")
    logger.setLevel(logging.INFO)
    # Evitar duplicados si se llama varias veces
    if not logger.handlers:
        handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
        logger.addHandler(handler)

    return tracer, meter, logger
