import React from 'react';
import { Database, Cpu, Shield, Lock, ExternalLink, BookOpen, Layers, CheckCircle2 } from 'lucide-react';

export default function AboutPage() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2.5rem', maxWidth: '900px', margin: '0 auto' }}>
      <div>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#fff' }}>
          System Architecture & Scientific Documentation
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', marginTop: '0.25rem' }}>
          Technical documentation of datasets, machine learning methodologies, heuristic threat signatures, and safety guarantees.
        </p>
      </div>

      {/* Dataset Section */}
      <section className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
          <Database size={22} color="#3b82f6" />
          <h2 className="card-title">1. Employment Scam Aegean Dataset (EMSCAD)</h2>
        </div>

        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1rem' }}>
          The machine learning core uses the <strong>Employment Scam Aegean Dataset (EMSCAD)</strong>, published by the University of the Aegean Information & Communication Systems Security (ICCS) laboratory.
        </p>

        <div style={{ background: 'var(--bg-secondary)', padding: '1rem 1.25rem', borderRadius: 'var(--radius-md)', marginBottom: '1.25rem', borderLeft: '4px solid #3b82f6' }}>
          <p style={{ fontSize: '0.85rem', color: '#e2e8f0', fontFamily: 'var(--font-mono)' }}>
            Vidros, S., Kolias, C., Kambourakis, G., & Akoglu, L. (2017). Automatic Detection of Online Recruitment Frauds: Characteristics, Methods, and a Public Dataset. Future Internet, 9(1), 6. DOI: 10.3390/fi9010006.
          </p>
        </div>

        <div className="grid-2" style={{ gap: '1rem', fontSize: '0.85rem' }}>
          <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-sm)' }}>
            <span style={{ fontWeight: 700, color: '#fff' }}>Dataset Scope & Imbalance</span>
            <ul style={{ listStyle: 'none', marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '4px', color: 'var(--text-secondary)' }}>
              <li>• Total Postings: <strong>17,880</strong></li>
              <li>• Legitimate Postings: <strong>17,014</strong> (~95.16%)</li>
              <li>• Fraudulent Postings: <strong>866</strong> (~4.84%)</li>
              <li>• Licence: <strong>Creative Commons CC BY 4.0</strong></li>
            </ul>
          </div>

          <div style={{ background: 'var(--bg-secondary)', padding: '1rem', borderRadius: 'var(--radius-sm)' }}>
            <span style={{ fontWeight: 700, color: '#fff' }}>Features Processed</span>
            <ul style={{ listStyle: 'none', marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '4px', color: 'var(--text-secondary)' }}>
              <li>• <code>title</code> + <code>company_profile</code></li>
              <li>• <code>description</code> + <code>requirements</code></li>
              <li>• <code>salary_range</code> + <code>telecommuting</code></li>
              <li>• <code>employment_type</code> + <code>has_company_logo</code></li>
            </ul>
          </div>
        </div>
      </section>

      {/* ML Pipeline & Leakage Prevention */}
      <section className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
          <Cpu size={22} color="#10b981" />
          <h2 className="card-title">2. ML Pipeline & Data Leakage Prevention</h2>
        </div>

        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1rem' }}>
          To guarantee rigorous experimental validity and real-world generalizability:
        </p>

        <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem', fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
          <li style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
            <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
            <span>
              <strong style={{ color: '#fff' }}>Strict Stratified Train-Test Splitting:</strong> The 80/20 train/test split maintains exact class proportions. Vocabulary extraction and IDF weight calculation are performed strictly on the training partition.
            </span>
          </li>
          <li style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
            <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
            <span>
              <strong style={{ color: '#fff' }}>TF-IDF Vectorization:</strong> Extracts 5,000 sublinearly scaled unigrams and bigrams, filtering English stop-words and rare noise tokens.
            </span>
          </li>
          <li style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
            <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
            <span>
              <strong style={{ color: '#fff' }}>Cost-Sensitive Calibrated Classification:</strong> Utilizes <code>class_weight='balanced'</code> to penalize false negatives proportionally to the ~5% minority fraud prevalence, outputting calibrated probability estimates.
            </span>
          </li>
          <li style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
            <CheckCircle2 size={16} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
            <span>
              <strong style={{ color: '#fff' }}>Deterministic Fallback Mode:</strong> If serialized models are absent, the engine activates deterministic heuristic scoring, clearly labeled via <code>is_fallback: true</code>.
            </span>
          </li>
        </ul>
      </section>

      {/* Security & SSRF Protection */}
      <section className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '1rem' }}>
          <Lock size={22} color="#f59e0b" />
          <h2 className="card-title">3. Scraping Safeguards & SSRF Mitigation</h2>
        </div>

        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginBottom: '1rem' }}>
          When ingesting external job links, the platform enforces strict security boundaries:
        </p>

        <div style={{ background: 'var(--bg-secondary)', padding: '1rem 1.25rem', borderRadius: 'var(--radius-md)', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '6px' }}>
            <li>🔒 <strong>Private IP Blocking:</strong> Disallows <code>127.0.0.0/8</code>, <code>10.0.0.0/8</code>, <code>172.16.0.0/12</code>, <code>192.168.0.0/16</code>, and cloud metadata (<code>169.254.169.254</code>).</li>
            <li>🔒 <strong>Protocol Restriction:</strong> Only <code>http://</code> and <code>https://</code> schemes are permitted; file, ftp, and internal schemes are rejected.</li>
            <li>🔒 <strong>Payload Caps:</strong> Enforces an 8-second timeout and 2 MB content length cap to prevent resource exhaustion.</li>
            <li>🔒 <strong>DOM Sanitization:</strong> Strips scripts, styles, and hidden event handlers prior to parsing.</li>
          </ul>
        </div>
      </section>

      {/* API Documentation */}
      <section className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h3 className="card-title" style={{ fontSize: '1.1rem' }}>FastAPI Swagger & OpenAPI Docs</h3>
          <p className="card-subtitle">
            Explore interactive API endpoints, request schemas, and responses in Swagger UI.
          </p>
        </div>
        <a
          href="/docs"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-primary"
        >
          <span>Open Swagger UI</span>
          <ExternalLink size={15} />
        </a>
      </section>
    </div>
  );
}
