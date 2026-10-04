import React from 'react';
import { 
  Users, 
  Flame, 
  Clock, 
  RefreshCw, 
  Archive, 
  CheckCircle2, 
  Sparkles,
  ArrowRight,
  TrendingUp,
  MessageSquare
} from 'lucide-react';
import { KpiCard } from '../components/KpiCard';
import { LeadsTable } from '../components/LeadsTable';
import { LiveRunProgress } from '../components/LiveRunProgress';
import { Lead, RunDetail, AnalyticsData } from '../types';

interface DashboardViewProps {
  analytics: AnalyticsData | null;
  recentLeads: Lead[];
  activeRun: RunDetail | null;
  onOpenFindLeads: () => void;
  onSelectLead: (lead: Lead) => void;
  onDownloadPackage: (leadId: string) => void;
  onViewAllLeads: () => void;
}

export const DashboardView: React.FC<DashboardViewProps> = ({
  analytics,
  recentLeads,
  activeRun,
  onOpenFindLeads,
  onSelectLead,
  onDownloadPackage,
  onViewAllLeads
}) => {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-r from-blue-950/40 via-indigo-950/30 to-[#0A0F1D] p-8 shadow-2xl backdrop-blur-xl">
        <div className="relative z-10 max-w-2xl space-y-3">
          <div className="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-400">
            <Sparkles className="h-3.5 w-3.5" />
            <span>Digiformation LTD • Local Business Intelligence</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">
            DIGI LEAD HUNTER Control Center
          </h1>
          <p className="text-xs text-slate-400 font-medium">
            by <strong className="text-slate-200">Digiformation LTD</strong> • Sponsored by Digi Biz OS
          </p>
          <p className="text-xs text-slate-300 leading-relaxed pt-1">
            Discover local businesses on Google Maps lacking official websites, verify direct WhatsApp channels, and automatically generate high-converting website architecture plans and ZIP opportunity packages.
          </p>
          <div className="pt-2 flex items-center space-x-3">
            <button
              onClick={onOpenFindLeads}
              className="flex items-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 px-5 py-2.5 font-bold text-xs text-white shadow-xl shadow-blue-600/25 transition-all hover:scale-[1.02]"
            >
              <Sparkles className="h-4 w-4 text-blue-200" />
              <span>Launch New Lead Hunt</span>
            </button>
            <button
              onClick={onViewAllLeads}
              className="flex items-center space-x-2 rounded-xl border border-slate-700 bg-slate-800/60 hover:bg-slate-800 px-4 py-2.5 font-semibold text-xs text-slate-200 transition-colors"
            >
              <span>Explore All Leads</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KpiCard
          title="Total Researched"
          value={analytics?.total_leads || 0}
          subtitle="Unique verified businesses"
          icon={Users}
          color="blue"
        />
        <KpiCard
          title="Priority 1 (Ready)"
          value={analytics?.p1_count || 0}
          subtitle="No website + WhatsApp verified"
          icon={Flame}
          color="emerald"
        />
        <KpiCard
          title="Priority 2 (Consult)"
          value={analytics?.p2_count || 0}
          subtitle="Limited assets / Onboarding needed"
          icon={Clock}
          color="amber"
        />
        <KpiCard
          title="Packages Ready"
          value={analytics?.ready_packages || 0}
          subtitle="Validated ZIP opportunity packs"
          icon={Archive}
          color="purple"
        />
      </div>

      {/* Active Run Banner (If currently executing) */}
      {activeRun && activeRun.status !== 'COMPLETED' && (
        <LiveRunProgress run={activeRun} />
      )}

      {/* Recent Discovered Leads */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-white">Recent Website Opportunities</h3>
            <p className="text-xs text-slate-400">Newly discovered leads and build-ready packages</p>
          </div>
          <button
            onClick={onViewAllLeads}
            className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center space-x-1"
          >
            <span>View All Leads ({analytics?.total_leads || 0})</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </button>
        </div>

        <LeadsTable
          leads={recentLeads.slice(0, 6)}
          onSelectLead={onSelectLead}
          onDownloadPackage={onDownloadPackage}
        />
      </div>
    </div>
  );
};
