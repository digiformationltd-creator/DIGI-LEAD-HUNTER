import React, { useState } from 'react';
import { 
  ExternalLink, 
  Download, 
  Eye, 
  Globe, 
  MapPin, 
  ShieldCheck, 
  CheckCircle,
  RotateCcw,
  Ban
} from 'lucide-react';
import { Lead } from '../types';

interface LeadsTableProps {
  leads: Lead[];
  onSelectLead: (lead: Lead) => void;
  onDownloadPackage?: (leadId: string) => void;
  onToggleUsed?: (leadId: string, currentlyUsed: boolean) => void;
}

export const LeadsTable: React.FC<LeadsTableProps> = ({ 
  leads, 
  onSelectLead, 
  onDownloadPackage,
  onToggleUsed
}) => {
  const [loadingLeadId, setLoadingLeadId] = useState<string | null>(null);

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

  const handleToggle = async (e: React.MouseEvent, lead: Lead) => {
    e.stopPropagation();
    if (!onToggleUsed) return;
    setLoadingLeadId(lead.id);
    try {
      await onToggleUsed(lead.id, !!lead.is_used);
    } finally {
      setLoadingLeadId(null);
    }
  };

  const handleDownload = (e: React.MouseEvent, leadId: string) => {
    e.stopPropagation();
    if (onDownloadPackage) {
      onDownloadPackage(leadId);
    } else {
      window.open(`/api/packages/lead/${leadId}/download`, '_blank');
    }
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800 bg-[#0F172A]/70 backdrop-blur-xl shadow-xl">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900/60 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              <th className="py-3.5 px-6">Business Details</th>
              <th className="py-3.5 px-6">Evidence</th>
              <th className="py-3.5 px-6 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {leads.map((lead) => {
              const isUsed = !!lead.is_used;
              const isLoading = loadingLeadId === lead.id;

              return (
                <tr 
                  key={lead.id} 
                  className={`transition-colors group cursor-pointer ${
                    isUsed 
                      ? 'bg-rose-950/25 border-l-4 border-rose-500 hover:bg-rose-950/35 text-rose-200' 
                      : 'hover:bg-slate-800/40 text-slate-200'
                  }`}
                  onClick={() => onSelectLead(lead)}
                >
                  {/* Business Details */}
                  <td className="py-4 px-6">
                    <div className="flex items-center space-x-2">
                      <span className={`font-semibold text-sm transition-colors ${
                        isUsed 
                          ? 'text-rose-200 line-through decoration-rose-500/70 group-hover:text-rose-100' 
                          : 'text-white group-hover:text-blue-400'
                      }`}>
                        {lead.business_name}
                      </span>
                      {isUsed && (
                        <span className="inline-flex items-center space-x-1 rounded-md bg-rose-500/20 px-2 py-0.5 text-[10px] font-bold text-rose-300 border border-rose-500/40">
                          <Ban className="h-2.5 w-2.5 text-rose-400" />
                          <span>USED</span>
                        </span>
                      )}
                    </div>
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1 text-[11px] text-slate-400 mt-1">
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
                      {lead.phone && (
                        <>
                          <span>•</span>
                          <span className="text-slate-400">📞 {lead.phone}</span>
                        </>
                      )}
                      {isUsed && lead.used_at && (
                        <>
                          <span>•</span>
                          <span className="text-rose-400 font-mono text-[10px]">
                            Used on {new Date(lead.used_at).toLocaleDateString()}
                          </span>
                        </>
                      )}
                    </div>
                  </td>

                  {/* Evidence */}
                  <td className="py-4 px-6">
                    <div className="flex flex-col space-y-1.5">
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
                            className="inline-flex items-center space-x-1 rounded bg-slate-800 hover:bg-slate-700 px-2 py-0.5 text-[10px] text-blue-400 hover:text-blue-300 transition-colors"
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
                            className="inline-flex items-center space-x-1 rounded bg-slate-800 hover:bg-slate-700 px-2 py-0.5 text-[10px] text-blue-400 hover:text-blue-300 transition-colors"
                            title="Verify on Google Maps"
                          >
                            <MapPin className="h-2.5 w-2.5" />
                            <span>Maps</span>
                            <ExternalLink className="h-2 w-2" />
                          </a>
                        )}
                      </div>
                    </div>
                  </td>

                  {/* Actions */}
                  <td className="py-4 px-5 text-right" onClick={(e) => e.stopPropagation()}>
                    <div className="flex items-center justify-end space-x-2">
                      {/* WhatsApp Action Button — Only active & green when confirmed on WhatsApp */}
                      {lead.whatsapp_number && (lead.whatsapp_verified || lead.whatsapp_confidence === 'CONFIRMED' || lead.whatsapp_status === 'WHATSAPP_CONFIRMED') ? (
                        <a
                          href={`https://wa.me/${lead.whatsapp_number}?text=Hello%20${encodeURIComponent(lead.business_name)}%2C%20I%20noticed%20your%20business%20on%20Google%20Maps%20and%20would%20love%20to%20help%20you%20with%20a%20modern%20website`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center space-x-1.5 rounded-lg bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 px-2.5 py-1.5 text-xs font-semibold text-emerald-400 hover:text-emerald-300 transition-colors shadow-sm"
                          title={`Direct Confirmed WhatsApp to ${lead.business_name} (+${lead.whatsapp_number})`}
                        >
                          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                          <span>WhatsApp ✓</span>
                          <ExternalLink className="h-3 w-3" />
                        </a>
                      ) : lead.phone ? (
                        <span
                          className="inline-flex items-center space-x-1 rounded-lg bg-slate-800/80 border border-slate-700/60 px-2 py-1 text-[11px] font-medium text-slate-400"
                          title="Mobile carrier format valid, but active WhatsApp account not independently confirmed"
                        >
                          <span>Unverified WA</span>
                        </span>
                      ) : null}

                      {/* Mark Used / Reset Toggle */}
                      {onToggleUsed && (
                        <button
                          onClick={(e) => handleToggle(e, lead)}
                          disabled={isLoading}
                          className={`inline-flex items-center space-x-1 rounded-lg px-2.5 py-1.5 text-xs font-semibold transition-all ${
                            isUsed
                              ? 'bg-rose-500/20 border border-rose-500/40 text-rose-300 hover:bg-rose-500/30'
                              : 'bg-slate-800 hover:bg-rose-600/20 hover:border-rose-500/30 border border-slate-700 text-slate-300 hover:text-rose-300'
                          }`}
                          title={isUsed ? "Marked as Used. Click to unmark/reset" : "Mark this lead as Used / Outreached"}
                        >
                          {isUsed ? (
                            <>
                              <RotateCcw className="h-3 w-3 text-rose-400" />
                              <span>Reset</span>
                            </>
                          ) : (
                            <>
                              <CheckCircle className="h-3 w-3 text-emerald-400" />
                              <span>Used</span>
                            </>
                          )}
                        </button>
                      )}

                      {/* Download Opportunity ZIP */}
                      <button
                        onClick={(e) => handleDownload(e, lead.id)}
                        className="inline-flex items-center space-x-1 rounded-lg bg-blue-600/15 border border-blue-500/30 px-2.5 py-1.5 text-xs font-semibold text-blue-400 hover:bg-blue-600/25 hover:text-blue-300 transition-colors shadow-sm"
                        title="Download Opportunity ZIP (Word Docx + Excel Xlsx + Real HD Images + Plan)"
                      >
                        <Download className="h-3.5 w-3.5" />
                        <span className="hidden sm:inline">ZIP</span>
                      </button>

                      {/* Overview Drawer Button */}
                      <button
                        onClick={() => onSelectLead(lead)}
                        className="inline-flex items-center space-x-1 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 px-2 py-1.5 text-xs font-medium text-slate-300 hover:text-white transition-colors"
                        title="View Full Business Overview & Evidence"
                      >
                        <Eye className="h-3.5 w-3.5" />
                        <span className="hidden md:inline">Overview</span>
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
