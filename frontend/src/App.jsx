import { useState, useEffect } from 'react';
import { Activity, Radio, Server, CheckCircle2, Terminal, Cpu, ShieldAlert } from 'lucide-react';
import './index.css';

function App() {
  const [logs, setLogs] = useState([]);
  const [selectedPlays, setSelectedPlays] = useState(new Set());
  const [isAuthorizing, setIsAuthorizing] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  // Simulated Watcher & Analyst Log Stream
  useEffect(() => {
    const initialLogs = [
      { time: '22:40:01', level: 'info', msg: '[System] Baseline stable. Target market: latam-saopaulo' },
      { time: '22:40:15', level: 'info', msg: '[Network] P99 Latency measuring at 120ms' },
    ];
    
    setLogs(initialLogs);
    
    const incidentSequence = [
      { delay: 2000, log: { time: '22:40:30', level: 'error', msg: 'ManifestTimeoutError: Primary CDN timeout after 1342ms' } },
      { delay: 3500, log: { time: '22:40:35', level: 'error', msg: 'ManifestTimeoutError: Primary CDN timeout after 1450ms' } },
      { delay: 5000, log: { time: '22:40:41', level: 'error', msg: 'CRITICAL: High startup failures detected (8,856 concurrent events)' } },
      { delay: 6500, log: { time: '22:40:50', level: 'warning', msg: '[Analyst] Triggered: Evaluating business impact...' } },
      { delay: 8000, log: { time: '22:40:52', level: 'info', msg: '[Advisor] Playbook generated. Awaiting Executive Authorization.' } }
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
    // Simulate Executor delay via MCP
    setTimeout(() => {
      setIsAuthorizing(false);
      setShowSuccessModal(true);
      
      const d = new Date();
      setLogs(prev => [...prev, { 
        time: `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()}`, 
        level: 'info', 
        msg: `[Executor] Action Complete: Authorized plays [${Array.from(selectedPlays).join(', ')}] committed to Grafana Cloud.` 
      }]);
    }, 1500);
  };

  const plays = [
    {
      id: 1,
      title: "Initiate CDN Failover",
      description: "Immediately route all traffic from primary Edge nodes to the backup CDN provider in the latam region.",
      icon: <Server size={20} color="#22d3ee" />,
      cost: "High ($$)",
      risk: "Medium",
      time: "~2 min",
      riskLevel: "medium"
    },
    {
      id: 2,
      title: "Audience Crisis Mode",
      description: "Deploy emergency push notifications and in-app banners explaining the delay to prevent subscriber churn.",
      icon: <Radio size={20} color="#f43f5e" />,
      cost: "Very High (PR)",
      risk: "Low",
      time: "Immediate",
      riskLevel: "low"
    }
  ];

  return (
    <>
      {/* Top Navigation */}
      <nav className="top-nav">
        <div className="logo-area">
          <Activity size={24} className="logo-icon" />
          <span className="brand-title">Marquee <span className="brand-accent">Global Premiere Control</span></span>
        </div>
        <div className="nav-metrics">
          <div className="nav-metric-item">
            <span className="nav-metric-label">Global Viewers</span>
            <span className="nav-metric-value pulse">14.2M</span>
          </div>
          <div className="nav-metric-item">
            <span className="nav-metric-label">Ingress Bitrate</span>
            <span className="nav-metric-value">4.8 Tbps</span>
          </div>
          <div className="nav-metric-item">
            <span className="nav-metric-label">Active Region</span>
            <span className="nav-metric-value" style={{color: '#94a3b8'}}>LATAM</span>
          </div>
        </div>
      </nav>

      {/* Main Bento Grid */}
      <main className="dashboard-container">
        
        {/* Left Column: Telemetry */}
        <div className="glass-panel">
          <div className="panel-header">
            <h2 className="panel-title"><Terminal size={20} /> Live Telemetry & Analyst Stream</h2>
            <div className="status-badge">
              <ShieldAlert size={14} />
              CRITICAL: latam-saopaulo
            </div>
          </div>
          
          <div className="analyst-summary">
            <div className="analyst-title">Business Impact Assessment</div>
            <div className="analyst-text">
              <span className="analyst-highlight">IMPACT:</span> Severe degradation in Market #2 (São Paulo), risking $40,000/min.<br/>
              <span className="analyst-highlight">ROOT CAUSE:</span> Logs confirm continuous ManifestTimeoutError from primary CDN.
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

        {/* Right Column: Playbook */}
        <div className="glass-panel">
          <div className="panel-header" style={{ marginBottom: '1rem' }}>
            <h2 className="panel-title"><Cpu size={20} color="#22d3ee" /> Executive Action Playbook</h2>
          </div>
          
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1.5rem', lineHeight: '1.5' }}>
            Advisor Agent has generated the following mitigation plays based on the current incident signature. Select the plays you wish to authorize for immediate execution.
          </p>

          <div className="plays-grid">
            {plays.map(play => (
              <div 
                key={play.id} 
                className={`play-card ${selectedPlays.has(play.id) ? 'selected' : ''}`}
                onClick={() => togglePlay(play.id)}
              >
                <div className="play-header">
                  <div className="play-title-group">
                    <div className="play-icon-wrap">{play.icon}</div>
                    <div>
                      <div className="play-title">{play.title}</div>
                      <div className="play-description">{play.description}</div>
                    </div>
                  </div>
                  {selectedPlays.has(play.id) && <CheckCircle2 size={24} color="#22d3ee" />}
                </div>
                
                <div className="play-metrics">
                  <div className="p-metric">
                    <span className="p-metric-label">Cost</span>
                    <span className="p-metric-val">{play.cost}</span>
                  </div>
                  <div className="p-metric">
                    <span className="p-metric-label">Risk</span>
                    <span className={`p-metric-val ${play.riskLevel === 'medium' ? 'val-med' : 'val-low'}`}>
                      {play.risk}
                    </span>
                  </div>
                  <div className="p-metric">
                    <span className="p-metric-label">ETA</span>
                    <span className="p-metric-val mono">{play.time}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="action-footer">
            <div className="selection-info">
              Selected Plays: <span>{selectedPlays.size}</span>
            </div>
            <button 
              className="btn-authorize" 
              disabled={selectedPlays.size === 0 || isAuthorizing}
              onClick={handleAuthorize}
            >
              {isAuthorizing ? 'EXECUTING...' : 'AUTHORIZE EXECUTION'}
            </button>
          </div>
        </div>
      </main>

      {/* Success Modal */}
      {showSuccessModal && (
        <div className="modal-overlay" onClick={() => setShowSuccessModal(false)}>
          <div className="modal-card" onClick={e => e.stopPropagation()}>
            <div className="modal-icon-wrap">
              <CheckCircle2 size={32} color="#10b981" />
            </div>
            <h2 className="modal-title">Execution Authorized</h2>
            <p className="modal-desc">
              The Executor Agent has securely registered your decision in Grafana via MCP and updated the active incident dashboard. Mitigations are now in progress.
            </p>
            <button className="btn-ghost" onClick={() => setShowSuccessModal(false)}>
              Close Terminal
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default App;
