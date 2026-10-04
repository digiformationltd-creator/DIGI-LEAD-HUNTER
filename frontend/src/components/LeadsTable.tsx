import React from 'react';
import { 
  ExternalLink, 
  Download, 
  Eye, 
  MessageSquare, 
  Globe, 
  MapPin, 
  ShieldCheck, 
  AlertCircle,
  FileCheck
} from 'lucide-react';
import { Lead } from '../types';

interface LeadsTableProps {
  leads: Lead[];
  onSelectLead: (lead: Lead) => void;
  onDownloadPackage?: (leadId: string) => void;
}

export const LeadsTable: React.FC<LeadsTableProps> = ({ 
  leads, 
  onSelectLead, 
  onDownloadPackage 
}) => {
  if (leads.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center rounded-2xl border border-slate-800 bg-[#0F172A]/50 p-12 text-center backdrop-blur-md">
        <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-slate-800 text-slate-400">
          <Globe className="h-6 w-6" />
        </div>
        <h3 className="mt-4 text-base font-semibold text-white">No Leads Found</h3>
        <p className="mt-1 text-xs text-slate-400 max-w-sm">
          Run a new Lead Hunt search for your target category and location to discover website opportunities.
        </p>
      </div>
    );
  }

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'P1':
        return <span className="inline-flex items-center rounded-md bg-emerald-500/10 px-2.5 py-1 text-xs font-bold text-emerald-400 border border-emerald-500/30">P1 • New Website</span>;
      case 'P2':
        return <span className="inline-flex items-center rounded-md bg-blue-500/10 px-2.5 py-1 text-xs font-bold text-blue-400 border border-blue-500/30">P2 • Redesign</span>;
      default:
        return <span className="inline-flex items-center rounded-md bg-slate-800 px-2 py-1 text-xs font-medium text-slate-400">Excluded</span>;
    }
  };

  const getWhatsAppBadge = (status: string, number?: string) => {
    if (status === 'WHATSAPP_VERIFIED') {
      return (
        <a
          href={`https://wa.me/${number}`}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center space-x-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 px-2 py-1 text-xs font-semibold text-emerald-400 hover:bg-emerald-500/20 transition-all"
          title="Direct WhatsApp Verified"
        >
          <MessageSquare className="h-3 w-3" />
          <span>+{number}</span>
        </a>
      );
    }
    if (status === 'WHATSAPP_POSSIBLE') {
      return (
        <span className="inline-flex items-center space-x-1 rounded-md bg-teal-500/10 px-2 py-1 text-xs font-medium text-teal-400 border border-teal-500/20">
          <span>+{number || 'Possible'}</span>
        </span>
      );
    }
    return <span className="text-xs text-slate-500">Phone Only</span>;
  };

  const getWebsiteBadge = (status: string, url?: string) => {
    if (status === 'NO_WEBSITE') {
      return (
        <span className="inline-flex items-center space-x-1 rounded-md bg-rose-500/10 px-2 py-1 text-xs font-bold text-rose-400 border border-rose-500/20">
          <AlertCircle className="h-3 w-3" />
          <span>No Website</span>
        </span>
      );
    }
    if (status === 'OUTDATED_WEAK') {
      return (
        <span className="inline-flex items-center space-x-1 rounded-md bg-blue-500/10 px-2 py-1 text-xs font-bold text-blue-400 border border-blue-500/20" title={url}>
          <span>Outdated / Weak</span>
        </span>
      );
    }
    return (
      <a 
        href={url} 
        target="_blank" 
        rel="noopener noreferrer"
        className="inline-flex items-center space-x-1 text-xs text-slate-400 hover:text-white truncate max-w-[120px]"
      >
        <span className="truncate">{url}</span>
        <ExternalLink className="h-2.5 w-2.5 flex-shrink-0" />
      </a>
    );
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0F172A]/70 backdrop-blur-xl shadow-xl">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900/60 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              <th className="py-3.5 px-4">Business Details</th>
              <th className="py-3.5 px-3">Priority</th>
              <th className="py-3.5 px-3">Website Status</th>
              <th className="py-3.5 px-3">WhatsApp Channel</th>
              <th className="py-3.5 px-3">Build Readiness</th>
              <th className="py-3.5 px-3">Evidence</th>
              <th className="py-3.5 px-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {leads.map((lead) => (
              <tr 
                key={lead.id} 
                className="hover:bg-slate-800/40 transition-colors group cursor-pointer"
                onClick={() => onSelectLead(lead)}
              >
                <td className="py-3.5 px-4">
                  <div className="font-semibold text-white group-hover:text-blue-400 transition-colors">
                    {lead.business_name}
                  </div>
                  <div className="flex items-center space-x-2 text-[11px] text-slate-400 mt-0.5">
                    <span className="text-slate-300 font-medium">{lead.category}</span>
                    <span>•</span>
                    <span className="flex items-center space-x-0.5">
                      <MapPin className="h-3 w-3 text-slate-500" />
                      <span>{lead.location || 'Local Area'}</span>
                    </span>
                    {lead.rating && (
                      <>
                        <span>•</span>
                        <span className="text-amber-400 font-bold">★ {lead.rating}</span>
                      </>
                    )}
                  </div>
                </td>

                <td className="py-3.5 px-3">
                  {getPriorityBadge(lead.priority)}
                </td>

                <td className="py-3.5 px-3">
                  {getWebsiteBadge(lead.website_status, lead.website_url)}
                </td>

                <td className="py-3.5 px-3">
                  {getWhatsAppBadge(lead.whatsapp_status, lead.whatsapp_number)}
                </td>

                <td className="py-3.5 px-3">
                  <div className="flex items-center space-x-2">
                    <div className="h-2 w-16 rounded-full bg-slate-800 overflow-hidden">
                      <div 
                        className={`h-full rounded-full ${
                          lead.build_readiness >= 80 ? 'bg-emerald-500' :
                          lead.build_readiness >= 50 ? 'bg-amber-500' : 'bg-blue-500'
                        }`}
                        style={{ width: `${lead.build_readiness}%` }}
                      ></div>
                    </div>
                    <span className="text-[11px] font-bold text-slate-300">{lead.build_readiness}%</span>
                  </div>
                </td>

                <td className="py-3.5 px-3">
                  <div className="flex flex-col space-y-1">
                    <span className="inline-flex items-center space-x-1 text-slate-400 text-[11px]">
                      <ShieldCheck className="h-3.5 w-3.5 text-blue-400" />
                      <span>{lead.evidence_count} claims</span>
                    </span>
                    <div className="flex items-center space-x-2 pt-0.5" onClick={(e) => e.stopPropagation()}>
                      {lead.google_maps_url ? (
                        <a
                          href={lead.google_maps_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center space-x-1 rounded bg-slate-800 hover:bg-slate-700 px-1.5 py-0.5 text-[10px] text-blue-400 hover:text-blue-300 transition-colors"
                          title="Verified Google Maps Listing"
                        >
                          <MapPin className="h-2.5 w-2.5" />
                          <span>Maps</span>
                          <ExternalLink className="h-2 w-2" />
                        </a>
                      ) : (
                        <a
                          href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(lead.business_name + ' ' + (lead.location || ''))}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center space-x-1 rounded bg-slate-800 hover:bg-slate-700 px-1.5 py-0.5 text-[10px] text-blue-400 hover:text-blue-300 transition-colors"
                          title="Verify on Google Maps"
                        >
                          <MapPin className="h-2.5 w-2.5" />
                          <span>Maps</span>
                          <ExternalLink className="h-2 w-2" />
                        </a>
                      )}
                      <a
                        href={lead.google_shop_url || `https://shopping.google.com/search?q=${encodeURIComponent(lead.business_name + ' ' + (lead.location || ''))}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center space-x-1 rounded bg-amber-500/10 hover:bg-amber-500/20 px-1.5 py-0.5 text-[10px] text-amber-400 hover:text-amber-300 border border-amber-500/20 transition-colors"
                        title="Direct Google Shop / Shopping Proof"
                      >
                        <Globe className="h-2.5 w-2.5" />
                        <span>Google Shop</span>
                        <ExternalLink className="h-2 w-2" />
                      </a>
                    </div>
                  </div>
                </td>

                <td className="py-3.5 px-4 text-right" onClick={(e) => e.stopPropagation()}>
                  <div className="flex items-center justify-end space-x-2">
                    <button
                      onClick={() => onSelectLead(lead)}
                      className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
                      title="View Plan & Evidence"
                    >
                      <Eye className="h-4 w-4" />
                    </button>
                    {lead.has_package && onDownloadPackage && (
                      <button
                        onClick={() => onDownloadPackage(lead.id)}
                        className="rounded-lg bg-blue-600/10 border border-blue-500/20 p-1.5 text-blue-400 hover:bg-blue-600/20 hover:text-blue-300 transition-colors"
                        title="Download Opportunity ZIP"
                      >
                        <Download className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
