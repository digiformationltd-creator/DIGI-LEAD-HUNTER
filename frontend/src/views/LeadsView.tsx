import React, { useState } from 'react';
import { Search, Filter, RefreshCw, Flame, Clock, RefreshCcw, Download } from 'lucide-react';
import { LeadsTable } from '../components/LeadsTable';
import { Lead } from '../types';

interface LeadsViewProps {
  leads: Lead[];
  onSelectLead: (lead: Lead) => void;
  onDownloadPackage?: (leadId: string) => void;
  onToggleUsed?: (leadId: string, currentlyUsed: boolean) => void;
  onRefresh?: () => void;
  defaultPriority?: string;
}

export const LeadsView: React.FC<LeadsViewProps> = ({
  leads,
  onSelectLead,
  onDownloadPackage,
  onToggleUsed,
  onRefresh,
  defaultPriority = 'ALL'
}) => {
  const [priorityFilter, setPriorityFilter] = useState(defaultPriority);
  const [searchTerm, setSearchTerm] = useState('');
  const [websiteFilter, setWebsiteFilter] = useState('ALL');
  const [whatsappFilter, setWhatsappFilter] = useState('ALL');

  const [usedFilter, setUsedFilter] = useState<'ACTIVE' | 'USED' | 'ALL'>('ACTIVE');

  // Compute counts for active vs used leads
  const activeLeadsCount = leads.filter((l) => !l.is_used).length;
  const usedLeadsCount = leads.filter((l) => !!l.is_used).length;

  const filteredLeads = leads.filter((lead) => {
    // Used filter: By default, only show ACTIVE un-used leads (minus used)
    if (usedFilter === 'ACTIVE' && lead.is_used) return false;
    if (usedFilter === 'USED' && !lead.is_used) return false;

    // Priority filter
    if (priorityFilter !== 'ALL' && lead.priority !== priorityFilter) return false;
    // Website filter
    if (websiteFilter !== 'ALL' && lead.website_status !== websiteFilter) return false;
    // WhatsApp filter
    if (whatsappFilter !== 'ALL' && lead.whatsapp_status !== whatsappFilter) return false;
    // Search term
    if (searchTerm.trim() !== '') {
      const term = searchTerm.toLowerCase();
      const matchName = lead.business_name.toLowerCase().includes(term);
      const matchCat = lead.category.toLowerCase().includes(term);
      const matchLoc = (lead.location || '').toLowerCase().includes(term);
      if (!matchName && !matchCat && !matchLoc) return false;
    }
    return true;
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-extrabold tracking-tight text-white">Verified Leads Database</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Showing <strong className="text-emerald-400 font-bold">{filteredLeads.length}</strong> active opportunities (from {activeLeadsCount} available
            {usedLeadsCount > 0 ? `, ${usedLeadsCount} deducted as used` : ''})
          </p>
        </div>

        <div className="flex items-center space-x-2">
          {/* Active vs Used Toggle Pill */}
          <div className="inline-flex rounded-xl bg-slate-900/90 border border-slate-800 p-1 text-xs">
            <button
              onClick={() => setUsedFilter('ACTIVE')}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all ${
                usedFilter === 'ACTIVE'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Active ({activeLeadsCount})
            </button>
            <button
              onClick={() => setUsedFilter('USED')}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all ${
                usedFilter === 'USED'
                  ? 'bg-rose-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-rose-300'
              }`}
            >
              Used ({usedLeadsCount})
            </button>
            <button
              onClick={() => setUsedFilter('ALL')}
              className={`px-3 py-1.5 rounded-lg font-semibold transition-all ${
                usedFilter === 'ALL'
                  ? 'bg-slate-800 text-white shadow-sm'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              All ({leads.length})
            </button>
          </div>

          {onRefresh && (
            <button
              onClick={onRefresh}
              className="flex items-center space-x-1.5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-300 transition-colors"
            >
              <RefreshCw className="h-3.5 w-3.5" />
              <span>Refresh</span>
            </button>
          )}
        </div>
      </div>

      {/* Priority Tabs */}
      <div className="flex border-b border-slate-800 space-x-2 text-xs font-semibold overflow-x-auto">
        {[
          { id: 'ALL', label: 'All Categories' },
          { id: 'P1', label: 'Priority 1 (New Website)', color: 'text-emerald-400 border-emerald-500' },
          { id: 'P2', label: 'Priority 2 (Redesign / Rebuild)', color: 'text-blue-400 border-blue-500' },
          { id: 'EXCLUDED', label: 'Excluded', color: 'text-slate-400 border-slate-500' },
        ].map((tab) => {
          const isActive = priorityFilter === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setPriorityFilter(tab.id)}
              className={`py-3 px-4 border-b-2 transition-all whitespace-nowrap ${
                isActive
                  ? tab.color || 'border-blue-500 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Search & Filter Toolbar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="relative">
          <Search className="absolute left-3.5 top-3 h-4 w-4 text-slate-500" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search business name, category, or city..."
            className="w-full rounded-xl border border-slate-800 bg-slate-900/80 pl-10 pr-4 py-2.5 text-xs text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none"
          />
        </div>

        <div>
          <select
            value={websiteFilter}
            onChange={(e) => setWebsiteFilter(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-2.5 text-xs text-slate-300 focus:border-blue-500 focus:outline-none"
          >
            <option value="ALL">All Website Statuses</option>
            <option value="NO_WEBSITE">No Official Website</option>
            <option value="OUTDATED_WEAK">Outdated / Weak Website</option>
            <option value="OFFICIAL_WEBSITE">Has Official Website</option>
          </select>
        </div>

        <div>
          <select
            value={whatsappFilter}
            onChange={(e) => setWhatsappFilter(e.target.value)}
            className="w-full rounded-xl border border-slate-800 bg-slate-900/80 px-3 py-2.5 text-xs text-slate-300 focus:border-blue-500 focus:outline-none"
          >
            <option value="ALL">All WhatsApp Statuses</option>
            <option value="WHATSAPP_VERIFIED">Verified WhatsApp</option>
            <option value="WHATSAPP_POSSIBLE">Possible WhatsApp</option>
            <option value="PHONE_ONLY">Phone Only</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <LeadsTable
        leads={filteredLeads}
        onSelectLead={onSelectLead}
        onDownloadPackage={onDownloadPackage}
        onToggleUsed={onToggleUsed}
      />
    </div>
  );
};
