import React, { useState, useEffect } from 'react';
import { FileSearch, Globe, FileText, AlertCircle, RefreshCw, ArrowRight, Sparkles, Building, Briefcase, CheckCircle2, AlertOctagon } from 'lucide-react';
import { api } from '../services/api';
import ErrorAlert from '../components/ErrorAlert';

export default function AnalyzePage({ setActivePage, setLatestAnalysis, preloadedAnalysis }) {
  const [activeTab, setActiveTab] = useState('url'); // 'url' or 'manual'
  const [jobUrl, setJobUrl] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [jobDescription, setJobDescription] = useState('');

  const [loading, setLoading] = useState(false);
  const [extracting, setExtracting] = useState(false);
  const [error, setError] = useState(null);
  const [extractSuccess, setExtractSuccess] = useState(null);

  // Sync preloaded data if passed from LandingPage or JobSearch
  useEffect(() => {
    if (preloadedAnalysis) {
      if (preloadedAnalysis.job_url) {
        setJobUrl(preloadedAnalysis.job_url);
        setActiveTab('url');
      } else {
        setActiveTab('manual');
      }
      setJobTitle(preloadedAnalysis.job_title || '');
      setCompanyName(preloadedAnalysis.company_name || '');
      setJobDescription(preloadedAnalysis.job_description || '');
    }
  }, [preloadedAnalysis]);

  // Safe Metadata Extraction via backend SSRF guard
  const handleExtractUrl = async () => {
    if (!jobUrl.trim()) {
      setError('Please enter a valid job URL first.');
      return;
    }
    setError(null);
    setExtractSuccess(null);
    setExtracting(true);

    try {
      const data = await api.extractJobUrl(jobUrl.trim());
      if (data.title && !jobTitle) setJobTitle(data.title);
      if (data.company && !companyName) setCompanyName(data.company);
      if (data.description && !jobDescription) setJobDescription(data.description);
      setExtractSuccess(`Successfully extracted title, company, and description from ${data.source_domain}`);
    } catch (err) {
      setError(`Safe URL Extraction Note: ${err.message}. You may enter or edit details manually below.`);
    } finally {
      setExtracting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const trimmedDesc = jobDescription.trim();
    const trimmedUrl = jobUrl.trim();

    if (!trimmedDesc && !trimmedUrl) {
      setError('Please provide either a valid Job Posting URL or a Job Description text to evaluate.');
      return;
    }

    setLoading(true);
    try {
      const response = await api.analyzeJob({
        job_title: jobTitle.trim(),
        company_name: companyName.trim(),
        job_description: trimmedDesc,
        job_url: trimmedUrl || null,
      });

      setLatestAnalysis(response);
      setActivePage('detail');
    } catch (err) {
      setError(err.message || 'Analysis failed. Please check inputs and try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (type) => {
    setError(null);
    setExtractSuccess(null);
    if (type === 'google') {
      setActiveTab('url');
      setJobUrl('https://careers.google.com/jobs/results/94823');
      setJobTitle('Staff Systems Software Engineer');
      setCompanyName('Google');
      setJobDescription('Google is seeking a Staff Systems Software Engineer to build distributed runtime platforms for planetary-scale computing. Requirements: BS/MS in Computer Science, 8+ years experience with distributed systems in Go or C++, deep Linux kernel familiarity, and system performance profiling.');
    } else if (type === 'telegram_scam') {
      setActiveTab('manual');
      setJobUrl('');
      setJobTitle('Data Entry Specialist - Immediate Hire ($45/hr)');
      setCompanyName('Global Remote Apex');
      setJobDescription('URGENT OPENING: We are hiring remote data entry assistants! Work 15 hours a week and earn $45/hour. No interview needed and immediate start today! Candidates are sent an upfront equipment cashier check of $3,500 to purchase a company laptop. You will deposit the check and wire transfer the excess funds back. Text our HR manager on Telegram at @apex_onboarding.');
    } else if (type === 'lookalike_phish') {
      setActiveTab('url');
      setJobUrl('https://microsoft-career-portal.xyz/apply');
      setJobTitle('Executive Administrative Assistant');
      setCompanyName('Microsoft');
      setJobDescription('Microsoft Corporation is hiring an Executive Administrative Assistant to support our corporate operations. Flexible work from home arrangement with complete medical benefits. Submit your application through our online form.');
    }
  };

  const handleClear = () => {
    setJobUrl('');
    setJobTitle('');
    setCompanyName('');
    setJobDescription('');
    setError(null);
    setExtractSuccess(null);
  };

  return (
    <div style={{ maxWidth: '840px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff' }}>Analyze Job Posting</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          Scan job advertisements for scam signatures, extortion patterns, and verify corporate domain authenticity.
        </p>
      </div>

      {/* Preset Test Scenarios */}
      <div className="card" style={{ padding: '1rem 1.25rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            Load Test Scenarios:
          </span>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            <button type="button" onClick={() => loadPreset('google')} className="btn btn-secondary btn-sm">
              <CheckCircle2 size={13} color="#10b981" /> Verified Google
            </button>
            <button type="button" onClick={() => loadPreset('telegram_scam')} className="btn btn-secondary btn-sm">
              <AlertOctagon size={13} color="#ef4444" /> Advance Fee Telegram Scam
            </button>
            <button type="button" onClick={() => loadPreset('lookalike_phish')} className="btn btn-secondary btn-sm">
              <AlertOctagon size={13} color="#f59e0b" /> Lookalike Phishing URL
            </button>
          </div>
        </div>
      </div>

      <ErrorAlert message={error} />

      {extractSuccess && (
        <div className="alert alert-success">
          <CheckCircle2 size={16} />
          <span>{extractSuccess}</span>
        </div>
      )}

      {/* Main Analysis Form */}
      <form onSubmit={handleSubmit} className="card">
        {/* Tab Switcher */}
        <div style={{ display: 'flex', borderBottom: '1px solid var(--border-subtle)', marginBottom: '1.5rem' }}>
          <button
            type="button"
            onClick={() => setActiveTab('url')}
            style={{
              padding: '0.75rem 1.25rem',
              fontWeight: 600,
              fontSize: '0.9rem',
              color: activeTab === 'url' ? '#3b82f6' : 'var(--text-secondary)',
              borderBottom: activeTab === 'url' ? '2px solid #3b82f6' : 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <Globe size={16} />
            <span>Job URL Submission</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('manual')}
            style={{
              padding: '0.75rem 1.25rem',
              fontWeight: 600,
              fontSize: '0.9rem',
              color: activeTab === 'manual' ? '#3b82f6' : 'var(--text-secondary)',
              borderBottom: activeTab === 'manual' ? '2px solid #3b82f6' : 'none',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}
          >
            <FileText size={16} />
            <span>Manual Text Input</span>
          </button>
        </div>

        {/* URL Input (if URL tab) */}
        {activeTab === 'url' && (
          <div className="form-group">
            <label className="form-label">Job Posting URL</label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="url"
                value={jobUrl}
                onChange={(e) => setJobUrl(e.target.value)}
                placeholder="https://example.com/careers/job-12345"
                className="form-input"
              />
              <button
                type="button"
                onClick={handleExtractUrl}
                disabled={extracting || !jobUrl}
                className="btn btn-secondary"
                style={{ flexShrink: 0 }}
                title="Extract job title, company, and description safely"
              >
                {extracting ? <RefreshCw size={14} className="spin" /> : <Globe size={14} />}
                <span>Auto-Fetch</span>
              </button>
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.35rem' }}>
              Protected with SSRF safeguards, content size restrictions, and domain reputation checks.
            </p>
          </div>
        )}

        {/* Optional Title & Company */}
        <div className="grid-2">
          <div className="form-group">
            <label className="form-label">Job Title (Optional)</label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Software Engineer"
                className="form-input"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Claimed Company Name (Optional)</label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="e.g. Google, Amazon, Microsoft"
                className="form-input"
              />
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.35rem' }}>
                If left blank, the system tries to detect a known company name from the job description. A name mention does not verify the employer or vacancy.
              </p>
            </div>
          </div>
        </div>

        {/* Job Description */}
        <div className="form-group">
          <label className="form-label">
            Job Description & Posting Details {activeTab === 'manual' ? '(Required)' : '(Optional if URL provided)'}
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the full job posting text here, including requirements, company profile, and application instructions..."
            className="form-textarea"
            rows={7}
          />
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.35rem' }}>
            The AI engine evaluates requirements, compensation claims, contact instructions, and structural signals.
          </p>
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '1.5rem', flexWrap: 'wrap', gap: '0.75rem' }}>
          <button type="button" onClick={handleClear} className="btn btn-secondary btn-sm">
            Clear Form
          </button>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ minWidth: '180px' }}
          >
            {loading ? (
              <>
                <RefreshCw size={16} className="spin" />
                <span>Running AI Audit...</span>
              </>
            ) : (
              <>
                <span>Evaluate Authenticity</span>
                <ArrowRight size={16} />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
