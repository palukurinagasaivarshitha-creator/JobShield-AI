import React from 'react';
import { Shield, ExternalLink, Github, Database, FileText } from 'lucide-react';

export default function Footer({ setActivePage }) {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-top">
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.5rem' }}>
              <div className="nav-brand-icon" style={{ width: '28px', height: '28px' }}>
                <Shield size={16} />
              </div>
              <span style={{ fontWeight: 800, fontSize: '1.05rem', color: '#fff' }}>
                Job<span style={{ color: '#3b82f6' }}>Shield</span> AI
              </span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', maxWidth: '420px' }}>
              Advanced multi-vector recruitment fraud intelligence platform combining EMSCAD-trained machine learning, rule-based threat heuristics, and authoritative company domain corroboration.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '2rem', flexWrap: 'wrap' }}>
            <div>
              <h4 style={{ color: '#fff', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.75rem' }}>Navigation</h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <li><button onClick={() => setActivePage('landing')} style={{ color: 'inherit' }}>Home</button></li>
                <li><button onClick={() => setActivePage('dashboard')} style={{ color: 'inherit' }}>Dashboard</button></li>
                <li><button onClick={() => setActivePage('analyze')} style={{ color: 'inherit' }}>Analyze Job</button></li>
                <li><button onClick={() => setActivePage('search')} style={{ color: 'inherit' }}>Verified Jobs</button></li>
                <li><button onClick={() => setActivePage('history')} style={{ color: 'inherit' }}>Audit History</button></li>
              </ul>
            </div>

            <div>
              <h4 style={{ color: '#fff', fontSize: '0.85rem', fontWeight: 700, marginBottom: '0.75rem' }}>ML & References</h4>
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.4rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <li>
                  <a href="http://recruiting.icsd.aegean.gr/scamdata/" target="_blank" rel="noopener noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    EMSCAD Dataset <ExternalLink size={12} />
                  </a>
                </li>
                <li>
                  <a href="/docs" target="_blank" rel="noopener noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    FastAPI Swagger <ExternalLink size={12} />
                  </a>
                </li>
                <li>
                  <button onClick={() => setActivePage('about')} style={{ color: 'inherit' }}>
                    Architecture & Models
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="footer-disclaimer">
          <p>
            <strong>Important Safety Notice:</strong> JobShield AI is an investigative decision-support tool. A "SAFE" classification signifies standard lexical patterns and absence of detected scam keywords, but does not constitute an absolute guarantee of employer authenticity. Job seekers must never transfer funds, purchase equipment, or disclose confidential financial credentials for job offers.
          </p>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.75rem', flexWrap: 'wrap', gap: '0.5rem', color: 'var(--text-muted)' }}>
            <span>&copy; {new Date().getFullYear()} Fake Job Detection & Verification Platform. Built with React & FastAPI.</span>
            <span>CC BY 4.0 EMSCAD Model Foundation</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
