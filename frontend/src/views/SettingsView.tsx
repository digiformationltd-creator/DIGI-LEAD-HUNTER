import React from 'react';
import { Settings as SettingsIcon, Database, ShieldCheck, Lock, HardDrive, Info } from 'lucide-react';

export const SettingsView: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      <div>
        <h2 className="text-2xl font-extrabold tracking-tight text-white">System Settings & Configuration</h2>
        <p className="text-xs text-slate-400 mt-0.5">Control Center runtime parameters, database paths, and licensing status</p>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-6 space-y-5">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <Database className="h-4 w-4 text-blue-400" />
          <span>Local Storage & Engine Paths</span>
        </h3>

        <div className="space-y-3 text-xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800/80 gap-1">
            <span className="text-slate-400">Database Engine:</span>
            <span className="font-mono text-slate-200">SQLite (Embedded Localhost)</span>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800/80 gap-1">
            <span className="text-slate-400">Database Location:</span>
            <span className="font-mono text-slate-200 truncate">data/database/lead_hunter.db</span>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800/80 gap-1">
            <span className="text-slate-400">Packages Storage:</span>
            <span className="font-mono text-slate-200 truncate">data/packages/</span>
          </div>
        </div>
      </div>

      <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/80 p-6 space-y-4">
        <div className="flex items-center space-x-2 text-white font-bold text-sm">
          <ShieldCheck className="h-4 w-4 text-emerald-400" />
          <span>Brand Ownership & Licensing Guard</span>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 text-xs text-slate-300 space-y-2 leading-relaxed">
          <p>
            <strong>Product:</strong> Digi Biz OS — Lead Hunter<br />
            <strong>Owner:</strong> Digiformation LTD<br />
            <strong>License:</strong> Source-Available (Personal & Internal Use)
          </p>
          <div className="flex items-center space-x-2 text-[11px] text-emerald-400 pt-2 border-t border-slate-800 font-medium">
            <Lock className="h-3.5 w-3.5" />
            <span>Brand Protection Locked: White-labeling and rebranding are strictly disabled per license.</span>
          </div>
        </div>
      </div>
    </div>
  );
};
