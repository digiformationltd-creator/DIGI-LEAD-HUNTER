import React, { useState } from 'react';
import { X, Sparkles, MapPin, Tag, Globe, Play, ShieldCheck } from 'lucide-react';

interface FindLeadsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onStartRun: (params: any) => void;
}

export const FindLeadsModal: React.FC<FindLeadsModalProps> = ({ isOpen, onClose, onStartRun }) => {
  const [category, setCategory] = useState('Local Businesses & Services');
  const [country, setCountry] = useState('Pakistan');
  const [location, setLocation] = useState('Lahore');
  const [radius, setRadius] = useState<number>(50);
  const [targetCount, setTargetCount] = useState<number>(15);
  const [p1, setP1] = useState(true);
  const [p2, setP2] = useState(true);

  if (!isOpen) return null;

  const radiusTiers = [
    { value: 5, label: '5 KM' },
    { value: 50, label: '50 KM' },
    { value: 100, label: '100 KM' },
    { value: 1000, label: '1,000 KM' },
    { value: 5000, label: '5,000 KM' },
    { value: 0, label: 'Worldwide' }
  ];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const prios = [];
    if (p1) prios.push('P1');
    if (p2) prios.push('P2');

    onStartRun({
      category,
      location,
      country,
      scope: radius === 0 ? 'WORLDWIDE' : radius >= 1000 ? 'COUNTRY' : 'CITY',
      radius: Number(radius),
      target_count: Number(targetCount),
      priority_filters: prios,
      research_depth: 'Standard',
      package_mode: 'Full Package',
      shariah_compliant_only: true
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md p-4 animate-in fade-in">
      <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-[#0F172A] p-6 shadow-2xl space-y-5">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <ShieldCheck className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Start Lead Hunt</h3>
              <p className="text-[11px] text-emerald-400 font-medium">Compliance & Quality Discovery Active</p>
            </div>
          </div>
          <button onClick={onClose} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white">
            <X className="h-5 w-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-300 mb-1 flex items-center space-x-1.5">
              <Tag className="h-3.5 w-3.5 text-blue-400" />
              <span>Target Category</span>
            </label>
            <input
              type="text"
              required
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              placeholder="e.g. Restaurants, Clinics, Dentists, Boutiques, Auto Workshops"
              className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3.5 py-2.5 text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-semibold text-slate-300 mb-1 flex items-center space-x-1">
                <Globe className="h-3.5 w-3.5 text-sky-400" />
                <span>Country</span>
              </label>
              <select
                value={country}
                onChange={(e) => setCountry(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3 py-2.5 text-white focus:border-blue-500 focus:outline-none"
              >
                <option value="Pakistan">Pakistan</option>
                <option value="United Kingdom">United Kingdom</option>
                <option value="United States">United States</option>
                <option value="United Arab Emirates">UAE</option>
                <option value="Saudi Arabia">Saudi Arabia</option>
                <option value="Canada">Canada</option>
                <option value="Worldwide">Worldwide</option>
              </select>
            </div>

            <div>
              <label className="block font-semibold text-slate-300 mb-1 flex items-center space-x-1">
                <MapPin className="h-3.5 w-3.5 text-emerald-400" />
                <span>City</span>
              </label>
              <input
                type="text"
                required
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. Lahore, London, Dubai"
                className="w-full rounded-xl border border-slate-800 bg-slate-900/90 px-3 py-2.5 text-white focus:border-emerald-500 focus:outline-none"
              />
            </div>
          </div>

          <div>
            <label className="block font-semibold text-slate-300 mb-1.5">Radius &amp; Scope</label>
            <div className="grid grid-cols-3 gap-2 text-center">
              {radiusTiers.map((tier) => (
                <button
                  type="button"
                  key={tier.value}
                  onClick={() => setRadius(tier.value)}
                  className={`rounded-lg border py-2 text-xs font-bold transition-all ${
                    radius === tier.value
                      ? 'border-blue-500 bg-blue-600/20 text-blue-300'
                      : 'border-slate-800 bg-slate-900/40 text-slate-400 hover:text-white'
                  }`}
                >
                  {tier.label}
                </button>
              ))}
            </div>
          </div>

          {/* Priority Opportunity Selection (P1 & P2 Only) */}
          <div className="space-y-2 pt-1">
            <label className="block font-semibold text-slate-300">Opportunity Priority Model</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setP1(!p1)}
                className={`p-2.5 rounded-xl border text-left transition-all ${
                  p1 
                    ? 'border-emerald-500/50 bg-emerald-950/20 text-emerald-300' 
                    : 'border-slate-800 bg-slate-900/40 text-slate-500 hover:text-slate-300'
                }`}
              >
                <div className="font-bold text-[11px] flex items-center justify-between">
                  <span>P1 • New Website</span>
                  <input type="checkbox" checked={p1} readOnly className="h-3.5 w-3.5 accent-emerald-500 pointer-events-none" />
                </div>
                <div className="text-[10px] text-slate-400 mt-0.5">Real Business with NO Website</div>
              </button>

              <button
                type="button"
                onClick={() => setP2(!p2)}
                className={`p-2.5 rounded-xl border text-left transition-all ${
                  p2 
                    ? 'border-blue-500/50 bg-blue-950/20 text-blue-300' 
                    : 'border-slate-800 bg-slate-900/40 text-slate-500 hover:text-slate-300'
                }`}
              >
                <div className="font-bold text-[11px] flex items-center justify-between">
                  <span>P2 • Redesign</span>
                  <input type="checkbox" checked={p2} readOnly className="h-3.5 w-3.5 accent-blue-500 pointer-events-none" />
                </div>
                <div className="text-[10px] text-slate-400 mt-0.5">Website Exists but Outdated/Unfit</div>
              </button>
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              className="flex w-full items-center justify-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 via-indigo-600 to-emerald-500 hover:from-blue-500 hover:to-emerald-400 py-3 font-bold text-white shadow-lg shadow-blue-600/25 transition-all text-sm"
            >
              <Play className="h-4 w-4 fill-white" />
              <span>RUN LEAD HUNT</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
