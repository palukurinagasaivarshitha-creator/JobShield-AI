import React from 'react';
import { Building, MapPin, DollarSign, ExternalLink, ShieldCheck, ArrowRight, CheckCircle2, AlertTriangle } from 'lucide-react';
import RiskBadge from './RiskBadge';

export default function JobCard({ job, onAnalyze }) {
  const {
    id,
    title,
    company,
    location,
    salary_range,
    description,
    source,
    official_domain,
    official_apply_url,
    is_verified_posting,
    initial_risk_estimate
  } = job;

  return (
    <div className="card" style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div className="card-header" style={{ marginBottom: '0.75rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>
              {company}
            </span>
            {is_verified_posting && (
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '3px',
                  fontSize: '0.7rem',
                  color: '#10b981',
                  background: 'rgba(16, 185, 129, 0.1)',
                  padding: '1px 6px',
                  borderRadius: '999px',
                  fontWeight: 600
                }}
              >
                <CheckCircle2 size={11} /> Verified Employer
              </span>
            )}
          </div>
          <h3 className="card-title" style={{ fontSize: '1.05rem', lineHeight: 1.3 }}>
            {title}
          </h3>
        </div>
        <RiskBadge classification={initial_risk_estimate} size="sm" />
      </div>

      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <MapPin size={13} color="#94a3b8" /> {location}
        </span>
        {salary_range && (
          <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <DollarSign size={13} color="#10b981" /> {salary_range}
          </span>
        )}
      </div>

      <p style={{
        fontSize: '0.85rem',
        color: 'var(--text-secondary)',
        lineHeight: 1.5,
        marginBottom: '1rem',
        display: '-webkit-box',
        WebkitLineClamp: 3,
        WebkitBoxOrient: 'vertical',
        overflow: 'hidden',
        flex: 1
      }}>
        {description}
      </p>

      {/* Domain Corroboration Metadata */}
      <div style={{
        padding: '0.5rem 0.75rem',
        background: 'var(--bg-secondary)',
        borderRadius: 'var(--radius-sm)',
        fontSize: '0.75rem',
        color: 'var(--text-muted)',
        marginBottom: '1rem',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <span>Source: <strong>{source}</strong></span>
        {official_domain && (
          <span style={{ fontFamily: 'var(--font-mono)' }}>{official_domain}</span>
        )}
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto' }}>
        {is_verified_posting && official_apply_url ? (
          <a
            href={official_apply_url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-success btn-sm"
            style={{ flex: 1 }}
          >
            <span>Apply on Official Website</span>
            <ExternalLink size={13} />
          </a>
        ) : (
          <div
            style={{
              flex: 1,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '4px',
              fontSize: '0.75rem',
              color: '#ef4444',
              background: 'rgba(239, 68, 68, 0.08)',
              padding: '0.4rem',
              borderRadius: 'var(--radius-sm)',
              fontWeight: 600
            }}
          >
            <AlertTriangle size={12} /> Apply Link Blocked (Unverified)
          </div>
        )}

        <button
          onClick={() => onAnalyze && onAnalyze(job)}
          className="btn btn-secondary btn-sm"
          title="Run full AI threat scan on this posting"
        >
          <span>Audit AI</span>
          <ArrowRight size={13} />
        </button>
      </div>
    </div>
  );
}
