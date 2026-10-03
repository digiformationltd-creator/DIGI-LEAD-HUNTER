import React, { useState } from 'react';
import { Search, MapPin, Tag, Sliders, Play, Sparkles, CheckCircle2 } from 'lucide-react';

interface FindLeadsViewProps {
  onStartRun: (params: any) => void;
}

export const FindLeadsView: React.FC<FindLeadsViewProps> = ({ onStartRun }) => {
  const [category, setCategory] = useState('Restaurants');
  const [location, setLocation] = useState('Lahore');
  const [radius, setRadius] = useState(10);
  const [targetCount, setTargetCount] = useState(15);
  const [p1, setP1] = useState(true);
  const [p2, setP2] = useState(true);
  const [p3, setP3] = useState(true);
  const [depth, setDepth] = useState('Standard');
  const [packageMode, setPackageMode] = useState('Full Package');

  const popularCategories = [
    'Restaurants', 'Cafes', 'Hotels', 'Salons & Spas', 
    'Clinics & Dentists', 'Gyms & Fitness', 'Auto Workshops', 
    'Furniture Stores', 'Real Estate', 'Boutiques'
  ];

  const popularLocations = [
    'Lahore', 'Karachi', 'Islamabad', 'London', 'Manchester', 
    'Birmingham', 'New York', 'Dubai'
  ];

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
      package_mode: packageMode
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      <div>
        <div className="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-400">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Automated Google Maps Discovery Engine</span>
        </div>
        <h2 className="text-2xl font-extrabold tracking-tight text-white mt-2">
          Find Local Business Website Opportunities
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Specify the business niche and target city. The engine discovers local businesses on Google Maps, validates WhatsApp numbers, verifies website status, and generates complete opportunity packages.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="rounded-3xl border border-slate-800 bg-[#0F172A]/80 p-8 shadow-2xl backdrop-blur-xl space-y-6">
        {/* Category Input & Quick Presets */}
        <div className="space-y-2">
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
            <Tag className="h-4 w-4 text-blue-400" />
            <span>Target Category</span>
          </label>
          <input
            type="text"
            required
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="e.g. Restaurants, Dentists, Salons, Car Repair"
            className="w-full rounded-2xl border border-slate-700 bg-slate-900/90 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
          />
          <div className="flex flex-wrap gap-1.5 pt-1">
            {popularCategories.map((cat) => (
              <button
                type="button"
                key={cat}
                onClick={() => setCategory(cat)}
                className={`rounded-lg px-2.5 py-1 text-xs transition-colors ${
                  category === cat
                    ? 'bg-blue-600 text-white font-semibold'
                    : 'bg-slate-800/80 text-slate-400 hover:text-slate-200'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Location Input & Quick Presets */}
        <div className="space-y-2">
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
            <MapPin className="h-4 w-4 text-emerald-400" />
            <span>Target Location / City</span>
          </label>
          <input
            type="text"
            required
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. Lahore, London, Manchester, New York"
            className="w-full rounded-2xl border border-slate-700 bg-slate-900/90 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
          />
          <div className="flex flex-wrap gap-1.5 pt-1">
            {popularLocations.map((loc) => (
              <button
                type="button"
                key={loc}
                onClick={() => setLocation(loc)}
                className={`rounded-lg px-2.5 py-1 text-xs transition-colors ${
                  location === loc
                    ? 'bg-emerald-600 text-white font-semibold'
                    : 'bg-slate-800/80 text-slate-400 hover:text-slate-200'
                }`}
              >
                {loc}
              </button>
            ))}
          </div>
        </div>

        {/* Sliders & Parameters */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4 space-y-2">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-300">Search Radius</span>
              <span className="text-blue-400 font-bold">{radius} KM</span>
            </div>
            <input
              type="range"
              min="2"
              max="40"
              value={radius}
              onChange={(e) => setRadius(Number(e.target.value))}
              className="w-full accent-blue-500 cursor-pointer"
            />
            <p className="text-[11px] text-slate-500">Scan distance from target city center.</p>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4 space-y-2">
            <div className="flex justify-between text-xs font-semibold">
              <span className="text-slate-300">Target Lead Count</span>
              <span className="text-emerald-400 font-bold">{targetCount} Leads</span>
            </div>
            <input
              type="range"
              min="5"
              max="50"
              step="5"
              value={targetCount}
              onChange={(e) => setTargetCount(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <p className="text-[11px] text-slate-500">Maximum candidates to discover and qualify.</p>
          </div>
        </div>

        {/* Priority Toggles */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4 space-y-3">
          <span className="text-xs font-bold text-slate-300 uppercase tracking-wider block">
            Opportunity Priority Filters
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <label className={`flex items-start space-x-3 rounded-xl border p-3 cursor-pointer transition-all ${
              p1 ? 'border-emerald-500/40 bg-emerald-950/20 text-emerald-300' : 'border-slate-800 bg-slate-900/30 text-slate-400'
            }`}>
              <input type="checkbox" checked={p1} onChange={(e) => setP1(e.target.checked)} className="mt-0.5 rounded text-emerald-500" />
              <div>
                <div className="font-bold text-xs text-white">Priority 1 (Ready)</div>
                <p className="text-[11px] text-slate-400 mt-0.5">No website + WhatsApp verified + Rich public assets.</p>
              </div>
            </label>

            <label className={`flex items-start space-x-3 rounded-xl border p-3 cursor-pointer transition-all ${
              p2 ? 'border-amber-500/40 bg-amber-950/20 text-amber-300' : 'border-slate-800 bg-slate-900/30 text-slate-400'
            }`}>
              <input type="checkbox" checked={p2} onChange={(e) => setP2(e.target.checked)} className="mt-0.5 rounded text-amber-500" />
              <div>
                <div className="font-bold text-xs text-white">Priority 2 (Consult)</div>
                <p className="text-[11px] text-slate-400 mt-0.5">No website + WhatsApp + Limited public assets.</p>
              </div>
            </label>

            <label className={`flex items-start space-x-3 rounded-xl border p-3 cursor-pointer transition-all ${
              p3 ? 'border-blue-500/40 bg-blue-950/20 text-blue-300' : 'border-slate-800 bg-slate-900/30 text-slate-400'
            }`}>
              <input type="checkbox" checked={p3} onChange={(e) => setP3(e.target.checked)} className="mt-0.5 rounded text-blue-500" />
              <div>
                <div className="font-bold text-xs text-white">Priority 3 (Redesign)</div>
                <p className="text-[11px] text-slate-400 mt-0.5">Existing website with outdated layout or poor mobile UX.</p>
              </div>
            </label>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-2">
          <button
            type="submit"
            className="flex w-full items-center justify-center space-x-2 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-teal-500 hover:from-blue-500 hover:to-teal-400 py-4 font-bold text-white shadow-2xl shadow-blue-600/30 transition-all text-base hover:scale-[1.01]"
          >
            <Play className="h-5 w-5 fill-white" />
            <span>START END-TO-END LEAD HUNT PIPELINE</span>
          </button>
        </div>
      </form>
    </div>
  );
};
