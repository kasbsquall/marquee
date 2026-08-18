# Marquee Executive Remediation Playbook

Este playbook contiene el catálogo de jugadas (plays) que el sistema ADK puede proponer a los ejecutivos del estreno ante incidentes críticos. 

Cada vez que el Analyst reporta una degradación con riesgo financiero y su causa raíz técnica, el Advisor cruzará esa información con las jugadas documentadas aquí para presentar opciones con trade-offs transparentes.

## Jugadas Técnicas (Infraestructura)

### 1. Conmutar a CDN de Respaldo (Failover)
* **Condición de uso:** `ManifestTimeoutError`, alta latencia o pérdida severa de paquetes en la CDN primaria.
* **Costo Financiero:** Alto (doble facturación por uso no planeado del contrato de contingencia).
* **Riesgo:** Medio. Los cachés estarán fríos, causando un pequeño pico inicial de latencia mientras se llenan.
* **Tiempo efectivo:** ~2 minutos (propagación de DNS y re-enrutamiento de borde).

### 2. Degradar Bitrate Máximo de Video (Throttling)
* **Condición de uso:** Saturación de red regional, picos extremos inesperados de tráfico.
* **Costo Financiero:** Ninguno directo.
* **Riesgo:** Alto impacto en la marca. Los espectadores en 4K/1080p bajarán forzosamente a 720p, lo que puede causar quejas masivas en redes sociales ("La imagen se ve pixelada").
* **Tiempo efectivo:** Casi Inmediato (~30 segundos en el próximo ciclo de manifiesto de los reproductores).

### 3. Reiniciar Pods de Streaming (Escalado Forzoso)
* **Condición de uso:** Fugas de memoria, deadlocks o colapso de base de datos en los microservicios locales.
* **Costo Financiero:** Bajo (pequeño aumento en compute cloud).
* **Riesgo:** Extremadamente alto en medio de un estreno. Si la carga es muy alta, los pods pueden entrar en *CrashLoopBackOff* durante el reinicio por la estampida de conexiones.
* **Tiempo efectivo:** 3-5 minutos (drenaje de conexiones y startups de contenedores).

---

## Jugadas de Negocio (Producto y Comunicación)

### 4. Retrasar Lanzamiento Escalonado Regional
* **Condición de uso:** Caídas críticas antes o durante los primeros minutos del estreno en una región que estaba por arrancar.
* **Costo Financiero:** Medio. Posibles cancelaciones y frustración publicitaria.
* **Riesgo:** Medio. Cambiar los horarios prometidos de estreno afecta a los partners locales de la región.
* **Tiempo efectivo:** Inmediato (bloqueo en base de datos de control de acceso).

### 5. Modo "Crisis de Audiencia": Notificación Push In-App + Banner
* **Condición de uso:** Error generalizado e inocultable que afecta la experiencia de más del 30% del mercado.
* **Costo Financiero:** Muy Alto (reembolsos parciales o créditos en la cuenta para calmar la ira del consumidor).
* **Riesgo:** Bajo desde la parte técnica, pero asume control de daños de Relaciones Públicas. "Estamos experimentando alta demanda, tu calidad podría verse afectada. Te obsequiaremos un cupón."
* **Tiempo efectivo:** Inmediato.

## Instrucciones para el Advisor
- NUNCA selecciones más de 3 opciones en total.
- SIEMPRE mezcla al menos una jugada técnica y una jugada de negocio/comunicación.
- Formatea explícitamente el Costo, Riesgo y Tiempo de cada opción elegida.
