import React from 'react';
import { 
  Building2, 
  MessageSquare, 
  Mail, 
  Globe, 
  ExternalLink, 
  ShieldCheck, 
  FileText, 
  Award,
  Sparkles,
  Lock,
  Phone
} from 'lucide-react';

export const AboutView: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-in fade-in duration-300">
      {/* Brand Header Banner */}
      <div className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-r from-blue-950/40 via-indigo-950/30 to-[#0A0F1D] p-8 shadow-2xl backdrop-blur-xl">
        <div className="flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-6">
          <img 
            src="/digi-logo.png" 
            alt="Digiformation LTD Logo" 
            className="h-20 w-20 rounded-2xl object-contain shadow-2xl border border-slate-700/60 bg-slate-900/60 p-1"
          />
          <div className="space-y-1.5">
            <div className="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-400">
              <Sparkles className="h-3.5 w-3.5" />
              <span>Official Product of Digiformation LTD</span>
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white">
              DIGI LEAD HUNTER
            </h1>
            <p className="text-xs text-slate-400 font-medium">
              by <strong className="text-white">Digiformation LTD</strong> • Sponsored by Digi Biz OS
            </p>
            <p className="text-xs text-slate-300 max-w-xl leading-relaxed pt-1">
              AI-driven Local Business Lead Intelligence, Website Opportunity Research & Automated Packaging Engine.
            </p>
          </div>
        </div>
      </div>

      {/* Official Contact Directory */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <Phone className="h-4 w-4 text-emerald-400" />
          <span>Official Contacts & Support Channels</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          {/* WhatsApp Card */}
          <div className="rounded-2xl border border-emerald-500/30 bg-emerald-950/20 p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-emerald-400 uppercase tracking-wider text-[11px]">Primary WhatsApp Hotline</span>
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>
            <div className="text-xl font-mono font-bold text-white">
              +92 316 4467464
            </div>
            <p className="text-slate-300 text-xs">
              Direct technical support, custom enterprise lead queries, and consulting assistance.
            </p>
            <a
              href="https://wa.me/923164467464?text=Hello%20Digi%20Formation%2C%20I%20am%20inquiring%20about%20Lead%20Hunter"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 px-4 py-2 font-bold text-slate-950 transition-all text-xs shadow-md shadow-emerald-500/20"
            >
              <MessageSquare className="h-4 w-4" />
              <span>Open WhatsApp Chat</span>
            </a>
          </div>

          {/* Email Card */}
          <div className="rounded-2xl border border-blue-500/30 bg-blue-950/20 p-5 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-blue-400 uppercase tracking-wider text-[11px]">Official Email Communications</span>
              <Mail className="h-4 w-4 text-blue-400" />
            </div>
            <div className="space-y-1.5 font-mono text-white text-xs">
              <div className="flex items-center space-x-2">
                <span className="text-slate-400">Corporate:</span>
                <a href="mailto:digiformation.info@digiformation.co.uk" className="text-blue-300 hover:underline">
                  digiformation.info@digiformation.co.uk
                </a>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-slate-400">Digi Biz:</span>
                <a href="mailto:info@digibizwiz.co.uk" className="text-indigo-300 hover:underline">
                  info@digibizwiz.co.uk
                </a>
              </div>
            </div>
            <p className="text-slate-300 text-xs">
              Inquiries regarding enterprise licensing, white-collar partnerships, and bespoke AI development.
            </p>
          </div>
        </div>
      </div>

      {/* Official Web Portals */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <Globe className="h-4 w-4 text-sky-400" />
          <span>Web Portals & Official Ecosystem</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs">
          <a
            href="https://www.digiformation.co.uk/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0F172A]/80 p-4 hover:border-slate-700 transition-all hover:scale-[1.01]"
          >
            <div>
              <div className="font-bold text-white">Digi Formation UK</div>
              <div className="text-[11px] text-slate-400">www.digiformation.co.uk</div>
            </div>
            <ExternalLink className="h-4 w-4 text-slate-500" />
          </a>

          <a
            href="https://www.digibizos.co.uk/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0F172A]/80 p-4 hover:border-slate-700 transition-all hover:scale-[1.01]"
          >
            <div>
              <div className="font-bold text-white">Digi Biz OS Platform</div>
              <div className="text-[11px] text-slate-400">www.digibizos.co.uk</div>
            </div>
            <ExternalLink className="h-4 w-4 text-slate-500" />
          </a>

          <a
            href="https://linktr.ee/digiformationltd"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0F172A]/80 p-4 hover:border-slate-700 transition-all hover:scale-[1.01]"
          >
            <div>
              <div className="font-bold text-white">Official Linktree</div>
              <div className="text-[11px] text-slate-400">linktr.ee/digiformationltd</div>
            </div>
            <ExternalLink className="h-4 w-4 text-slate-500" />
          </a>
        </div>
      </div>

      {/* License & Brand Protection Terms */}
      <div className="rounded-2xl border border-slate-800 bg-[#0F172A]/90 p-6 space-y-4">
        <div className="flex items-center space-x-2 text-white font-bold text-sm">
          <ShieldCheck className="h-5 w-5 text-blue-400" />
          <span>Source-Available License & Brand Ownership Notice</span>
        </div>

        <div className="text-xs text-slate-300 space-y-3 leading-relaxed">
          <p>
            <strong>Digi Biz OS — Lead Hunter</strong> is published under the <em>Digiformation LTD Source-Available (Personal & Internal Use) License</em>.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            <div className="rounded-xl border border-emerald-500/20 bg-emerald-950/10 p-3.5 space-y-1.5">
              <span className="font-bold text-emerald-400 flex items-center space-x-1.5">
                <span>✅ Permitted Actions:</span>
              </span>
              <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px]">
                <li>Inspect and download the complete source code.</li>
                <li>Run locally for personal lead discovery and outreach.</li>
                <li>Use internally for your own agency or business workflow.</li>
                <li>Modify code for private internal enhancements.</li>
              </ul>
            </div>

            <div className="rounded-xl border border-rose-500/20 bg-rose-950/10 p-3.5 space-y-1.5">
              <span className="font-bold text-rose-400 flex items-center space-x-1.5">
                <span>❌ Strict Restrictions:</span>
              </span>
              <ul className="list-disc list-inside text-slate-300 space-y-1 text-[11px]">
                <li>No commercial resale or selling modified copies.</li>
                <li>No offering as a paid SaaS or hosted service.</li>
                <li>No white-labeling or rebranding as your own tool.</li>
                <li>Digiformation LTD branding & copyright must remain intact.</li>
              </ul>
            </div>
          </div>

          <p className="text-[11px] text-slate-500 pt-2 border-t border-slate-800">
            © 2026 Digiformation LTD. All Rights Reserved. Digi Biz OS is a registered product identity.
          </p>
        </div>
      </div>
    </div>
  );
};
