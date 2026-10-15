import React, { useState, useEffect } from 'react';
import { Shield, LayoutDashboard, Search, FileSearch, History, Info, Menu, X, CheckCircle2 } from 'lucide-react';
import { api } from '../services/api';

export default function Navbar({ activePage, setActivePage }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [systemOnline, setSystemOnline] = useState(false);

  useEffect(() => {
    api.getHealth()
      .then((data) => {
        if (data.status === 'healthy') setSystemOnline(true);
      })
      .catch(() => setSystemOnline(false));
  }, []);

  const navItems = [
    { id: 'landing', label: 'Home', icon: Shield },
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'analyze', label: 'Analyze Job', icon: FileSearch },
    { id: 'search', label: 'Job Search', icon: Search },
    { id: 'history', label: 'Audit History', icon: History },
    { id: 'about', label: 'ML & Docs', icon: Info },
  ];

  const handleNavClick = (id) => {
    setActivePage(id);
    setMobileMenuOpen(false);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <div className="nav-brand" onClick={() => handleNavClick('landing')} style={{ cursor: 'pointer' }}>
          <div className="nav-brand-icon">
            <Shield size={20} />
          </div>
          <div>
            <span style={{ color: '#fff', fontWeight: 800 }}>Job</span>
            <span style={{ color: '#3b82f6', fontWeight: 800 }}>Shield</span>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8', marginLeft: '6px', fontWeight: 500 }}>AI Verifier</span>
          </div>
        </div>

        {/* Desktop Nav */}
        <div className="nav-links desktop-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activePage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`nav-item ${isActive ? 'active' : ''}`}
              >
                <Icon size={16} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

        {/* System Status Indicator & Mobile Toggle */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '4px 10px',
              borderRadius: '999px',
              fontSize: '0.75rem',
              fontWeight: 600,
              background: systemOnline ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
              color: systemOnline ? '#10b981' : '#ef4444',
              border: `1px solid ${systemOnline ? 'rgba(16, 185, 129, 0.25)' : 'rgba(239, 68, 68, 0.25)'}`
            }}
            title={systemOnline ? 'ML Pipeline & API operational' : 'API offline'}
          >
            <span
              style={{
                width: '7px',
                height: '7px',
                borderRadius: '50%',
                backgroundColor: systemOnline ? '#10b981' : '#ef4444',
                boxShadow: systemOnline ? '0 0 8px #10b981' : 'none'
              }}
            />
            <span>{systemOnline ? 'API Ready' : 'Connecting'}</span>
          </div>

          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="mobile-toggle"
            style={{ color: '#94a3b8', padding: '6px', display: 'flex', alignItems: 'center' }}
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div style={{ background: '#111827', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', padding: '1rem 1.5rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`nav-item ${isActive ? 'active' : ''}`}
                  style={{ width: '100%', justifyContent: 'flex-start' }}
                >
                  <Icon size={18} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      <style>{`
        @media (min-width: 768px) {
          .desktop-nav { display: flex !important; }
          .mobile-toggle { display: none !important; }
        }
        @media (max-width: 767px) {
          .desktop-nav { display: none !important; }
          .mobile-toggle { display: flex !important; }
        }
      `}</style>
    </nav>
  );
}
