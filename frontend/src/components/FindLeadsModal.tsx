import React, { useState } from 'react';
import { X, Sparkles, MapPin, Tag, Sliders, Layers, Play } from 'lucide-react';

interface FindLeadsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onStartRun: (params: any) => void;
}

export const FindLeadsModal: React.FC<FindLeadsModalProps> = ({ isOpen, onClose, onStartRun }) => {
  const [category, setCategory] = useState('Restaurants');
  const [location, setLocation] = useState('Lahore');
  const [radius, setRadius] = useState(10);
  const [targetCount, setTargetCount] = useState(15);
  const [p1, setP1] = useState(true);
  const [p2, setP2] = useState(true);
  const [p3, setP3] = useState(true);
  const [depth, setDepth] = useState('Standard');
  const [pkgMode, setPkgMode] = useState('Full Package');

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const prios = [];
    if (p1) prios.push('P1');
    if (p2) prios.push('P2');
    if (p3) prios.push('P3');

    onStartRun({
      category,
      location,
      radius: Number(radius),
      target_count: Number(targetCount),
      priority_filters: prios,
      research_depth: depth,
      package_mode: pkgMode
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md p-4 animate-in fade-in">
      <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-[#0F172A] p-6 shadow-2xl space-y-6">
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Start New Lead Hunt</h3>
              <p className="text-xs text-slate-400">Google Maps Discovery & Opportunity Packaging</p>
            </div>
          </div>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white">
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-300 mb-1.5 flex items-center space-x-1.5">
              <Tag className="h-3.5 w-3.5 text-blue-400" />
              <span>Target Business Category</span>
            </label>
            <input
              type="text"
              required
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="e.g. Restaurants, Salons, Dentists, Clinics, Gyms"
              className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3.5 py-2.5 text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-300 mb-1.5 flex items-center space-x-1.5">
              <MapPin className="h-3.5 w-3.5 text-emerald-400" />
              <span>Target City / Area</span>
            </label>
            <input
              type="text"
              required
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Lahore, London, Manchester, New York"
              className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3.5 py-2.5 text-white placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block font-semibold text-slate-300 mb-1.5">Search Radius (KM)</label>
              <input
                type="number"
                min="1"
                max="50"
                value={radius}
                onChange={(e) => setRadius(Number(e.target.value))}
                className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
              />
            </div>
            <div>
              <label className="block font-semibold text-slate-300 mb-1.5">Target Lead Count</label>
              <input
                type="number"
                min="5"
                max="50"
                value={targetCount}
                onChange={(e) => setTargetCount(Number(e.target.value))}
                className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3 py-2 text-white focus:border-blue-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-300 mb-2">Priority Filters</label>
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-1.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={p1}
                  onChange={(e) => setP1(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-0"
                />
                <span className="text-emerald-400 font-semibold">P1 (Ready)</span>
              </label>
              <label className="flex items-center space-x-1.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={p2}
                  onChange={(e) => setP2(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-800 text-amber-500 focus:ring-0"
                />
                <span className="text-amber-400 font-semibold">P2 (Consult)</span>
              </label>
              <label className="flex items-center space-x-1.5 cursor-pointer">
                <input
                  type="checkbox"
                  checked={p3}
                  onChange={(e) => setP3(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-800 text-blue-500 focus:ring-0"
                />
                <span className="text-blue-400 font-semibold">P3 (Redesign)</span>
              </label>
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              className="flex w-full items-center justify-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 py-3 font-bold text-white shadow-lg shadow-blue-600/25 transition-all text-sm"
            >
              <Play className="h-4 w-4 fill-white" />
              <span>RUN LEAD HUNT PIPELINE</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
