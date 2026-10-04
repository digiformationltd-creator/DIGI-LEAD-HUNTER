import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { WhatsAppWidget } from './components/WhatsAppWidget';
import { FindLeadsModal } from './components/FindLeadsModal';
import { LeadDetailDrawer } from './components/LeadDetailDrawer';

import { DashboardView } from './views/DashboardView';
import { FindLeadsView } from './views/FindLeadsView';
import { LeadsView } from './views/LeadsView';
import { RunsView } from './views/RunsView';
import { PackagesView } from './views/PackagesView';
import { AnalyticsView } from './views/AnalyticsView';
import { AboutView } from './views/AboutView';
import { SettingsView } from './views/SettingsView';

import { Lead, RunDetail, AnalyticsData } from './types';

export const App: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<string>('dashboard');
  const [isFindLeadsModalOpen, setIsFindLeadsModalOpen] = useState(false);
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

  const [leads, setLeads] = useState<Lead[]>([]);
  const [runs, setRuns] = useState<any[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [activeRun, setActiveRun] = useState<RunDetail | null>(null);

  const fetchLeads = () => {
    fetch('/api/leads?limit=250')
      .then(res => res.json())
      .then(data => setLeads(data))
      .catch(err => console.error("Error fetching leads:", err));
  };

  const fetchRuns = () => {
    fetch('/api/runs')
      .then(res => res.json())
      .then(data => {
        setRuns(data);
        const inProgress = data.find((r: any) => 
          ['INITIALIZING', 'DISCOVERING', 'VERIFYING', 'CLASSIFYING', 'PLANNING', 'PACKAGING'].includes(r.status)
        );
        if (inProgress) {
          fetchRunDetail(inProgress.run_id);
        }
      })
      .catch(err => console.error("Error fetching runs:", err));
  };

  const fetchRunDetail = (runId: string) => {
    fetch(`/api/runs/${runId}`)
      .then(res => res.json())
      .then(data => setActiveRun(data))
      .catch(err => console.error("Error fetching run detail:", err));
  };

  const fetchAnalytics = () => {
    fetch('/api/analytics')
      .then(res => res.json())
      .then(data => setAnalytics(data))
      .catch(err => console.error("Error fetching analytics:", err));
  };

  const refreshAll = () => {
    fetchLeads();
    fetchRuns();
    fetchAnalytics();
  };

  useEffect(() => {
    refreshAll();
  }, []);

  // Poll active run if running
  useEffect(() => {
    if (!activeRun || activeRun.status === 'COMPLETED' || activeRun.status === 'FAILED') return;
    const interval = setInterval(() => {
      fetch(`/api/runs/${activeRun.run_id}`)
        .then(res => res.json())
        .then(data => {
          setActiveRun(data);
          if (data.status === 'COMPLETED' || data.status === 'FAILED') {
            refreshAll();
          }
        })
        .catch(err => console.error("Polling error:", err));
    }, 2500);

    return () => clearInterval(interval);
  }, [activeRun]);

  const handleStartRun = (params: any) => {
    fetch('/api/runs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    })
      .then(res => res.json())
      .then(data => {
        if (data.run_id) {
          fetchRunDetail(data.run_id);
          setCurrentTab('dashboard');
        }
      })
      .catch(err => console.error("Error starting run:", err));
  };

  const handleDownloadPackage = (leadId: string) => {
    window.open(`/api/packages/lead/${leadId}/download`, '_blank');
  };

  return (
    <div className="flex h-screen flex-col bg-[#080C14] text-slate-100 overflow-hidden">
      {/* Top Navbar */}
      <Navbar 
        onOpenFindLeads={() => setIsFindLeadsModalOpen(true)}
        onNavigateAbout={() => setCurrentTab('about')}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          currentTab={currentTab}
          onSelectTab={(tab) => setCurrentTab(tab)}
          p1Count={analytics?.p1_count}
          p2Count={analytics?.p2_count}
        />

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8">
          {currentTab === 'dashboard' && (
            <DashboardView
              analytics={analytics}
              recentLeads={leads}
              activeRun={activeRun}
              onOpenFindLeads={() => setIsFindLeadsModalOpen(true)}
              onSelectLead={(lead) => setSelectedLead(lead)}
              onDownloadPackage={handleDownloadPackage}
              onViewAllLeads={() => setCurrentTab('all-leads')}
            />
          )}

          {currentTab === 'find-leads' && (
            <FindLeadsView onStartRun={handleStartRun} />
          )}

          {currentTab === 'all-leads' && (
            <LeadsView
              leads={leads}
              onSelectLead={(lead) => setSelectedLead(lead)}
              onDownloadPackage={handleDownloadPackage}
              onRefresh={fetchLeads}
              defaultPriority="ALL"
            />
          )}

          {currentTab === 'p1-leads' && (
            <LeadsView
              leads={leads}
              onSelectLead={(lead) => setSelectedLead(lead)}
              onDownloadPackage={handleDownloadPackage}
              onRefresh={fetchLeads}
              defaultPriority="P1"
            />
          )}

          {currentTab === 'p2-leads' && (
            <LeadsView
              leads={leads}
              onSelectLead={(lead) => setSelectedLead(lead)}
              onDownloadPackage={handleDownloadPackage}
              onRefresh={fetchLeads}
              defaultPriority="P2"
            />
          )}

          {currentTab === 'runs' && (
            <RunsView
              runs={runs}
              activeRun={activeRun}
              onRefresh={fetchRuns}
              onSelectRun={(runId) => fetchRunDetail(runId)}
              onOpenFindLeads={() => setIsFindLeadsModalOpen(true)}
            />
          )}

          {currentTab === 'packages' && (
            <PackagesView onDownloadPackage={handleDownloadPackage} />
          )}

          {currentTab === 'analytics' && (
            <AnalyticsView analytics={analytics} />
          )}

          {currentTab === 'about' && (
            <AboutView />
          )}

          {currentTab === 'settings' && (
            <SettingsView />
          )}
        </main>
      </div>

      {/* Floating WhatsApp Support Widget */}
      <WhatsAppWidget />

      {/* Find Leads Modal */}
      <FindLeadsModal
        isOpen={isFindLeadsModalOpen}
        onClose={() => setIsFindLeadsModalOpen(false)}
        onStartRun={handleStartRun}
      />

      {/* Lead Detail Drawer */}
      <LeadDetailDrawer
        lead={selectedLead}
        onClose={() => setSelectedLead(null)}
        onDownloadPackage={handleDownloadPackage}
      />
    </div>
  );
};
export default App;
