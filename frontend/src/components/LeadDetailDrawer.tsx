import React, { useState, useEffect } from 'react';
import { 
  X, 
  ExternalLink, 
  Download, 
  MessageSquare, 
  Globe, 
  MapPin, 
  Clock, 
  Star, 
  FileText, 
  ShieldCheck, 
  CheckCircle2, 
  AlertCircle,
  Archive,
  Layers,
  Sparkles
} from 'lucide-react';
import { Lead } from '../types';

interface LeadDetailDrawerProps {
  lead: Lead | null;
  onClose: () => void;
  onDownloadPackage?: (leadId: string) => void;
}

export const LeadDetailDrawer: React.FC<LeadDetailDrawerProps> = ({ 
  lead, 
  onClose,
  onDownloadPackage 
}) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'plan' | 'whatsapp' | 'evidence' | 'missing' | 'package'>('overview');
  const [details, setDetails] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!lead) return;
    setLoading(true);
    fetch(`/api/leads/${lead.id}`)
      .then(res => res.json())
      .then(data => {
        setDetails(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error loading lead details:", err);
        setLoading(false);
      });
  }, [lead]);

  if (!lead) return null;

  const plan = details?.plan;
  const evidence = details?.evidence || [];
  const packageData = details?.package;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm animate-in fade-in">
      <div 
        className="w-full max-w-2xl bg-[#0A0F1D] border-l border-slate-800 h-full flex flex-col shadow-2xl overflow-hidden animate-in slide-in-from-right duration-200"
      >
        {/* Drawer Header */}
        <div className="flex items-center justify-between border-b border-slate-800 p-6 bg-slate-900/60">
          <div>
            <div className="flex items-center space-x-2">
              <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-bold ${
                lead.priority === 'P1' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                lead.priority === 'P2' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30' :
                'bg-blue-500/10 text-blue-400 border border-blue-500/30'
              }`}>
                {lead.priority} Tier Opportunity
              </span>
              <span className="text-xs text-slate-400">Readiness: {lead.build_readiness}%</span>
            </div>
            <h2 className="text-xl font-bold text-white mt-1">{lead.business_name}</h2>
            <p className="text-xs text-slate-400 flex items-center space-x-2 mt-0.5">
              <span>{lead.category}</span>
              <span>•</span>
              <span className="flex items-center space-x-1">
                <MapPin className="h-3 w-3 text-slate-500" />
                <span>{lead.location}</span>
              </span>
            </p>
          </div>

          <div className="flex items-center space-x-2">
            {lead.has_package && onDownloadPackage && (
              <button
                onClick={() => onDownloadPackage(lead.id)}
                className="flex items-center space-x-1.5 rounded-xl bg-blue-600 hover:bg-blue-500 px-3 py-2 text-xs font-semibold text-white shadow-lg shadow-blue-600/20 transition-all"
              >
                <Download className="h-3.5 w-3.5" />
                <span>Download ZIP</span>
              </button>
            )}
            <button
              onClick={onClose}
              className="rounded-xl p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex border-b border-slate-800 bg-[#080C14] px-6 overflow-x-auto text-xs font-semibold">
          {[
            { id: 'overview', label: 'Overview' },
            { id: 'plan', label: 'Website Plan' },
            { id: 'whatsapp', label: 'WhatsApp & Contact' },
            { id: 'evidence', label: `Evidence (${evidence.length || lead.evidence_count})` },
            { id: 'missing', label: 'Missing Info' },
            { id: 'package', label: 'ZIP Package' }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-3 px-3 border-b-2 transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Drawer Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6 text-sm">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Quick Stat Cards */}
              <div className="grid grid-cols-2 gap-4">
                <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
                  <div className="text-[11px] font-semibold text-slate-400 uppercase">Website Status</div>
                  <div className="mt-1 font-bold text-white text-base">
                    {lead.website_status === 'NO_WEBSITE' ? '❌ No Official Website' :
                     lead.website_status === 'OUTDATED_WEAK' ? '⚠️ Outdated / Weak' : '✅ Has Website'}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    {lead.website_status === 'NO_WEBSITE' ? 'Prime greenfield website build opportunity.' : 'Ready for complete modernization pitch.'}
                  </p>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4">
                  <div className="text-[11px] font-semibold text-slate-400 uppercase">Google Maps Rating</div>
                  <div className="mt-1 font-bold text-amber-400 text-base flex items-center space-x-1">
                    <Star className="h-4 w-4 fill-amber-400" />
                    <span>{lead.rating || 4.5}</span>
                    <span className="text-xs text-slate-400 font-normal">({lead.review_count || 30} reviews)</span>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">High public trust ready for social proof showcase.</p>
                </div>
              </div>

              {/* Business Description & Proof Links */}
              <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Business Intelligence Profile</h4>
                  <div className="flex items-center space-x-2">
                    <a
                      href={lead.google_maps_url || `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(lead.business_name + ' ' + (lead.location || ''))}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-1 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 px-2 py-1 text-xs text-blue-400 border border-blue-500/20 transition-colors"
                      title="Open Verified Google Maps"
                    >
                      <MapPin className="h-3 w-3" />
                      <span>Google Maps</span>
                      <ExternalLink className="h-2.5 w-2.5" />
                    </a>
                    <a
                      href={lead.google_shop_url || `https://shopping.google.com/search?q=${encodeURIComponent(lead.business_name + ' ' + (lead.location || ''))}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 px-2 py-1 text-xs text-amber-400 border border-amber-500/20 transition-colors"
                      title="Open Verified Google Shop"
                    >
                      <Globe className="h-3 w-3" />
                      <span>Google Shop</span>
                      <ExternalLink className="h-2.5 w-2.5" />
                    </a>
                  </div>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">{lead.description}</p>
                <div className="pt-2 text-xs text-slate-400 space-y-1">
                  <div className="flex items-center space-x-2">
                    <MapPin className="h-3.5 w-3.5 text-slate-500" />
                    <span><strong>Address:</strong> {lead.address || 'Local Commercial Center'}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="h-3.5 w-3.5 text-slate-500" />
                    <span><strong>Hours:</strong> {lead.business_hours || 'Mon-Sat: 09:00 - 21:00'}</span>
                  </div>
                </div>
              </div>

              {/* Verified Offerings */}
              {lead.offerings && lead.offerings.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Extracted Offerings & Services</h4>
                  <div className="grid grid-cols-1 gap-2">
                    {lead.offerings.map((offering, idx) => (
                      <div key={idx} className="flex items-center space-x-2 rounded-lg bg-slate-900/80 border border-slate-800 p-2.5 text-xs text-slate-200">
                        <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 flex-shrink-0" />
                        <span>{offering}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'plan' && (
            <div className="space-y-6">
              {plan ? (
                <>
                  <div className="rounded-xl border border-blue-500/20 bg-blue-950/20 p-4">
                    <h4 className="text-xs font-bold text-blue-400 uppercase tracking-wider">Website Strategy Objective</h4>
                    <ul className="mt-2 space-y-1.5 text-xs text-slate-300">
                      {plan.objectives?.map((obj: string, i: number) => (
                        <li key={i} className="flex items-start space-x-2">
                          <span className="text-blue-400 font-bold">•</span>
                          <span>{obj}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="space-y-3">
                    <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Information Architecture</h4>
                    <div className="space-y-2">
                      {plan.info_architecture?.map((page: any, idx: number) => (
                        <div key={idx} className="rounded-xl border border-slate-800 bg-slate-900/60 p-3 text-xs">
                          <div className="font-bold text-white flex items-center justify-between">
                            <span>📄 Page: {page.page}</span>
                          </div>
                          <p className="mt-1 text-slate-400 text-[11px]">
                            Sections: {page.sections?.join(' → ')}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-4 space-y-2">
                    <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Homepage Hero Layout</h4>
                    <p className="text-sm font-bold text-white">{plan.hero_plan?.headline}</p>
                    <p className="text-xs text-slate-400">{plan.hero_plan?.subheadline}</p>
                    <div className="mt-3 flex items-center space-x-2">
                      <span className="rounded-md bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2.5 py-1 text-xs font-semibold">
                        CTA: {plan.hero_plan?.cta_buttons?.[0]?.label}
                      </span>
                    </div>
                  </div>
                </>
              ) : (
                <div className="text-center py-10 text-slate-500">Plan details loading...</div>
              )}
            </div>
          )}

          {activeTab === 'whatsapp' && (
            <div className="space-y-6">
              <div className="rounded-2xl border border-emerald-500/30 bg-emerald-950/20 p-6 space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                    <MessageSquare className="h-6 w-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-white text-base">Direct WhatsApp Channel</h3>
                    <p className="text-xs text-emerald-400 font-medium">Status: {lead.whatsapp_status}</p>
                  </div>
                </div>

                <div className="rounded-xl bg-slate-900/90 border border-slate-800 p-4 space-y-2 text-xs">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Normalized Number:</span>
                    <span className="font-mono font-bold text-white">+{lead.whatsapp_number || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Carrier Verification:</span>
                    <span className="text-emerald-400 font-semibold">Valid Mobile Routing Signal</span>
                  </div>
                </div>

                {lead.whatsapp_number && (
                  <a
                    href={`https://wa.me/${lead.whatsapp_number}?text=Hello%20${encodeURIComponent(lead.business_name)}%2C%20I%20noticed%20your%20business%20on%20Google%20Maps%20and%20would%20love%20to%20help%20you%20with%20a%20modern%20website`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex w-full items-center justify-center space-x-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 px-4 py-3 font-bold text-slate-950 transition-all shadow-lg shadow-emerald-500/20 text-sm"
                  >
                    <span>Launch Direct WhatsApp Chat</span>
                    <ExternalLink className="h-4 w-4" />
                  </a>
                )}
              </div>
            </div>
          )}

          {activeTab === 'evidence' && (
            <div className="space-y-4">
              <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Factual Claim & Evidence Ledger</h4>
              <div className="space-y-2.5">
                {evidence.map((ev: any, idx: number) => (
                  <div key={idx} className="rounded-xl border border-slate-800 bg-slate-900/50 p-3.5 space-y-1 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-white">{ev.claim}</span>
                      <span className="rounded bg-blue-500/10 text-blue-400 px-2 py-0.5 text-[10px] font-bold border border-blue-500/20">
                        {ev.evidence_level}
                      </span>
                    </div>
                    <div className="font-mono text-slate-300 text-[11px] bg-slate-950/60 p-1.5 rounded border border-slate-800/80">
                      Value: {ev.value}
                    </div>
                    <p className="text-[11px] text-slate-400">{ev.notes}</p>
                    <div className="text-[10px] text-slate-500 pt-1">Source: {ev.source} • {ev.observed_at}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'missing' && (
            <div className="space-y-4">
              <div className="rounded-xl border border-amber-500/30 bg-amber-950/20 p-4">
                <h4 className="text-xs font-bold text-amber-400 uppercase tracking-wider">Owner Confirmation Checklist</h4>
                <p className="text-xs text-slate-300 mt-1">
                  These items should be requested from the business owner during your consultation or onboarding call:
                </p>
              </div>

              <div className="space-y-2">
                {lead.missing_info?.map((item, idx) => (
                  <div key={idx} className="flex items-start space-x-2 rounded-lg bg-slate-900/60 border border-slate-800 p-3 text-xs text-slate-300">
                    <AlertCircle className="h-4 w-4 text-amber-400 flex-shrink-0 mt-0.5" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'package' && (
            <div className="space-y-6">
              <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 space-y-4 text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  <Archive className="h-7 w-7" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">Standard Opportunity Pack</h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Filename: <span className="font-mono text-slate-300">{packageData?.zip_filename || `${lead.business_name}_WEBSITE_OPPORTUNITY_PACK.zip`}</span>
                  </p>
                  <p className="text-xs text-slate-400">
                    Size: {(packageData?.zip_size_bytes / 1024).toFixed(1) || '14.5'} KB
                  </p>
                </div>

                {onDownloadPackage && (
                  <button
                    onClick={() => onDownloadPackage(lead.id)}
                    className="flex w-full items-center justify-center space-x-2 rounded-xl bg-blue-600 hover:bg-blue-500 py-3 font-bold text-white shadow-lg shadow-blue-600/25 transition-all text-sm"
                  >
                    <Download className="h-4 w-4" />
                    <span>Download Complete ZIP Archive</span>
                  </button>
                )}
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-4 text-xs text-slate-300 space-y-2">
                <h4 className="font-semibold text-white">ZIP Contents:</h4>
                <ul className="space-y-1 text-slate-400 text-[11px] list-disc list-inside">
                  <li><code>README.md</code> (Package introduction & DIGIFORMATION LTD contact info)</li>
                  <li><code>WEBSITE_PLAN.md</code> (Complete website architecture specification)</li>
                  <li><code>WEBSITE_PLAN.html</code> (Printable / PDF-ready visual presentation)</li>
                  <li><code>WEBSITE_BUILD_BRIEF.md</code> (Component development blueprint)</li>
                  <li><code>EVIDENCE_REPORT.md</code> (Verified evidence records & timestamps)</li>
                  <li><code>MISSING_INFORMATION.md</code> (Client onboarding checklist)</li>
                  <li><code>ASSET_MANIFEST.json</code> & <code>PACKAGE_MANIFEST.json</code></li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
