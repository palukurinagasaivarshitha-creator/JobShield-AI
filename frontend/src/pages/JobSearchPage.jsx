import React, { useState, useEffect } from 'react';
import { Search, Filter, RefreshCw, Briefcase, AlertCircle, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';
import JobCard from '../components/JobCard';
import ErrorAlert from '../components/ErrorAlert';

export default function JobSearchPage({ setActivePage, setPreloadedAnalysis }) {
  const [jobs, setJobs] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedFilter, setSelectedFilter] = useState(''); // '', 'SAFE', 'SUSPICIOUS', 'HIGH_RISK'
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchJobs = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.searchJobs(searchQuery, selectedFilter, 20, 0);
      setJobs(data);
    } catch (err) {
      setError(err.message || 'Failed to fetch job postings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, [selectedFilter]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchJobs();
  };

  const handleAnalyzeJob = (job) => {
    setPreloadedAnalysis({
      job_title: job.title,
      company_name: job.company,
      job_description: `${job.description}\n\nRequirements:\n${job.requirements || ''}`,
      job_url: job.official_apply_url || '',
    });
    setActivePage('analyze');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff' }}>Verified Jobs & Scam Test Feed</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Explore documented genuine opportunities with verified official career application links alongside cataloged fraud signatures.
        </p>
      </div>

      {/* Search and Filters Bar */}
      <div className="card" style={{ padding: '1rem 1.25rem' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: '240px', position: 'relative' }}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by job title, company, or keywords..."
              className="form-input"
            />
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button
              type="button"
              onClick={() => setSelectedFilter('')}
              className={`btn btn-sm ${selectedFilter === '' ? 'btn-primary' : 'btn-secondary'}`}
            >
              All Categories
            </button>
            <button
              type="button"
              onClick={() => setSelectedFilter('SAFE')}
              className={`btn btn-sm ${selectedFilter === 'SAFE' ? 'btn-success' : 'btn-secondary'}`}
            >
              Verified Safe
            </button>
            <button
              type="button"
              onClick={() => setSelectedFilter('HIGH_RISK')}
              className={`btn btn-sm ${selectedFilter === 'HIGH_RISK' ? 'btn-danger' : 'btn-secondary'}`}
            >
              High Risk Scams
            </button>
            <button type="submit" className="btn btn-primary btn-sm">
              <Search size={14} />
              <span>Search</span>
            </button>
          </div>
        </form>
      </div>

      <ErrorAlert message={error} onRetry={fetchJobs} />

      {/* Job Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
          <RefreshCw size={24} className="spin" style={{ margin: '0 auto 0.75rem' }} />
          <p>Filtering documented vacancy records...</p>
        </div>
      ) : jobs.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <Briefcase size={36} color="#64748b" style={{ margin: '0 auto 1rem' }} />
          <h3 style={{ color: '#fff', fontSize: '1.15rem' }}>No matching listings found</h3>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
            Try adjusting your search keywords or clear your classification filter.
          </p>
          <button
            onClick={() => {
              setSearchQuery('');
              setSelectedFilter('');
            }}
            className="btn btn-secondary btn-sm"
            style={{ marginTop: '1rem' }}
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid-2">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} onAnalyze={handleAnalyzeJob} />
          ))}
        </div>
      )}
    </div>
  );
}
