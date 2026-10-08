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
      <div className="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-r from-blue-950/40 via-indigo-950/30 to-[#0A0F1D] px-6 py-5 shadow-xl backdrop-blur-xl">
        <div className="flex flex-col sm:flex-row sm:items-center space-y-4 sm:space-y-0 sm:space-x-5">
          <img 
            src="/digi-logo.png" 
            alt="DIGIFORMATION LTD Logo" 
            className="h-16 w-16 rounded-xl object-contain shadow-xl border border-slate-700/60 bg-slate-900/60 p-1"
          />
          <div className="space-y-1">
            <div className="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-2.5 py-0.5 text-xs font-semibold text-blue-400">
              <Sparkles className="h-3 w-3" />
              <span>Official Product of DIGIFORMATION LTD</span>
            </div>
            <h1 className="text-2xl font-extrabold tracking-tight text-white">
              DIGI LEAD HUNTER
            </h1>
            <p className="text-xs text-slate-400 font-medium">
              by <strong className="text-white">DIGIFORMATION LTD</strong> • Sponsored by Digi Biz OS
            </p>
            <p className="text-xs text-slate-300 max-w-xl leading-relaxed">
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
              href="https://wa.me/923164467464?text=Hello%20DIGIFORMATION%20LTD%2C%20I%20am%20inquiring%20about%20Lead%20Hunter"
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
                <a href="mailto:info@digiformation.co.uk" className="text-blue-300 hover:underline">
                  info@digiformation.co.uk
                </a>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-slate-400">Digi Biz:</span>
                <a href="mailto:info@digibizos.co.uk" className="text-indigo-300 hover:underline">
                  info@digibizos.co.uk
                </a>
              </div>
            </div>
            <p className="text-slate-300 text-xs">
              Inquiries regarding enterprise licensing, white-collar partnerships, and bespoke AI development.
            </p>
          </div>
        </div>
      </div>

      {/* Official Web Portals & Company Registry */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
          <Globe className="h-4 w-4 text-sky-400" />
          <span>Web Portals & Official Ecosystem</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
          {/* Box 1: Official UK Companies House Registry */}
          <a
            href="https://find-and-update.company-information.service.gov.uk/company/16994903"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-blue-500/30 bg-blue-950/20 p-4 hover:border-blue-400/50 hover:bg-blue-900/30 transition-all hover:scale-[1.01] group"
          >
            <div>
              <div className="font-bold text-white group-hover:text-blue-300 transition-colors">Companies House UK</div>
              <div className="text-[11px] text-blue-300 font-mono">Company # 16994903</div>
              <div className="text-[10px] text-slate-400 mt-0.5">Official UK Registry</div>
            </div>
            <ExternalLink className="h-4 w-4 text-blue-400 group-hover:text-blue-300 flex-shrink-0" />
          </a>

          {/* Box 2: DIGIFORMATION LTD Corporate Website */}
          <a
            href="https://www.digiformation.co.uk/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0F172A]/80 p-4 hover:border-slate-700 hover:bg-slate-850 transition-all hover:scale-[1.01] group"
          >
            <div>
              <div className="font-bold text-white group-hover:text-sky-300 transition-colors">DIGIFORMATION LTD</div>
              <div className="text-[11px] text-slate-400 font-mono">www.digiformation.co.uk</div>
              <div className="text-[10px] text-slate-500 mt-0.5">Corporate Website</div>
            </div>
            <ExternalLink className="h-4 w-4 text-slate-500 group-hover:text-sky-400 flex-shrink-0" />
          </a>

          {/* Box 3: Digi Biz OS Platform */}
          <a
            href="https://www.digibizos.co.uk/"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0F172A]/80 p-4 hover:border-slate-700 hover:bg-slate-850 transition-all hover:scale-[1.01] group"
          >
            <div>
              <div className="font-bold text-white group-hover:text-indigo-300 transition-colors">Digi Biz OS Platform</div>
              <div className="text-[11px] text-slate-400 font-mono">www.digibizos.co.uk</div>
              <div className="text-[10px] text-slate-500 mt-0.5">Business OS Suite</div>
            </div>
            <ExternalLink className="h-4 w-4 text-slate-500 group-hover:text-indigo-400 flex-shrink-0" />
          </a>

          {/* Box 4: Official Linktree */}
          <a
            href="https://linktr.ee/digiformationltd"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between rounded-xl border border-slate-800 bg-[#0F172A]/80 p-4 hover:border-slate-700 hover:bg-slate-850 transition-all hover:scale-[1.01] group"
          >
            <div>
              <div className="font-bold text-white group-hover:text-emerald-300 transition-colors">Official Linktree</div>
              <div className="text-[11px] text-slate-400 font-mono">linktr.ee/digiformationltd</div>
              <div className="text-[10px] text-slate-500 mt-0.5">All Verified Links</div>
            </div>
            <ExternalLink className="h-4 w-4 text-slate-500 group-hover:text-emerald-400 flex-shrink-0" />
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
            <strong>Digi Biz OS — Lead Hunter</strong> is published under the <em>DIGIFORMATION LTD Source-Available (Personal & Internal Use) License</em>.
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
                <li>DIGIFORMATION LTD branding & copyright must remain intact.</li>
              </ul>
            </div>
          </div>

          <p className="text-[11px] text-slate-500 pt-2 border-t border-slate-800">
            © 2026 DIGIFORMATION LTD. All Rights Reserved. Digi Biz OS is a registered product identity.
          </p>
        </div>
      </div>
    </div>
  );
};
