import React, { useState, useEffect } from 'react';
import { Archive, Download, CheckCircle2, RefreshCw, FileText, Search } from 'lucide-react';
import { PackageItem } from '../types';

interface PackagesViewProps {
  onDownloadPackage: (leadId: string) => void;
}

export const PackagesView: React.FC<PackagesViewProps> = ({ onDownloadPackage }) => {
  const [packages, setPackages] = useState<PackageItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('');

  const loadPackages = () => {
    setLoading(true);
    fetch('/api/packages')
      .then(res => res.json())
      .then(data => {
        setPackages(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading packages:", err);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadPackages();
  }, []);

  const filtered = packages.filter(p => 
    p.business_name.toLowerCase().includes(search.toLowerCase()) ||
    p.zip_filename.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight text-white">ZIP Opportunity Packages</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Downloadable standardized client pitches, website architecture plans, and evidence archives
          </p>
        </div>

        <button
          onClick={loadPackages}
          className="flex items-center space-x-1.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-300 transition-colors self-start sm:self-auto"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh Packages</span>
        </button>
      </div>

      <div className="relative max-w-md">
        <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Filter packages by business name..."
          className="w-full rounded-xl border border-slate-800 bg-slate-900/80 pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((pkg) => (
          <div key={pkg.id} className="rounded-2xl border border-slate-800 bg-[#0F172A]/70 p-5 backdrop-blur-xl shadow-xl space-y-4 flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className={`rounded px-2 py-0.5 text-[10px] font-bold border ${
                  pkg.priority === 'P1' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' :
                  pkg.priority === 'P2' ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' :
                  'bg-blue-500/10 text-blue-400 border-blue-500/30'
                }`}>
                  {pkg.priority} Package
                </span>
                <span className="flex items-center space-x-1 text-[11px] text-emerald-400 font-semibold">
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  <span>Valid ZIP</span>
                </span>
              </div>

              <h3 className="font-bold text-white text-base truncate" title={pkg.business_name}>
                {pkg.business_name}
              </h3>

              <div className="rounded-lg bg-slate-900/90 border border-slate-800/80 p-2.5 text-xs font-mono text-slate-400 truncate">
                {pkg.zip_filename}
              </div>

              <div className="flex justify-between text-xs text-slate-400 pt-1">
                <span>Size: {(pkg.zip_size_bytes / 1024).toFixed(1)} KB</span>
                <span>v{pkg.version}</span>
              </div>
            </div>

            <button
              onClick={() => onDownloadPackage(pkg.lead_id)}
              className="flex w-full items-center justify-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 py-2.5 text-xs font-bold text-white shadow-lg shadow-blue-600/20 transition-all hover:scale-[1.01]"
            >
              <Download className="h-4 w-4" />
              <span>Download ZIP Package</span>
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
