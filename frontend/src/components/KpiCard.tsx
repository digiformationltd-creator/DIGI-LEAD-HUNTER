import React from 'react';
import { LucideIcon } from 'lucide-react';

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  badge?: string;
  color?: 'blue' | 'emerald' | 'amber' | 'purple' | 'slate';
  onClick?: () => void;
}

export const KpiCard: React.FC<KpiCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  badge,
  color = 'blue',
  onClick
}) => {
  const colorMap = {
    blue: 'border-blue-500/20 bg-blue-950/20 text-blue-400 group-hover:border-blue-500/40',
    emerald: 'border-emerald-500/20 bg-emerald-950/20 text-emerald-400 group-hover:border-emerald-500/40',
    amber: 'border-amber-500/20 bg-amber-950/20 text-amber-400 group-hover:border-amber-500/40',
    purple: 'border-purple-500/20 bg-purple-950/20 text-purple-400 group-hover:border-purple-500/40',
    slate: 'border-slate-700/40 bg-slate-900/40 text-slate-400 group-hover:border-slate-600',
  };

  const iconBgMap = {
    blue: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    emerald: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    amber: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    purple: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    slate: 'bg-slate-800 text-slate-400 border-slate-700',
  };

  return (
    <div
      onClick={onClick}
      className={`group relative overflow-hidden rounded-2xl border p-5 transition-all backdrop-blur-md ${colorMap[color]} ${onClick ? 'cursor-pointer hover:scale-[1.01]' : ''}`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        <div className={`flex h-10 w-10 items-center justify-center rounded-xl border ${iconBgMap[color]}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <div className="mt-4 flex items-baseline space-x-2">
        <span className="text-3xl font-extrabold tracking-tight text-white">{value}</span>
        {badge && (
          <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] font-semibold text-slate-300 border border-slate-700">
            {badge}
          </span>
        )}
      </div>
      {subtitle && <p className="mt-1 text-xs text-slate-400">{subtitle}</p>}
    </div>
  );
};
