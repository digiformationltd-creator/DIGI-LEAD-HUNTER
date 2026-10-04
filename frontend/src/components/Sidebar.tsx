import React from 'react';
import { 
  LayoutDashboard, 
  Search, 
  Users, 
  Flame, 
  Clock, 
  RefreshCw, 
  Archive, 
  BarChart3, 
  Info, 
  Settings,
  ShieldCheck,
  Building2
} from 'lucide-react';

interface SidebarProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
  p1Count?: number;
  p2Count?: number;
  p3Count?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  currentTab, 
  onSelectTab, 
  p1Count = 0, 
  p2Count = 0, 
  p3Count = 0 
}) => {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'find-leads', label: 'Find Leads', icon: Search, highlight: true },
    { id: 'all-leads', label: 'All Leads', icon: Users },
    { id: 'p1-leads', label: 'Priority 1 (Ready)', icon: Flame, badge: p1Count, badgeColor: 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' },
    { id: 'p2-leads', label: 'Priority 2 (Consult)', icon: Clock, badge: p2Count, badgeColor: 'bg-amber-500/20 text-amber-400 border border-amber-500/30' },
    { id: 'p3-leads', label: 'Priority 3 (Redesign)', icon: RefreshCw, badge: p3Count, badgeColor: 'bg-blue-500/20 text-blue-400 border border-blue-500/30' },
    { id: 'runs', label: 'Active & Run History', icon: RefreshCw },
    { id: 'packages', label: 'ZIP Packages', icon: Archive },
    { id: 'analytics', label: 'Analytics & Funnel', icon: BarChart3 },
    { id: 'about', label: 'About & Contacts', icon: Info },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 flex-shrink-0 border-r border-slate-800/80 bg-[#0A0F1D]/80 flex flex-col justify-between p-4 backdrop-blur-md">
      <div className="space-y-6">
        <div>
          <span className="px-3 text-[11px] font-bold tracking-wider text-slate-500 uppercase">
            Platform Navigation
          </span>
          <nav className="mt-2 space-y-1">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onSelectTab(item.id)}
                  className={`flex w-full items-center justify-between rounded-xl px-3 py-2.5 text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-blue-600/15 text-blue-400 border border-blue-500/30 shadow-sm'
                      : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                  } ${item.highlight && !isActive ? 'border border-indigo-500/20 text-indigo-300' : ''}`}
                >
                  <div className="flex items-center space-x-3">
                    <Icon className={`h-4 w-4 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge !== undefined && item.badge > 0 && (
                    <span className={`rounded-md px-2 py-0.5 text-[10px] font-bold ${item.badgeColor}`}>
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Brand Ownership & Attribution Box */}
      <div className="rounded-2xl border border-slate-800/90 bg-[#0F172A]/90 p-3.5 text-xs text-slate-400 space-y-2">
        <div className="flex items-center space-x-2 text-slate-300 font-semibold">
          <Building2 className="h-4 w-4 text-blue-400" />
          <span className="text-[11px] text-white">DIGIFORMATION LTD</span>
        </div>
        <p className="text-[10px] leading-relaxed text-slate-400">
          Source-available personal & internal research engine. Commercial resale & white-labeling strictly prohibited.
        </p>
        <div className="pt-1 flex items-center justify-between text-[10px] border-t border-slate-800 text-slate-500">
          <span>v1.0.0 Production</span>
          <span className="text-emerald-400 font-medium">Licensed</span>
        </div>
      </div>
    </aside>
  );
};
