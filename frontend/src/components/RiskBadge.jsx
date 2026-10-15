import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon } from 'lucide-react';

export default function RiskBadge({ classification, size = 'md' }) {
  const norm = (classification || '').toUpperCase();

  let badgeClass = 'badge-safe';
  let label = 'SAFE';
  let Icon = ShieldCheck;

  if (norm === 'HIGH_RISK' || norm === 'HIGH RISK' || norm === 'HIGH') {
    badgeClass = 'badge-high-risk';
    label = 'HIGH RISK';
    Icon = AlertOctagon;
  } else if (norm === 'SUSPICIOUS' || norm === 'MODERATE') {
    badgeClass = 'badge-suspicious';
    label = 'SUSPICIOUS';
    Icon = AlertTriangle;
  }

  const iconSizes = { sm: 12, md: 14, lg: 16 };
  const iconSize = iconSizes[size] || 14;

  return (
    <span className={`badge ${badgeClass}`}>
      <Icon size={iconSize} />
      <span>{label}</span>
    </span>
  );
}
