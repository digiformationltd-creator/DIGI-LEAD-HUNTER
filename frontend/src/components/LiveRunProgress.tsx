import React from 'react';
import { RefreshCw, CheckCircle2, AlertTriangle, Layers, Activity } from 'lucide-react';
import { RunDetail } from '../types';

interface LiveRunProgressProps {
  run: RunDetail | null;
  onRefresh?: () => void;
}

export const LiveRunProgress: React.FC<LiveRunProgressProps> = ({ run, onRefresh }) => {
  if (!run) return null;

  const stages = [
    { key: 'INITIALIZING', label: 'Init' },
    { key: 'DISCOVERING', label: 'Discovery' },
    { key: 'VERIFYING', label: 'Verification' },
    { key: 'CLASSIFYING', label: 'Classification' },
    { key: 'PLANNING', label: 'Website Plan' },
    { key: 'PACKAGING', label: 'ZIP Packaging' },
    { key: 'COMPLETED', label: 'Complete' }
  ];

  const currentStageIndex = stages.findIndex(s => s.key === run.status);
  const isCompleted = run.status === 'COMPLETED';
  const isFailed = run.status === 'FAILED';

  const progressPercent = isCompleted ? 100 :
    currentStageIndex !== -1 ? Math.round(((currentStageIndex + 1) / stages.length) * 100) : 35;

  return (
    <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-6 backdrop-blur-xl shadow-xl space-y-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className={`flex h-10 w-10 items-center justify-center rounded-xl border ${
            isCompleted ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
            isFailed ? 'bg-rose-500/10 text-rose-400 border-rose-500/20' :
            'bg-blue-500/10 text-blue-400 border-blue-500/20'
          }`}>
            {isCompleted ? <CheckCircle2 className="h-5 w-5" /> :
             isFailed ? <AlertTriangle className="h-5 w-5" /> :
             <RefreshCw className="h-5 w-5 animate-spin" />}
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h3 className="font-bold text-white text-base">Active Search Pipeline</h3>
              <span className="font-mono text-xs text-slate-400">({run.run_id})</span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Target: <strong className="text-slate-200">{run.category}</strong> in <strong className="text-slate-200">{run.location}</strong> ({run.radius} km radius)
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <span className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold border ${
            isCompleted ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' :
            isFailed ? 'bg-rose-500/10 text-rose-400 border-rose-500/30' :
            'bg-blue-500/10 text-blue-400 border-blue-500/30 animate-pulse'
          }`}>
            {run.status}
          </span>
          {onRefresh && (
            <button onClick={onRefresh} className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors">
              <RefreshCw className="h-4 w-4" />
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-1.5">
        <div className="flex justify-between text-xs font-semibold">
          <span className="text-slate-400">Stage: {run.status}</span>
          <span className="text-blue-400">{progressPercent}%</span>
        </div>
        <div className="h-2.5 w-full rounded-full bg-slate-800 overflow-hidden">
          <div 
            className={`h-full rounded-full transition-all duration-500 ${
              isCompleted ? 'bg-emerald-500' : isFailed ? 'bg-rose-500' : 'bg-gradient-to-r from-blue-600 to-indigo-500'
            }`}
            style={{ width: `${progressPercent}%` }}
          ></div>
        </div>
      </div>

      {/* Real-time counters */}
      <div className="grid grid-cols-4 gap-3 pt-2 text-center text-xs">
        <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-2.5">
          <div className="text-slate-500 text-[10px] uppercase font-bold">Discovered</div>
          <div className="text-base font-bold text-white mt-0.5">{run.lead_count}</div>
        </div>
        <div className="rounded-xl bg-emerald-950/20 border border-emerald-500/20 p-2.5">
          <div className="text-emerald-400 text-[10px] uppercase font-bold">P1 Ready</div>
          <div className="text-base font-bold text-emerald-400 mt-0.5">{run.p1_count}</div>
        </div>
        <div className="rounded-xl bg-blue-950/20 border border-blue-500/20 p-2.5">
          <div className="text-blue-400 text-[10px] uppercase font-bold">P2 Redesign</div>
          <div className="text-base font-bold text-blue-400 mt-0.5">{run.p2_count}</div>
        </div>
        <div className="rounded-xl bg-slate-900/60 border border-slate-800 p-2.5">
          <div className="text-slate-400 text-[10px] uppercase font-bold">Excluded</div>
          <div className="text-base font-bold text-slate-400 mt-0.5">
            {Math.max(0, (run.lead_count || 0) - (run.p1_count || 0) - (run.p2_count || 0))}
          </div>
        </div>
      </div>

      {/* Live Event Console */}
      {run.events && run.events.length > 0 && (
        <div className="space-y-2">
          <div className="text-[11px] font-bold text-slate-400 uppercase flex items-center space-x-1.5">
            <Activity className="h-3.5 w-3.5 text-blue-400" />
            <span>Live Orchestration Stream</span>
          </div>
          <div className="max-h-36 overflow-y-auto rounded-xl bg-slate-950/80 border border-slate-800 p-3 font-mono text-[11px] text-slate-300 space-y-1">
            {run.events.slice(-6).map((e, idx) => (
              <div key={idx} className="flex items-start space-x-2">
                <span className="text-slate-500">[{e.stage}]</span>
                <span className={e.level === 'ERROR' ? 'text-rose-400' : 'text-slate-300'}>{e.message}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
