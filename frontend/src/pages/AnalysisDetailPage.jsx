import React, { useState, useEffect } from 'react';
import {
  ArrowLeft,
  ShieldCheck,
  AlertTriangle,
  AlertOctagon,
  ExternalLink,
  Building,
  Globe,
  Clock,
  Cpu,
  CheckCircle2,
  ListChecks,
  Info,
  Printer,
  Share2
} from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import RiskGauge from '../components/RiskGauge';
import VerificationBadge from '../components/VerificationBadge';
import SignalCard from '../components/SignalCard';
import { api } from '../services/api';

export default function AnalysisDetailPage({
  analysis,
  analysisId,
  setActivePage,
  setSelectedAnalysisId
}) {
  const [data, setData] = useState(analysis || null);
  const [loading, setLoading] = useState(!analysis && !!analysisId);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!analysis && analysisId) {
      setLoading(true);
      api.getHistoryDetail(analysisId)
        .then((res) => setData(res))
        .catch((err) => setError(err.message || 'Failed to load analysis details.'))
        .finally(() => setLoading(false));
    }
  }, [analysis, analysisId]);

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-secondary)' }}>
        <p>Loading forensic threat report...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="card" style={{ maxWidth: '600px', margin: '2rem auto', textAlign: 'center', padding: '2rem' }}>
        <AlertTriangle size={36} color="#ef4444" style={{ margin: '0 auto 1rem' }} />
        <h2 style={{ color: '#fff', fontSize: '1.25rem', marginBottom: '0.5rem' }}>Report Not Found</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
          {error || 'The requested job analysis record could not be loaded.'}
        </p>
        <button onClick={() => setActivePage('analyze')} className="btn btn-primary btn-sm">
          Return to Job Scanner
        </button>
      </div>
    );
  }

  const {
    id,
    timestamp,
    job_title,
    company_name,
    job_url,
    job_description_snippet,
    classification,
    risk_score,
    risk_level_explanation,
    ml_prediction,
    detected_signals,
    verification,
    recommendations,
    disclaimer
  } = data;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Top Navigation & Actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <button
          onClick={() => {
            if (setSelectedAnalysisId) setSelectedAnalysisId(null);
            setActivePage('analyze');
          }}
          className="btn btn-secondary btn-sm"
        >
          <ArrowLeft size={14} />
          <span>Back to Scanner</span>
        </button>

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button onClick={handlePrint} className="btn btn-secondary btn-sm" title="Print this report">
            <Printer size={14} />
            <span>Print Report</span>
          </button>
        </div>
      </div>

      {/* Report Header Card */}
      <div className="card" style={{ borderTop: `4px solid ${risk_score >= 70 ? '#ef4444' : risk_score >= 35 ? '#f59e0b' : '#10b981'}` }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1.5rem' }}>
          <div style={{ flex: 1, minWidth: '280px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.4rem', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
                {company_name || 'Unspecified Employer'}
              </span>
              <VerificationBadge status={verification?.status} domain={verification?.official_domain} />
              {id && (
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  #AUDIT-{id}
                </span>
              )}
            </div>

            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff', lineHeight: 1.2, marginBottom: '0.5rem' }}>
              {job_title}
            </h1>

            {job_url && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem', color: 'var(--text-muted)', wordBreak: 'break-all' }}>
                <Globe size={13} />
                <a href={job_url} target="_blank" rel="noopener noreferrer" style={{ color: '#60a5fa', textDecoration: 'underline' }}>
                  {job_url}
                </a>
              </div>
            )}

            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
              <Clock size={12} />
              <span>Audited on {timestamp ? new Date(timestamp).toLocaleString() : 'Recent'}</span>
            </div>
          </div>

          {/* Risk Gauge Header Widget */}
          <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-md)', minWidth: '180px' }}>
            <RiskGauge score={risk_score} classification={classification} />
          </div>
        </div>

        <div style={{ marginTop: '1.25rem', paddingTop: '1.25rem', borderTop: '1px solid var(--border-subtle)' }}>
          <p style={{ fontSize: '0.95rem', color: '#fff', fontWeight: 600 }}>
            {risk_level_explanation}
          </p>
        </div>
      </div>

      {/* Official Company Website & Apply Feature (Section 6 Key Feature) */}
      <div className="card" style={{
        background: verification?.vacancy_verified
          ? 'linear-gradient(135deg, rgba(16, 185, 129, 0.08), rgba(6, 78, 59, 0.15))'
          : verification?.status === 'MISMATCH'
          ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(127, 29, 29, 0.15))'
          : 'var(--bg-card)',
        borderColor: verification?.vacancy_verified
          ? 'rgba(16, 185, 129, 0.3)'
          : verification?.status === 'MISMATCH'
          ? 'rgba(239, 68, 68, 0.35)'
          : 'var(--border-subtle)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <Building size={18} color="#3b82f6" />
              <h2 className="card-title" style={{ fontSize: '1.15rem' }}>
                Employer & Domain Verification Status
              </h2>
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', maxWidth: '650px', lineHeight: 1.5 }}>
              {verification?.notes || 'Company domain corroboration results.'}
            </p>
          </div>

          <div>
            {verification?.vacancy_verified && verification?.official_apply_url ? (
              <a
                href={verification.official_apply_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-success"
                style={{ padding: '0.75rem 1.5rem', fontSize: '0.95rem' }}
              >
                <span>Apply on Official Website</span>
                <ExternalLink size={16} />
              </a>
            ) : verification?.official_career_url ? (
              <a
                href={verification.official_career_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ borderColor: '#3b82f6', color: '#60a5fa' }}
              >
                <span>Visit Official Careers Portal</span>
                <ExternalLink size={14} />
              </a>
            ) : verification?.official_career_url ? (
              <a
                href={verification.official_career_url}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ borderColor: '#3b82f6', color: '#60a5fa' }}
              >
                <span>Visit Official Careers Portal</span>
                <ExternalLink size={14} />
              </a>
            ) : company_name && company_name.trim() ? (
              <a
                href={`https://www.google.com/search?q=${encodeURIComponent(company_name + ' official website careers')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="btn btn-secondary"
                style={{ borderColor: '#f59e0b', color: '#fbbf24' }}
                title="Search results are not verification. Confirm the domain before applying."
              >
                <span>Find Official Website</span>
                <ExternalLink size={14} />
              </a>
            ) : (
              <div style={{
                fontSize: '0.8rem',
                color: '#ef4444',
                background: 'rgba(239, 68, 68, 0.12)',
                padding: '0.5rem 0.85rem',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 600,
                border: '1px solid rgba(239, 68, 68, 0.25)'
              }}>
                Enter an employer name to find its website
              </div>
            )}
          </div>
        </div>

        {/* Verification Evidence List */}
        {verification?.evidence?.length > 0 && (
          <div style={{ marginTop: '1rem', paddingTop: '1rem', borderTop: '1px solid var(--border-subtle)' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
              Verification Evidence:
            </span>
            <ul style={{ listStyle: 'none', marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
              {verification.evidence.map((item, idx) => (
                <li key={idx} style={{ fontSize: '0.825rem', color: '#cbd5e1', display: 'flex', alignItems: 'flex-start', gap: '6px' }}>
                  <span style={{ color: verification.status === 'MISMATCH' ? '#ef4444' : '#10b981' }}>•</span>
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Two-Column Breakdown: Detected Threat Signals vs ML Architecture */}
      <div className="grid-2">
        {/* Detected Threats */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Detected Threat Signals</h2>
              <p className="card-subtitle">
                {detected_signals?.length || 0} heuristic indicator(s) identified
              </p>
            </div>
          </div>

          {detected_signals?.length === 0 ? (
            <div style={{ padding: '1.5rem', textAlign: 'center', color: '#10b981', background: 'rgba(16, 185, 129, 0.05)', borderRadius: 'var(--radius-md)' }}>
              <CheckCircle2 size={28} style={{ margin: '0 auto 0.5rem' }} />
              <p style={{ fontWeight: 600 }}>No active scam patterns detected</p>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                The job description contains no demands for registration fees, telegram contacts, or unrealistic compensation claims.
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {detected_signals.map((signal, idx) => (
                <SignalCard key={idx} signal={signal} />
              ))}
            </div>
          )}
        </div>

        {/* Machine Learning Model Diagnostics */}
        <div className="card">
          <div className="card-header">
            <div>
              <h2 className="card-title">Machine Learning Classification</h2>
              <p className="card-subtitle">EMSCAD NLP Pipeline Inference</p>
            </div>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: 'var(--radius-sm)',
              background: 'rgba(59, 130, 246, 0.1)',
              color: '#3b82f6',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}>
              <Cpu size={18} />
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Model Prediction</span>
              <span style={{ fontWeight: 700, color: ml_prediction?.is_fake ? '#ef4444' : '#10b981' }}>
                {ml_prediction?.is_fake ? 'FRAUDULENT' : 'LEGITIMATE'}
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Estimated Fraud Probability</span>
              <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>
                {Math.round((ml_prediction?.fraud_probability || 0) * 100)}%
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Classification Confidence</span>
              <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', color: '#fff' }}>
                {Math.round((ml_prediction?.confidence || 0) * 100)}%
              </span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '0.75rem 1rem', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-sm)' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Algorithm Architecture</span>
              <span style={{ fontSize: '0.8rem', color: '#94a3b8', textAlign: 'right' }}>
                {ml_prediction?.algorithm || 'TF-IDF + Calibrated Classifier'}
              </span>
            </div>

            {ml_prediction?.is_fallback && (
              <div className="alert alert-warning" style={{ fontSize: '0.8rem', margin: 0 }}>
                <Info size={14} />
                <span>Deterministic heuristic fallback mode active (model uninitialized).</span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recommended Next Steps */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
          <ListChecks size={20} color="#3b82f6" />
          <h2 className="card-title">Recommended Safety Next Steps</h2>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
          {recommendations?.map((rec, idx) => (
            <div key={idx} style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.6rem',
              padding: '0.75rem 1rem',
              background: 'var(--bg-secondary)',
              borderRadius: 'var(--radius-sm)',
              fontSize: '0.875rem',
              color: '#f1f5f9'
            }}>
              <span style={{
                color: '#3b82f6',
                fontWeight: 700,
                width: '20px',
                height: '20px',
                borderRadius: '50%',
                background: 'rgba(59, 130, 246, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.75rem',
                flexShrink: 0
              }}>
                {idx + 1}
              </span>
              <span>{rec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Forensic Disclaimer */}
      <div style={{
        padding: '1rem 1.25rem',
        background: 'rgba(255, 255, 255, 0.03)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-subtle)',
        fontSize: '0.8rem',
        color: 'var(--text-muted)',
        lineHeight: 1.6
      }}>
        <p>
          <strong>Transparency Notice:</strong> {disclaimer}
        </p>
      </div>
    </div>
  );
}
