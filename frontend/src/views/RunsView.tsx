import React from 'react';
import { RefreshCw, Play, CheckCircle2, AlertTriangle, Layers, Calendar, ArrowRight } from 'lucide-react';
import { RunDetail } from '../types';

interface RunsViewProps {
  runs: any[];
  activeRun: RunDetail | null;
  onRefresh: () => void;
  onSelectRun: (runId: string) => void;
  onOpenFindLeads: () => void;
}

export const RunsView: React.FC<RunsViewProps> = ({ 
  runs, 
  activeRun, 
  onRefresh, 
  onSelectRun,
  onOpenFindLeads 
}) => {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight text-white">Pipeline Runs & Orchestration</h2>
          <p className="text-xs text-slate-400 mt-0.5">Execution history, live stage checkpoints, and logs</p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={onRefresh}
            className="flex items-center space-x-1.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-300 transition-colors"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            <span>Refresh Runs</span>
          </button>
          <button
            onClick={onOpenFindLeads}
            className="flex items-center space-x-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 px-4 py-2 text-xs font-semibold text-white transition-colors"
          >
            <Play className="h-3.5 w-3.5 fill-white" />
            <span>New Run</span>
          </button>
        </div>
      </div>

      {/* Runs Table */}
      <div className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0F172A]/70 backdrop-blur-xl shadow-xl">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900/60 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              <th className="py-3.5 px-4">Run ID / Scope</th>
              <th className="py-3.5 px-3">Status</th>
              <th className="py-3.5 px-3">Target vs Qualified</th>
              <th className="py-3.5 px-3">P1 / P2 / P3 Breakdown</th>
              <th className="py-3.5 px-3">Started</th>
              <th className="py-3.5 px-4 text-right">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {runs.map((r) => (
              <tr key={r.run_id} className="hover:bg-slate-800/40 transition-colors">
                <td className="py-3.5 px-4">
                  <div className="font-bold text-white font-mono">{r.run_id}</div>
                  <div className="text-slate-400 text-[11px] mt-0.5">
                    <strong>{r.category}</strong> in <strong>{r.location}</strong> ({r.radius} km)
                  </div>
                </td>

                <td className="py-3.5 px-3">
                  <span className={`inline-flex items-center rounded-md px-2.5 py-1 text-xs font-bold border ${
                    r.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' :
                    r.status === 'FAILED' ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
                    'bg-blue-500/10 text-blue-400 border-blue-500/30 animate-pulse'
                  }`}>
                    {r.status}
                  </span>
                </td>

                <td className="py-3.5 px-3">
                  <div className="text-slate-200 font-semibold">{r.qualified_count || 0} Qualified</div>
                  <div className="text-[11px] text-slate-500">{r.lead_count || 0} Discovered (Target: {r.target_count})</div>
                </td>

                <td className="py-3.5 px-3">
                  <div className="flex items-center space-x-2 text-[11px] font-semibold">
                    <span className="text-emerald-400">P1: {r.p1_count || 0}</span>
                    <span>•</span>
                    <span className="text-amber-400">P2: {r.p2_count || 0}</span>
                    <span>•</span>
                    <span className="text-blue-400">P3: {r.p3_count || 0}</span>
                  </div>
                </td>

                <td className="py-3.5 px-3 text-slate-400 text-[11px]">
                  {r.started_at ? new Date(r.started_at).toLocaleString() : 'N/A'}
                </td>

                <td className="py-3.5 px-4 text-right">
                  <button
                    onClick={() => onSelectRun(r.run_id)}
                    className="inline-flex items-center space-x-1 rounded-lg border border-slate-800 bg-slate-900/60 hover:bg-slate-800 px-3 py-1.5 text-xs text-slate-300 transition-colors"
                  >
                    <span>View Stream</span>
                    <ArrowRight className="h-3 w-3" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
