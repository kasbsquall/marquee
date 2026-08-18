import os
import time
import random
from dotenv import load_dotenv
from opentelemetry import trace

# Asegurar que el path incluye la raíz para poder importar telemetry
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telemetry.otel_exporter import setup_telemetry
from telemetry.incident_script import SCRIPT_STEPS

# Regiones y su peso relativo de audiencia
REGIONS = {
    "na-east": 1.2,
    "na-west": 1.0,
    "latam-saopaulo": 0.8,
    "eu-west": 1.1,
    "ap-tokyo": 0.9,
    "eu-central": 1.0,
    "ap-seoul": 0.7,
    "latam-mexico": 0.5
}

def run_simulation(tick_interval=5):
    """
    Ejecuta el simulador del estreno leyendo el guion paso a paso.
    tick_interval controla la velocidad de la demo (5 segundos por defecto).
    """
    load_dotenv()
    
    try:
        tracer, meter, logger = setup_telemetry()
    except ValueError as e:
        print(f"Error de configuración: {e}")
        print("Asegúrate de que el .env tiene OTLP_ENDPOINT, OTLP_INSTANCE_ID y GRAFANA_WRITE_TOKEN")
        return

    # Definición de métricas
    # Usamos gauge para valores absolutos que suben y bajan, counter para conteos incrementales, histogram para latencia
    playback_quality = meter.create_gauge("premiere.playback.quality", description="Quality of playback score (0-100)")
    active_viewers = meter.create_gauge("premiere.active.viewers", description="Current active viewers in the region")
    startup_failures = meter.create_counter("premiere.startup.failures", description="Number of video startup failures")
    rebuffering_ratio = meter.create_gauge("premiere.rebuffering.ratio", description="Percentage of sessions experiencing rebuffering")
    manifest_latency = meter.create_histogram("premiere.manifest.latency", description="Latency of manifest requests (ms)")

    print(f"Iniciando Simulador de Estreno 'Marquee' (Total ticks: {len(SCRIPT_STEPS)})")
    
    for step in SCRIPT_STEPS:
        tick = step["tick"]
        state = step["state"]
        latam_mod = step["latam_modifier"]
        latency_base = step["latency_base"]
        error_prob = step["error_prob"]
        
        print(f"Tick {tick:02d} | Estado: {state.upper()} | Modificador LATAM: {latam_mod}")
        
        for region, weight in REGIONS.items():
            is_latam_sp = (region == "latam-saopaulo")
            
            # Aplicar modificadores de incidente solo a São Paulo (o toda latam si se desea)
            r_mod = latam_mod if is_latam_sp else 1.0
            r_latency_base = latency_base if is_latam_sp else 80
            r_error_prob = error_prob if is_latam_sp else 0.01

            # 1. Audiencia (Active Viewers)
            # Audiencia base es de ~100k por peso. El modificador baja la audiencia si hay fallos
            base_viewers = 100000 * weight
            viewers = int(random.uniform(base_viewers * 0.95, base_viewers * 1.05) * r_mod)
            active_viewers.set(viewers, {"region": region})
            
            # 2. Calidad de Reproducción (Playback Quality)
            quality = int(random.uniform(95, 100) * r_mod)
            playback_quality.set(quality, {"region": region})
            
            # 3. Fallos de Inicio (Startup Failures)
            # En un estado normal hay muy pocos. En crisis, se disparan.
            failures = int(viewers * random.uniform(r_error_prob * 0.8, r_error_prob * 1.2) * 0.05)
            if failures > 0:
                startup_failures.add(failures, {"region": region})
                
            # 4. Rebuffering Ratio
            rebuf = random.uniform(0.1, 1.0) if not is_latam_sp else random.uniform(r_error_prob * 10, r_error_prob * 20)
            rebuf = min(rebuf, 100.0) # Cap a 100%
            rebuffering_ratio.set(rebuf, {"region": region})
            
            # 5. Latencia de Manifiesto
            # Generamos varias muestras para el histograma en cada tick
            for _ in range(5):
                latency = random.uniform(r_latency_base * 0.8, r_latency_base * 1.2)
                manifest_latency.record(latency, {"region": region})

            # --- LOGS Y TRAZAS ---
            # Para no saturar, solo emitimos logs y trazas si hay errores o de forma muestreada
            with tracer.start_as_current_span("get_manifest") as span:
                span.set_attribute("region", region)
                span.set_attribute("viewers", viewers)
                
                # Simulamos la operación de obtener manifiesto de la CDN
                op_latency = random.uniform(r_latency_base * 0.8, r_latency_base * 1.2)
                span.set_attribute("latency_ms", op_latency)
                
                if random.random() < r_error_prob:
                    # Falla
                    span.set_status(trace.status.Status(trace.status.StatusCode.ERROR))
                    span.record_exception(Exception(f"ManifestTimeoutError: CDN timeout after {op_latency:.0f}ms"))
                    
                    # Emitir Log de error
                    logger.error(f"CDN Error en {region}: ManifestTimeoutError. Latencia observada {op_latency:.0f}ms. Tasa de error actual: {r_error_prob*100:.1f}%")
                else:
                    # Éxito (logueamos solo algunos para no hacer spam, ej. 10% de las veces)
                    if random.random() < 0.1:
                        logger.info(f"Manifiesto servido en {region} (Latencia: {op_latency:.0f}ms)")

        # Esperar antes del siguiente tick
        time.sleep(tick_interval)
        
    print("Simulación terminada.")

if __name__ == "__main__":
    run_simulation(tick_interval=5)
