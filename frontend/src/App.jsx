import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Pages
import LandingPage from './pages/LandingPage';
import DashboardPage from './pages/DashboardPage';
import AnalyzePage from './pages/AnalyzePage';
import AnalysisDetailPage from './pages/AnalysisDetailPage';
import JobSearchPage from './pages/JobSearchPage';
import HistoryPage from './pages/HistoryPage';
import AboutPage from './pages/AboutPage';

export default function App() {
  const [activePage, setActivePage] = useState('landing');
  const [latestAnalysis, setLatestAnalysis] = useState(null);
  const [selectedAnalysisId, setSelectedAnalysisId] = useState(null);
  const [preloadedAnalysis, setPreloadedAnalysis] = useState(null);

  const renderCurrentPage = () => {
    switch (activePage) {
      case 'landing':
        return (
          <LandingPage
            setActivePage={setActivePage}
            setPreloadedAnalysis={setPreloadedAnalysis}
          />
        );
      case 'dashboard':
        return (
          <DashboardPage
            setActivePage={setActivePage}
            setSelectedAnalysisId={setSelectedAnalysisId}
          />
        );
      case 'analyze':
        return (
          <AnalyzePage
            setActivePage={setActivePage}
            setLatestAnalysis={setLatestAnalysis}
            preloadedAnalysis={preloadedAnalysis}
          />
        );
      case 'detail':
        return (
          <AnalysisDetailPage
            analysis={latestAnalysis}
            analysisId={selectedAnalysisId}
            setActivePage={setActivePage}
            setSelectedAnalysisId={setSelectedAnalysisId}
          />
        );
      case 'search':
        return (
          <JobSearchPage
            setActivePage={setActivePage}
            setPreloadedAnalysis={setPreloadedAnalysis}
          />
        );
      case 'history':
        return (
          <HistoryPage
            setActivePage={setActivePage}
            setSelectedAnalysisId={setSelectedAnalysisId}
          />
        );
      case 'about':
        return <AboutPage />;
      default:
        return (
          <LandingPage
            setActivePage={setActivePage}
            setPreloadedAnalysis={setPreloadedAnalysis}
          />
        );
    }
  };

  return (
    <div className="app-container">
      <Navbar activePage={activePage} setActivePage={setActivePage} />
      <main className="main-content">
        {renderCurrentPage()}
      </main>
      <Footer setActivePage={setActivePage} />
    </div>
  );
}
