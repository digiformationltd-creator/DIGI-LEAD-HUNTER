import React from 'react';
import { BarChart3, TrendingUp, ShieldCheck, CheckCircle2, Globe, Flame, Clock } from 'lucide-react';
import { AnalyticsData } from '../types';

interface AnalyticsViewProps {
  analytics: AnalyticsData | null;
}

export const AnalyticsView: React.FC<AnalyticsViewProps> = ({ analytics }) => {
  const total = analytics?.total_leads || 1;
  const p1Ratio = Math.round(((analytics?.p1_count || 0) / total) * 100);
  const p2Ratio = Math.round(((analytics?.p2_count || 0) / total) * 100);
  const waVerifiedRatio = Math.round(((analytics?.whatsapp_verified_count || 0) / total) * 100);

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      <div>
        <h2 className="text-2xl font-extrabold tracking-tight text-white">Lead Intelligence & Conversion Analytics</h2>
        <p className="text-xs text-slate-400 mt-0.5">Factual breakdown of verified opportunities and build-readiness tiers</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-5 space-y-2">
          <div className="text-xs font-semibold text-slate-400 uppercase">P1 Build-Ready Share</div>
          <div className="text-3xl font-extrabold text-emerald-400">{p1Ratio}%</div>
          <p className="text-[11px] text-slate-500">{analytics?.p1_count || 0} leads with verified WhatsApp and no website.</p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-5 space-y-2">
          <div className="text-xs font-semibold text-slate-400 uppercase">WhatsApp Verification Rate</div>
          <div className="text-3xl font-extrabold text-teal-400">{waVerifiedRatio}%</div>
          <p className="text-[11px] text-slate-500">{analytics?.whatsapp_verified_count || 0} leads validated for instant mobile messaging.</p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-5 space-y-2">
          <div className="text-xs font-semibold text-slate-400 uppercase">Packages Assembled</div>
          <div className="text-3xl font-extrabold text-purple-400">{analytics?.ready_packages || 0}</div>
          <p className="text-[11px] text-slate-500">Validated ZIP archives ready for client consultation.</p>
        </div>
      </div>

      {/* Funnel Progress */}
      <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-6 space-y-5">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider">Opportunity Distribution</h3>

        <div className="space-y-4">
          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-emerald-400 flex items-center space-x-1.5">
                <Flame className="h-3.5 w-3.5" />
                <span>Priority 1: High Build-Readiness ({analytics?.p1_count || 0})</span>
              </span>
              <span className="text-slate-300">{p1Ratio}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${p1Ratio}%` }}></div>
            </div>
          </div>

          <div className="space-y-1.5">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-blue-400 flex items-center space-x-1.5">
                <Globe className="h-3.5 w-3.5" />
                <span>Priority 2: Website Redesign / Rebuild Opportunity ({analytics?.p2_count || 0})</span>
              </span>
              <span className="text-slate-300">{p2Ratio}%</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div className="h-full bg-blue-500 rounded-full" style={{ width: `${p2Ratio}%` }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
