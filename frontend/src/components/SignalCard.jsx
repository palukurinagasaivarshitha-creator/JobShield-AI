import React from 'react';
import { AlertCircle, AlertTriangle, DollarSign, MessageSquare, ShieldAlert, Globe } from 'lucide-react';

export default function SignalCard({ signal }) {
  const { name, severity, category, description, evidence } = signal;

  const severityClass = (severity || 'low').toLowerCase();

  const getCategoryIcon = (cat) => {
    switch ((cat || '').toUpperCase()) {
      case 'FINANCIAL':
        return <DollarSign size={16} />;
      case 'CONTACT':
        return <MessageSquare size={16} />;
      case 'DOMAIN':
        return <Globe size={16} />;
      default:
        return <ShieldAlert size={16} />;
    }
  };

  const getSeverityBadge = (sev) => {
    const s = (sev || '').toUpperCase();
    if (s === 'CRITICAL') return <span className="badge badge-high-risk">CRITICAL THREAT</span>;
    if (s === 'HIGH') return <span className="badge" style={{ background: 'rgba(249, 115, 22, 0.15)', color: '#fb923c', border: '1px solid rgba(249, 115, 22, 0.3)' }}>HIGH RISK</span>;
    if (s === 'MEDIUM') return <span className="badge badge-suspicious">MEDIUM CAUTION</span>;
    return <span className="badge badge-verified">LOW RISK</span>;
  };

  return (
    <div className={`signal-item ${severityClass}`}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '0.4rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span style={{ color: 'var(--text-secondary)' }}>
            {getCategoryIcon(category)}
          </span>
          <span style={{ fontWeight: 700, fontSize: '0.95rem', color: '#fff' }}>
            {name}
          </span>
        </div>
        <div>
          {getSeverityBadge(severity)}
        </div>
      </div>

      <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: evidence ? '0.5rem' : '0' }}>
        {description}
      </p>

      {evidence && (
        <div style={{
          marginTop: '0.4rem',
          padding: '0.4rem 0.75rem',
          background: 'rgba(0, 0, 0, 0.25)',
          borderRadius: 'var(--radius-sm)',
          fontSize: '0.8rem',
          fontFamily: 'var(--font-mono)',
          color: '#cbd5e1',
          borderLeft: '2px solid rgba(255, 255, 255, 0.2)'
        }}>
          {evidence}
        </div>
      )}
    </div>
  );
}
