import React, { useState } from 'react';
import { ShieldCheck, ShieldAlert, ArrowRight, Zap, CheckCircle2, Lock, Search, Sparkles, AlertOctagon, HelpCircle } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';

export default function LandingPage({ setActivePage, setPreloadedAnalysis }) {
  const [quickInput, setQuickInput] = useState('');

  const handleQuickSubmit = (e) => {
    e.preventDefault();
    if (!quickInput.trim()) return;

    const isUrl = quickInput.startsWith('http://') || quickInput.startsWith('https://');
    setPreloadedAnalysis({
      job_title: '',
      company_name: '',
      job_description: isUrl ? '' : quickInput,
      job_url: isUrl ? quickInput : '',
    });
    setActivePage('analyze');
  };

  const handleDemoPreset = (presetType) => {
    if (presetType === 'safe') {
      setPreloadedAnalysis({
        job_title: 'Senior Cloud Backend Engineer',
        company_name: 'Google',
        job_description: 'We are seeking a Senior Cloud Backend Engineer to join our infrastructure team in Sunnyvale. Responsible for building scalable microservices in Python and Go, optimizing distributed storage systems, and collaborating with cross-functional architects. Minimum 5 years software development experience with distributed systems and a BS in Computer Science or equivalent practical experience.',
        job_url: 'https://careers.google.com/jobs/results/12345'
      });
    } else if (presetType === 'scam') {
      setPreloadedAnalysis({
        job_title: 'Remote Data Entry Clerk ($55/hr)',
        company_name: 'Fast Track Logistics',
        job_description: 'URGENT HIRING: Remote Data Entry Clerk needed immediately! No interview needed and no experience required. Earn $55 per hour working from home. Candidates will receive an upfront check of $2,500 to purchase home office equipment. You must deposit the check and wire transfer the remaining balance. Text our hiring manager on Telegram at @fasttrack_jobs immediately.',
        job_url: ''
      });
    } else {
      setPreloadedAnalysis({
        job_title: 'Executive Assistant to VP',
        company_name: 'Microsoft',
        job_description: 'Microsoft is hiring an Executive Assistant to assist our leadership. Work from home with full medical benefits.',
        job_url: 'https://microsoft-career-portal.xyz/apply'
      });
    }
    setActivePage('analyze');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '3.5rem' }}>
      {/* Hero Section */}
      <section style={{ textAlign: 'center', padding: '2.5rem 1rem 1rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '8px',
          padding: '6px 14px',
          borderRadius: '999px',
          background: 'rgba(59, 130, 246, 0.1)',
          border: '1px solid rgba(59, 130, 246, 0.25)',
          color: '#60a5fa',
          fontSize: '0.85rem',
          fontWeight: 600,
          marginBottom: '1.25rem'
        }}>
          <Sparkles size={15} />
          <span>AI-Powered Recruitment Threat Intelligence</span>
        </div>

        <h1 style={{
          fontSize: 'clamp(2.2rem, 5vw, 3.4rem)',
          fontWeight: 800,
          lineHeight: 1.15,
          letterSpacing: '-0.03em',
          maxWidth: '850px',
          margin: '0 auto 1.25rem',
          color: '#fff'
        }}>
          Verify Any Job Vacancy Before You Apply
        </h1>

        <p style={{
          fontSize: 'clamp(1rem, 2vw, 1.15rem)',
          color: 'var(--text-secondary)',
          maxWidth: '680px',
          margin: '0 auto 2.5rem',
          lineHeight: 1.6
        }}>
          Protect yourself against fake employment scams, phishing portals, upfront fee extortion, and impersonated employers. Powered by the <strong>EMSCAD dataset</strong>, heuristic threat signatures, and authoritative domain corroboration.
        </p>

        {/* Quick Check Form */}
        <form
          onSubmit={handleQuickSubmit}
          style={{
            maxWidth: '640px',
            margin: '0 auto 2rem',
            display: 'flex',
            gap: '0.5rem',
            background: 'var(--bg-card)',
            padding: '0.5rem',
            borderRadius: 'var(--radius-lg)',
            border: '1px solid var(--border-medium)',
            boxShadow: 'var(--shadow-lg)'
          }}
        >
          <input
            type="text"
            value={quickInput}
            onChange={(e) => setQuickInput(e.target.value)}
            placeholder="Paste job posting URL or job description text..."
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              padding: '0.75rem 1rem',
              color: '#fff',
              fontSize: '0.95rem',
              outline: 'none'
            }}
          />
          <button type="submit" className="btn btn-primary" style={{ flexShrink: 0 }}>
            <span>Scan Posting</span>
            <ArrowRight size={16} />
          </button>
        </form>

        {/* One-Click Demo Presets */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flexWrap: 'wrap', gap: '0.75rem', fontSize: '0.85rem' }}>
          <span style={{ color: 'var(--text-muted)' }}>Try instant live demo:</span>
          <button
            onClick={() => handleDemoPreset('safe')}
            className="btn btn-secondary btn-sm"
            style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
          >
            <CheckCircle2 size={13} color="#10b981" /> Verified Google Role
          </button>
          <button
            onClick={() => handleDemoPreset('scam')}
            className="btn btn-secondary btn-sm"
            style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
          >
            <AlertOctagon size={13} color="#ef4444" /> Telegram Advance-Fee Scam
          </button>
          <button
            onClick={() => handleDemoPreset('phish')}
            className="btn btn-secondary btn-sm"
            style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
          >
            <AlertOctagon size={13} color="#f59e0b" /> Lookalike Domain Phishing
          </button>
        </div>
      </section>

      {/* Feature Pillars */}
      <section className="grid-3">
        <div className="card">
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(59, 130, 246, 0.12)',
            color: '#3b82f6',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem'
          }}>
            <Zap size={22} />
          </div>
          <h3 className="card-title">EMSCAD Machine Learning</h3>
          <p className="card-subtitle" style={{ fontSize: '0.9rem', lineHeight: 1.6, marginTop: '0.5rem' }}>
            Trained on verified ground-truth employment fraud cases from the University of the Aegean EMSCAD repository. Detects deceptive lexical patterns and subtle vocabulary red flags.
          </p>
        </div>

        <div className="card">
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(239, 68, 68, 0.12)',
            color: '#ef4444',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem'
          }}>
            <ShieldAlert size={22} />
          </div>
          <h3 className="card-title">Multi-Threat Heuristic Engine</h3>
          <p className="card-subtitle" style={{ fontSize: '0.9rem', lineHeight: 1.6, marginTop: '0.5rem' }}>
            Deterministic pattern matching catches wire transfer extortion, upfront registration fees, fake equipment checks, and recruiters attempting to conduct interviews on Telegram or WhatsApp.
          </p>
        </div>

        <div className="card">
          <div style={{
            width: '42px',
            height: '42px',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(16, 185, 129, 0.12)',
            color: '#10b981',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '1rem'
          }}>
            <Lock size={22} />
          </div>
          <h3 className="card-title">Official Domain & Apply Portal</h3>
          <p className="card-subtitle" style={{ fontSize: '0.9rem', lineHeight: 1.6, marginTop: '0.5rem' }}>
            Performs DNS and corporate registry checks to confirm that the job posting link belongs to the genuine employer. Directly connects you to verified official careers application pages.
          </p>
        </div>
      </section>

      {/* Comparison Grid */}
      <section className="card" style={{ padding: '2rem' }}>
        <h2 style={{ fontSize: '1.4rem', fontWeight: 800, marginBottom: '0.5rem', color: '#fff', textAlign: 'center' }}>
          How JobShield Protects Your Career Search
        </h2>
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '2rem', fontSize: '0.95rem' }}>
          Distinguishing legitimate corporate vacancies from sophisticated recruitment fraud
        </p>

        <div className="grid-2">
          <div style={{ background: 'var(--bg-secondary)', padding: '1.5rem', borderRadius: 'var(--radius-md)', border: '1px solid rgba(239, 68, 68, 0.2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#ef4444', fontWeight: 700, marginBottom: '0.75rem' }}>
              <AlertOctagon size={18} />
              <span>Hallmarks of a Fake Job Posting</span>
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              <li>❌ Demands $50–$300 for background checks, onboarding or equipment</li>
              <li>❌ Recruiter conducts interview purely through text on Telegram</li>
              <li>❌ Promises $5,000/week for basic entry-level or data entry duties</li>
              <li>❌ Offers instant hiring on the spot with zero technical evaluation</li>
              <li>❌ Hosted on lookalike domains (e.g. <code>microsoft-careers-portal.xyz</code>)</li>
            </ul>
          </div>

          <div style={{ background: 'var(--bg-secondary)', padding: '1.5rem', borderRadius: 'var(--radius-md)', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#10b981', fontWeight: 700, marginBottom: '0.75rem' }}>
              <CheckCircle2 size={18} />
              <span>Verified Legitimate Hiring Standards</span>
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.6rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
              <li>✔️ Employer provides all necessary hardware and onboarding materials free</li>
              <li>✔️ Formal interviews conducted over verified enterprise video platforms</li>
              <li>✔️ Realistic compensation indexed to verified industry market standards</li>
              <li>✔️ Applications routed directly through verified ATS or official domain</li>
              <li>✔️ Direct "Apply on Official Website" corroboration enabled</li>
            </ul>
          </div>
        </div>

        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button onClick={() => setActivePage('analyze')} className="btn btn-primary">
            <span>Launch In-Depth Job Scanner</span>
            <ArrowRight size={16} />
          </button>
        </div>
      </section>
    </div>
  );
}
