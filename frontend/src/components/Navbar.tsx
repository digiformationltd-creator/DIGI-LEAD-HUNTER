import React from 'react';
import { Search, MessageSquare, ExternalLink, ShieldCheck, Sparkles } from 'lucide-react';

interface NavbarProps {
  onOpenFindLeads: () => void;
  onNavigateAbout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpenFindLeads, onNavigateAbout }) => {
  return (
    <header className="sticky top-0 z-30 flex h-16 w-full items-center justify-between border-b border-slate-800/80 bg-[#080C14]/90 px-6 backdrop-blur-md">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-3">
          <img 
            src="/digi-logo.png" 
            alt="Digi Lead Hunter Logo" 
            className="h-9 w-9 rounded-xl object-contain shadow-md shadow-blue-500/10 border border-slate-700/50" 
            onError={(e) => {
              (e.target as HTMLElement).style.display = 'none';
            }}
          />
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold tracking-tight text-white text-base">DIGI LEAD HUNTER</span>
              <span className="rounded-md bg-blue-500/10 px-2 py-0.5 text-[10px] font-semibold tracking-wider text-blue-400 border border-blue-500/20 uppercase">
                Autonomous Agent
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">
              by <strong className="text-slate-300">DIGIFORMATION LTD</strong> • <span className="text-slate-500">Sponsored by Digi Biz OS</span>
            </p>
          </div>
        </div>
      </div>

      <div className="flex items-center space-x-3">
        <div className="hidden md:flex items-center space-x-2 rounded-full bg-slate-900/80 px-3 py-1 text-xs border border-slate-800 text-slate-300">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>Engine Active (Localhost)</span>
        </div>

        <button
          onClick={onOpenFindLeads}
          className="flex items-center space-x-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 px-4 py-2 text-xs font-semibold text-white shadow-lg shadow-blue-600/20 transition-all hover:scale-[1.02]"
        >
          <Sparkles className="h-3.5 w-3.5 text-blue-200" />
          <span>New Lead Hunt</span>
        </button>

        <a
          href="https://wa.me/923164467464?text=Hello%20DIGIFORMATION%20LTD%2C%20I%20am%20using%20Digi%20Lead%20Hunter"
          target="_blank"
          rel="noopener noreferrer"
          className="hidden sm:flex items-center space-x-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 px-3 py-2 text-xs font-medium text-emerald-400 hover:bg-emerald-500/20 transition-all"
        >
          <MessageSquare className="h-3.5 w-3.5" />
          <span>03164467464</span>
        </a>

        <button
          onClick={onNavigateAbout}
          className="rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800 px-3 py-2 text-xs font-medium text-slate-300 transition-colors"
        >
          About & Contact
        </button>
      </div>
    </header>
  );
};
