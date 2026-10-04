import React, { useState } from 'react';
import { 
  Search, 
  MapPin, 
  Tag, 
  Globe, 
  Play, 
  Sparkles, 
  ShieldCheck, 
  CheckCircle2, 
  AlertCircle 
} from 'lucide-react';

interface FindLeadsViewProps {
  onStartRun: (params: any) => void;
}

export const FindLeadsView: React.FC<FindLeadsViewProps> = ({ onStartRun }) => {
  const [category, setCategory] = useState('Restaurants & Dining');
  const [country, setCountry] = useState('Pakistan');
  const [location, setLocation] = useState('Lahore');
  const [scope, setScope] = useState<'CITY' | 'COUNTRY' | 'WORLDWIDE'>('CITY');
  const [radius, setRadius] = useState<number>(50);
  const [targetCount, setTargetCount] = useState<number>(15);
  const [p1, setP1] = useState(true);
  const [p2, setP2] = useState(true);
  const [depth, setDepth] = useState('Standard');
  const [packageMode, setPackageMode] = useState('Full Package');

  const radiusTiers = [
    { value: 5, label: '5 KM', subtitle: 'Hyper-Local' },
    { value: 50, label: '50 KM', subtitle: 'City-Wide' },
    { value: 100, label: '100 KM', subtitle: 'Regional' },
    { value: 1000, label: '1,000 KM', subtitle: 'Country-Wide' },
    { value: 5000, label: '5,000 KM', subtitle: 'Continental' },
    { value: 0, label: 'Worldwide', subtitle: 'Global Scope' }
  ];

  const standardCategories = [
    'Restaurants & Dining',
    'Clinics & Medical Centers',
    'Dental Care & Dentists',
    'Boutiques & Fashion',
    'Salons & Grooming Care',
    'Auto Repair & Workshops',
    'Furniture & Home Decor',
    'Schools & Academies',
    'Gyms & Sports Fitness',
    'Real Estate & Construction',
    'IT & Software Services'
  ];

  const countryCityMap: Record<string, string[]> = {
    'Pakistan': ['Lahore', 'Karachi', 'Islamabad', 'Rawalpindi', 'Faisalabad', 'Multan', 'Peshawar'],
    'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow', 'Bradford'],
    'United States': ['New York', 'Chicago', 'Houston', 'Dallas', 'Los Angeles'],
    'United Arab Emirates': ['Dubai', 'Abu Dhabi', 'Sharjah', 'Ajman'],
    'Saudi Arabia': ['Riyadh', 'Jeddah', 'Dammam', 'Makkah', 'Madinah'],
    'Canada': ['Toronto', 'Vancouver', 'Calgary', 'Montreal'],
    'Worldwide': ['London', 'New York', 'Dubai', 'Lahore', 'Toronto']
  };

  const handleCountryChange = (c: string) => {
    setCountry(c);
    const cities = countryCityMap[c] || ['Main City'];
    setLocation(cities[0]);
  };

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
      research_depth: depth,
      package_mode: packageMode,
      shariah_compliant_only: true
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in duration-300">
      <div>
        <div className="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-400">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Verified Business Intelligence Engine</span>
        </div>
        <h2 className="text-2xl font-extrabold tracking-tight text-white mt-2">
          Find Local & Global Website Opportunities
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Target verified businesses across customizable radii from 5 KM to 5,000 KM or Worldwide with automated quality audits.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="rounded-3xl border border-slate-800 bg-[#0F172A]/80 p-8 shadow-2xl backdrop-blur-xl space-y-6">
        {/* Category Input & Presets */}
        <div className="space-y-2">
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
            <Tag className="h-4 w-4 text-blue-400" />
            <span>Target Business Category</span>
          </label>
          <input
            type="text"
            required
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="e.g. Restaurants, Dental Clinics, Boutiques, Auto Workshops"
            className="w-full rounded-2xl border border-slate-700 bg-slate-900/90 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
          />
          <div className="flex flex-wrap gap-1.5 pt-1">
            {standardCategories.map((cat) => (
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

        {/* Country & Location Selectors */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
              <Globe className="h-4 w-4 text-sky-400" />
              <span>Target Country</span>
            </label>
            <select
              value={country}
              onChange={(e) => handleCountryChange(e.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-900/90 px-4 py-3 text-sm text-white focus:border-blue-500 focus:outline-none"
            >
              <option value="Pakistan">Pakistan</option>
              <option value="United Kingdom">United Kingdom (UK)</option>
              <option value="United States">United States (USA)</option>
              <option value="United Arab Emirates">United Arab Emirates (UAE)</option>
              <option value="Saudi Arabia">Saudi Arabia (KSA)</option>
              <option value="Canada">Canada</option>
              <option value="Worldwide">Worldwide / Global Scope</option>
            </select>
          </div>

          <div className="space-y-2">
            <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
              <MapPin className="h-4 w-4 text-emerald-400" />
              <span>Target City / Region</span>
            </label>
            <input
              type="text"
              required
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="e.g. Lahore, London, Dubai, New York"
              className="w-full rounded-2xl border border-slate-700 bg-slate-900/90 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-emerald-500 focus:outline-none"
            />
            <div className="flex flex-wrap gap-1.5 pt-1">
              {(countryCityMap[country] || []).map((city) => (
                <button
                  type="button"
                  key={city}
                  onClick={() => setLocation(city)}
                  className={`rounded-lg px-2.5 py-0.5 text-[11px] transition-colors ${
                    location === city
                      ? 'bg-emerald-600 text-white font-semibold'
                      : 'bg-slate-800/80 text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {city}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Radius & Geographic Scope Selectors (5km, 50km, 100km, 1000km, 5000km, Worldwide) */}
        <div className="space-y-3 pt-2">
          <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider">
            Geographic Scope & Search Radius
          </label>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
            {radiusTiers.map((tier) => (
              <button
                type="button"
                key={tier.value}
                onClick={() => setRadius(tier.value)}
                className={`rounded-xl border p-3 text-center transition-all ${
                  radius === tier.value
                    ? 'border-blue-500 bg-blue-600/20 text-blue-300 shadow-md shadow-blue-500/10'
                    : 'border-slate-800 bg-slate-900/40 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                }`}
              >
                <div className="font-extrabold text-sm text-white">{tier.label}</div>
                <div className="text-[10px] text-slate-400 mt-0.5">{tier.subtitle}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Lead Target Count Slider */}
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
        </div>

        {/* Submit Button */}
        <div className="pt-2">
          <button
            type="submit"
            className="flex w-full items-center justify-center space-x-2 rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-emerald-500 hover:from-blue-500 hover:to-emerald-400 py-4 font-bold text-white shadow-2xl shadow-blue-600/30 transition-all text-base hover:scale-[1.01]"
          >
            <Play className="h-5 w-5 fill-white" />
            <span>RUN LEAD HUNT PIPELINE</span>
          </button>
        </div>
      </form>
    </div>
  );
};
