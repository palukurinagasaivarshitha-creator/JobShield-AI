import React, { useState, useEffect } from 'react';
import { History, Search, Trash2, ExternalLink, RefreshCw, Eye, AlertOctagon } from 'lucide-react';
import { api } from '../services/api';
import RiskBadge from '../components/RiskBadge';
import VerificationBadge from '../components/VerificationBadge';
import ErrorAlert from '../components/ErrorAlert';

export default function HistoryPage({ setActivePage, setSelectedAnalysisId }) {
  const [history, setHistory] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterClass, setFilterClass] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getHistory(searchQuery, filterClass, 50, 0);
      setHistory(data);
    } catch (err) {
      setError(err.message || 'Failed to load audit history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, [filterClass]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchHistory();
  };

  const handleInspect = (id) => {
    setSelectedAnalysisId(id);
    setActivePage('detail');
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Are you sure you want to remove this scan record from database history?')) {
      return;
    }
    try {
      await api.deleteHistory(id);
      setHistory(history.filter((item) => item.id !== id));
    } catch (err) {
      alert(`Delete failed: ${err.message}`);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff' }}>Persistent Audit History</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Historical records of evaluated job postings stored in PostgreSQL / SQLite database with multi-vector forensics.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="card" style={{ padding: '1rem 1.25rem' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '240px' }}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search history by job title or company..."
              className="form-input"
            />
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={() => setFilterClass('')}
              className={`btn btn-sm ${filterClass === '' ? 'btn-primary' : 'btn-secondary'}`}
            >
              All Records
            </button>
            <button
              type="button"
              onClick={() => setFilterClass('SAFE')}
              className={`btn btn-sm ${filterClass === 'SAFE' ? 'btn-success' : 'btn-secondary'}`}
            >
              Safe
            </button>
            <button
              type="button"
              onClick={() => setFilterClass('SUSPICIOUS')}
              className={`btn btn-sm ${filterClass === 'SUSPICIOUS' ? 'btn-secondary' : 'btn-secondary'}`}
              style={{ color: filterClass === 'SUSPICIOUS' ? '#f59e0b' : 'inherit' }}
            >
              Suspicious
            </button>
            <button
              type="button"
              onClick={() => setFilterClass('HIGH_RISK')}
              className={`btn btn-sm ${filterClass === 'HIGH_RISK' ? 'btn-danger' : 'btn-secondary'}`}
            >
              High Risk
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              <Search size={14} />
              <span>Filter</span>
            </button>
          </div>
        </form>
      </div>

      <ErrorAlert message={error} onRetry={fetchHistory} />

      {/* History Table */}
      <div className="card">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
            <RefreshCw size={24} className="spin" style={{ margin: '0 auto 0.75rem' }} />
            <p>Loading database audit logs...</p>
          </div>
        ) : history.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
            <History size={36} color="#64748b" style={{ margin: '0 auto 1rem' }} />
            <h3 style={{ color: '#fff', fontSize: '1.15rem' }}>No history records found</h3>
            <p style={{ fontSize: '0.85rem', marginTop: '0.25rem' }}>
              Run a job analysis to populate persistent verification logs.
            </p>
            <button onClick={() => setActivePage('analyze')} className="btn btn-primary btn-sm" style={{ marginTop: '1rem' }}>
              Run Analysis Scan
            </button>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Audit ID</th>
                  <th>Job Title</th>
                  <th>Company</th>
                  <th>Threat Status</th>
                  <th>Risk Score</th>
                  <th>Domain Check</th>
                  <th>Scanned Date</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {history.map((record) => (
                  <tr
                    key={record.id}
                    onClick={() => handleInspect(record.id)}
                    style={{ cursor: 'pointer' }}
                  >
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      #{record.id}
                    </td>
                    <td style={{ fontWeight: 600, color: '#fff' }}>
                      {record.job_title}
                    </td>
                    <td>{record.company_name}</td>
                    <td>
                      <RiskBadge classification={record.classification} size="sm" />
                    </td>
                    <td>
                      <span style={{
                        fontFamily: 'var(--font-mono)',
                        fontWeight: 700,
                        color: record.risk_score >= 70 ? '#ef4444' : record.risk_score >= 35 ? '#f59e0b' : '#10b981'
                      }}>
                        {record.risk_score} / 100
                      </span>
                    </td>
                    <td>
                      <VerificationBadge status={record.verification?.status} domain={record.verification?.official_domain} />
                    </td>
                    <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      {record.timestamp ? new Date(record.timestamp).toLocaleDateString() : '—'}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.35rem' }} onClick={(e) => e.stopPropagation()}>
                        <button
                          onClick={() => handleInspect(record.id)}
                          className="btn btn-secondary btn-sm"
                          title="Inspect complete threat breakdown"
                        >
                          <Eye size={13} />
                        </button>
                        <button
                          onClick={(e) => handleDelete(record.id, e)}
                          className="btn btn-secondary btn-sm"
                          style={{ color: '#ef4444' }}
                          title="Delete audit record"
                        >
                          <Trash2 size={13} />
                        </button>
                      </div>
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
