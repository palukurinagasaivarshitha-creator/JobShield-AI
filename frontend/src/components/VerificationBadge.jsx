import React from 'react';
import { CheckCircle2, AlertOctagon, AlertTriangle, HelpCircle } from 'lucide-react';

export default function VerificationBadge({ status = 'INCONCLUSIVE', domain = '' }) {
  const norm = (status || '').toUpperCase();

  if (norm === 'VERIFIED') {
    return (
      <span className="badge badge-verified" title={domain ? `Verified domain: ${domain}` : 'Verified Employer'}>
        <CheckCircle2 size={13} />
        <span>Verified Corporate Domain</span>
      </span>
    );
  }

  if (norm === 'MISMATCH') {
    return (
      <span className="badge badge-mismatch" title="Job URL does not match claimed employer's official domain">
        <AlertOctagon size={13} />
        <span>Domain Mismatch Warning</span>
      </span>
    );
  }

  if (norm === 'UNVERIFIED') {
    return (
      <span className="badge badge-suspicious" title="Company domain not verified by authoritative source">
        <AlertTriangle size={13} />
        <span>Unverified Employer</span>
      </span>
    );
  }

  return (
    <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.08)', color: '#94a3b8' }}>
      <HelpCircle size={13} />
      <span>Domain Inconclusive</span>
    </span>
  );
}
