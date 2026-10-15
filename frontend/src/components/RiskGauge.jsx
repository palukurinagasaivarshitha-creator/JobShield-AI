import React from 'react';

export default function RiskGauge({ score = 0, classification = 'SAFE' }) {
  const clamped = Math.max(0, Math.min(100, Math.round(score)));

  let strokeColor = '#10b981'; // safe
  let bgColor = 'rgba(16, 185, 129, 0.15)';
  let label = 'Low Risk';

  if (clamped >= 70) {
    strokeColor = '#ef4444'; // high risk
    bgColor = 'rgba(239, 68, 68, 0.15)';
    label = 'Severe Scam Threat';
  } else if (clamped >= 35) {
    strokeColor = '#f59e0b'; // suspicious
    bgColor = 'rgba(245, 158, 11, 0.15)';
    label = 'Moderate Caution';
  }

  // SVG Gauge calculations
  const radius = 58;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (clamped / 100) * circumference;

  return (
    <div className="gauge-container">
      <div style={{ position: 'relative', width: '150px', height: '150px' }}>
        <svg width="150" height="150" style={{ transform: 'rotate(-90deg)' }}>
          {/* Background Track */}
          <circle
            cx="75"
            cy="75"
            r={radius}
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="10"
            fill="transparent"
          />
          {/* Animated Value Arc */}
          <circle
            cx="75"
            cy="75"
            r={radius}
            stroke={strokeColor}
            strokeWidth="10"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            fill="transparent"
            style={{ transition: 'stroke-dashoffset 0.8s ease, stroke 0.4s ease' }}
          />
        </svg>

        {/* Center Text */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <span style={{ fontSize: '2rem', fontWeight: 800, color: strokeColor, lineHeight: 1 }}>
            {clamped}
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>
            / 100
          </span>
        </div>
      </div>

      <div style={{ textAlign: 'center', marginTop: '0.75rem' }}>
        <div style={{ fontWeight: 700, fontSize: '1rem', color: strokeColor }}>
          {classification.replace('_', ' ')}
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
          Threat Index: {label}
        </div>
      </div>
    </div>
  );
}
