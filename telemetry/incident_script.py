"""
Guion reproducible del estreno global.
El simulador leerá este guion tick a tick para emitir métricas, logs y trazas.
El incidente ocurre en la región de São Paulo (latam-saopaulo) afectando la latencia del manifiesto y la calidad.
"""

SCRIPT_STEPS = [
    # Fase 1: Estreno normal y exitoso
    {"tick": 0, "state": "normal", "latam_modifier": 1.0, "latency_base": 80, "error_prob": 0.01},
    {"tick": 1, "state": "normal", "latam_modifier": 1.0, "latency_base": 80, "error_prob": 0.01},
    {"tick": 2, "state": "normal", "latam_modifier": 1.0, "latency_base": 80, "error_prob": 0.01},
    
    # Fase 2: Comienza la degradación (nadie lo nota en el negocio todavía)
    {"tick": 3, "state": "degraded", "latam_modifier": 0.9, "latency_base": 300, "error_prob": 0.15},
    {"tick": 4, "state": "degraded", "latam_modifier": 0.8, "latency_base": 800, "error_prob": 0.30},
    
    # Fase 3: Incidente crítico (la audiencia empieza a abandonar por buffering y fallos)
    {"tick": 5, "state": "critical", "latam_modifier": 0.6, "latency_base": 2500, "error_prob": 0.60},
    {"tick": 6, "state": "critical", "latam_modifier": 0.4, "latency_base": 3500, "error_prob": 0.80},
    {"tick": 7, "state": "critical", "latam_modifier": 0.3, "latency_base": 4000, "error_prob": 0.90},
    {"tick": 8, "state": "critical", "latam_modifier": 0.3, "latency_base": 4500, "error_prob": 0.95},
    {"tick": 9, "state": "critical", "latam_modifier": 0.3, "latency_base": 4500, "error_prob": 0.95},
    
    # Fase 4: Se aplica la mitigación (ej. switch a CDN backup) y empieza la recuperación
    {"tick": 10, "state": "recovering", "latam_modifier": 0.6, "latency_base": 400, "error_prob": 0.20},
    {"tick": 11, "state": "recovering", "latam_modifier": 0.8, "latency_base": 150, "error_prob": 0.05},
    
    # Fase 5: Estabilizado
    {"tick": 12, "state": "normal", "latam_modifier": 0.95, "latency_base": 80, "error_prob": 0.01},
    {"tick": 13, "state": "normal", "latam_modifier": 1.0, "latency_base": 80, "error_prob": 0.01},
]
