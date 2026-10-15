import React, { useState, useEffect } from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon, Activity, FileSearch, ArrowRight, RefreshCw, ExternalLink } from 'lucide-react';
import { api } from '../services/api';
import StatsCounter from '../components/StatsCounter';
import RiskBadge from '../components/RiskBadge';
import ErrorAlert from '../components/ErrorAlert';

export default function DashboardPage({ setActivePage, setSelectedAnalysisId }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch dashboard metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  const handleViewReport = (id) => {
    if (setSelectedAnalysisId) {
      setSelectedAnalysisId(id);
      setActivePage('detail');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* Page Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff' }}>Security Intelligence Dashboard</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
            Real-time telemetry, threat detection metrics, and recent job authenticity audits
          </p>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button onClick={fetchStats} className="btn btn-secondary btn-sm" disabled={loading}>
            <RefreshCw size={14} className={loading ? 'spin' : ''} />
            <span>Refresh</span>
          </button>
          <button onClick={() => setActivePage('analyze')} className="btn btn-primary btn-sm">
            <FileSearch size={14} />
            <span>New Scan</span>
          </button>
        </div>
      </div>

      <ErrorAlert message={error} onRetry={fetchStats} />

      {/* Metrics Row */}
      <div className="grid-4">
        <StatsCounter
          title="Total Scans Logged"
          value={loading ? '...' : (stats?.total_scans ?? 0)}
          icon={Activity}
          color="#3b82f6"
          subtitle="Persistent database audit records"
        />
        <StatsCounter
          title="Safe Postings"
          value={loading ? '...' : (stats?.safe_count ?? 0)}
          icon={ShieldCheck}
          color="#10b981"
          subtitle="Verified genuine patterns"
        />
        <StatsCounter
          title="Suspicious Flags"
          value={loading ? '...' : (stats?.suspicious_count ?? 0)}
          icon={AlertTriangle}
          color="#f59e0b"
          subtitle="Anomalies requiring caution"
        />
        <StatsCounter
          title="High Risk Blocked"
          value={loading ? '...' : (stats?.high_risk_count ?? 0)}
          icon={AlertOctagon}
          color="#ef4444"
          subtitle="Direct recruitment scam threats"
        />
      </div>

      {/* Secondary Highlights Row */}
      <div className="grid-2">
        <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1.5rem' }}>
          <div>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
              Corroborated Corporate Vacancies
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#10b981', marginTop: '0.25rem' }}>
              {loading ? '...' : (stats?.verified_vacancies_count ?? 0)}
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              Official apply links enabled via verified employer infrastructure
            </p>
          </div>
          <button onClick={() => setActivePage('search')} className="btn btn-secondary btn-sm">
            <span>Browse Jobs</span>
            <ArrowRight size={13} />
          </button>
        </div>

        <div className="card" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '1.5rem' }}>
          <div>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
              Platform Threat Average
            </span>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: '#f59e0b', marginTop: '0.25rem' }}>
              {loading ? '...' : `${stats?.average_risk_score ?? 0} / 100`}
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              Weighted risk score computed across all evaluated postings
            </p>
          </div>
          <button onClick={() => setActivePage('about')} className="btn btn-secondary btn-sm">
            <span>ML Specs</span>
            <ArrowRight size={13} />
          </button>
        </div>
      </div>

      {/* Recent Checks Table */}
      <div className="card">
        <div className="card-header">
          <div>
            <h2 className="card-title">Recent Authenticity Audits</h2>
            <p className="card-subtitle">Last postings scanned by the detection pipeline</p>
          </div>
          <button onClick={() => setActivePage('history')} className="btn btn-secondary btn-sm">
            <span>View Full History</span>
            <ArrowRight size={13} />
          </button>
        </div>

        {loading ? (
          <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            Loading recent checks from database...
          </div>
        ) : stats?.recent_checks?.length === 0 ? (
          <div style={{ padding: '2.5rem', textAlign: 'center', color: 'var(--text-muted)' }}>
            <p>No audit scans recorded yet.</p>
            <button onClick={() => setActivePage('analyze')} className="btn btn-primary btn-sm" style={{ marginTop: '1rem' }}>
              Run First Analysis
            </button>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Job Title</th>
                  <th>Company</th>
                  <th>Status</th>
                  <th>Risk Score</th>
                  <th>Verified Apply</th>
                  <th>Audited At</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {stats?.recent_checks?.map((check) => (
                  <tr key={check.id}>
                    <td style={{ fontWeight: 600, color: '#fff' }}>
                      {check.job_title}
                    </td>
                    <td>{check.company_name}</td>
                    <td>
                      <RiskBadge classification={check.classification} size="sm" />
                    </td>
                    <td>
                      <span style={{
                        fontFamily: 'var(--font-mono)',
                        fontWeight: 700,
                        color: check.risk_score >= 70 ? '#ef4444' : check.risk_score >= 35 ? '#f59e0b' : '#10b981'
                      }}>
                        {check.risk_score} / 100
                      </span>
                    </td>
                    <td>
                      {check.vacancy_verified ? (
                        <span style={{ color: '#10b981', fontSize: '0.8rem', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '3px' }}>
                          ✔️ Enabled
                        </span>
                      ) : (
                        <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                          — Blocked
                        </span>
                      )}
                    </td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      {check.created_at ? new Date(check.created_at).toLocaleDateString() : '—'}
                    </td>
                    <td>
                      <button
                        onClick={() => handleViewReport(check.id)}
                        className="btn btn-secondary btn-sm"
                        style={{ padding: '0.3rem 0.6rem', fontSize: '0.75rem' }}
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
