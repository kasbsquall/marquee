import { useState, useEffect } from 'react';
import { Activity, AlertTriangle, ShieldCheck, Zap, Server, Radio, Power } from 'lucide-react';
import './index.css';

function App() {
  const [logs, setLogs] = useState([]);
  const [selectedPlays, setSelectedPlays] = useState(new Set());
  const [isAuthorizing, setIsAuthorizing] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  // Simulación del log stream del Watcher
  useEffect(() => {
    const initialLogs = [
      { time: '22:40:01', level: 'info', msg: 'System stable. Market: latam-saopaulo' },
      { time: '22:40:15', level: 'info', msg: 'Latency 120ms' },
    ];
    
    setLogs(initialLogs);
    
    const incidentSequence = [
      { delay: 2000, log: { time: '22:40:30', level: 'error', msg: 'ManifestTimeoutError: CDN timeout after 1342ms' } },
      { delay: 3500, log: { time: '22:40:35', level: 'error', msg: 'ManifestTimeoutError: CDN timeout after 1450ms' } },
      { delay: 5000, log: { time: '22:40:41', level: 'error', msg: 'High startup failures detected (8,856 total)' } },
      { delay: 6500, log: { time: '22:40:50', level: 'warning', msg: 'Analyst triggered: Evaluating business impact' } }
    ];

    incidentSequence.forEach(({ delay, log }) => {
      setTimeout(() => {
        setLogs(prev => [...prev, log]);
      }, delay);
    });
  }, []);

  const togglePlay = (id) => {
    const next = new Set(selectedPlays);
    if (next.has(id)) {
      next.delete(id);
    } else {
      next.add(id);
    }
    setSelectedPlays(next);
  };

  const handleAuthorize = () => {
    setIsAuthorizing(true);
    // Simular llamada al Executor
    setTimeout(() => {
      setIsAuthorizing(false);
      setShowSuccessModal(true);
      
      // Añadir log de auditoría
      const d = new Date();
      setLogs(prev => [...prev, { 
        time: `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}`, 
        level: 'info', 
        msg: `Executor Action: Authorized plays [${Array.from(selectedPlays).join(', ')}] applied to Grafana` 
      }]);
    }, 1500);
  };

  const plays = [
    {
      id: 1,
      title: "Conmutar a CDN de Respaldo",
      icon: <Server size={20} color="#00f0ff" />,
      cost: "Alto ($$)",
      risk: "Medio",
      time: "~2 min",
      riskLevel: "medium"
    },
    {
      id: 2,
      title: "Modo 'Crisis de Audiencia'",
      icon: <Radio size={20} color="#ff3366" />,
      cost: "Muy Alto (PR)",
      risk: "Bajo",
      time: "Inmediato",
      riskLevel: "low"
    }
  ];

  return (
    <div className="dashboard-container">
      <header>
        <div className="logo-area">
          <Activity size={32} className="logo-icon" />
          <h1>Marquee</h1>
        </div>
        <div className="status-badge">
          <AlertTriangle size={16} />
          CRITICAL: latam-saopaulo
        </div>
      </header>

      <div className="main-grid">
        {/* Columna Izquierda: Telemetría y Análisis */}
        <div className="glass-panel">
          <div className="panel-header warning">
            <Activity size={24} />
            Watcher & Analyst Stream
          </div>
          
          <div className="analyst-summary">
            <div className="analyst-title">Diagnóstico de Negocio</div>
            <div className="analyst-text">
              <strong>IMPACTO:</strong> Caída en mercado #2 (São Paulo), arriesgando $40,000/min.<br/>
              <strong>CAUSA:</strong> Logs confirman ManifestTimeoutError continuo de la CDN primaria.
            </div>
          </div>

          <div className="log-stream">
            {logs.map((log, idx) => (
              <div key={idx} className="log-entry">
                <span className="log-time">[{log.time}]</span>
                <span className={`log-level ${log.level}`}>
                  {log.level.toUpperCase()}
                </span>
                <span className="log-message">{log.msg}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Columna Derecha: Advisor y Ejecución */}
        <div className="glass-panel">
          <div className="panel-header">
            <Zap size={24} color="#00f0ff" />
            Advisor Playbook
          </div>
          
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
            Selecciona las jugadas de mitigación a autorizar para el Executor.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '0.5rem' }}>
            {plays.map(play => (
              <div 
                key={play.id} 
                className={`play-card ${selectedPlays.has(play.id) ? 'selected' : ''}`}
                onClick={() => togglePlay(play.id)}
              >
                <div className="play-title">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    {play.icon}
                    {play.title}
                  </div>
                  {selectedPlays.has(play.id) && <ShieldCheck size={20} color="#00f0ff" />}
                </div>
                
                <div className="play-meta">
                  <div className="meta-item">
                    <span className="meta-label">Costo</span>
                    <span className="meta-value">{play.cost}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-label">Riesgo</span>
                    <span className={`meta-value ${play.risk === 'Alto' ? 'high-risk' : play.risk === 'Bajo' ? 'low-risk' : ''}`}>
                      {play.risk}
                    </span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-label">Tiempo</span>
                    <span className="meta-value">{play.time}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="action-bar">
            <button 
              className="btn-authorize" 
              disabled={selectedPlays.size === 0 || isAuthorizing}
              onClick={handleAuthorize}
            >
              <Power size={20} />
              {isAuthorizing ? 'Ejecutando...' : 'AUTORIZAR EJECUCIÓN'}
            </button>
          </div>
        </div>
      </div>

      {showSuccessModal && (
        <div className="modal-overlay" onClick={() => setShowSuccessModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <ShieldCheck className="modal-icon" />
            <h2 style={{ color: '#fff', marginBottom: '1rem', fontFamily: 'Outfit' }}>Acción Ejecutada</h2>
            <p style={{ color: 'var(--text-secondary)' }}>
              El Executor ha registrado la decisión en Grafana vía MCP y ha actualizado el dashboard del incidente.
            </p>
            <button 
              style={{
                marginTop: '1.5rem',
                padding: '0.75rem 2rem',
                background: 'rgba(255,255,255,0.1)',
                border: '1px solid rgba(255,255,255,0.2)',
                color: '#fff',
                borderRadius: '8px',
                cursor: 'pointer'
              }}
              onClick={() => setShowSuccessModal(false)}
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
