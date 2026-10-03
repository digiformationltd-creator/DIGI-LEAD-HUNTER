import React, { useState } from 'react';
import { MessageSquare, ExternalLink, X, Phone, Mail, Globe } from 'lucide-react';

export const WhatsAppWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const whatsappNumber = "03164467464";
  const whatsappClean = "923164467464";
  const waUrl = `https://wa.me/${whatsappClean}?text=Hello%20Digi%20Formation%2C%20I%20am%20using%20Lead%20Hunter%20Agent`;

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen && (
        <div className="mb-4 w-80 rounded-2xl bg-[#0F172A] border border-slate-700/80 p-5 shadow-2xl backdrop-blur-xl animate-in fade-in slide-in-from-bottom-5">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <div className="flex items-center space-x-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400">
                <MessageSquare className="h-5 w-5" />
              </div>
              <div>
                <h4 className="text-sm font-semibold text-white">Digi Formation Support</h4>
                <p className="text-xs text-emerald-400 flex items-center space-x-1">
                  <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span>Direct WhatsApp Online</span>
                </p>
              </div>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="rounded-lg p-1 text-slate-400 hover:bg-slate-800 hover:text-white"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          <div className="mt-4 space-y-3 text-xs text-slate-300">
            <p>
              Need assistance with lead discovery, website opportunity packaging, or custom client setups? Reach out directly to our engineering desk.
            </p>
            
            <div className="space-y-1.5 rounded-xl bg-slate-900/80 p-3 border border-slate-800/80">
              <div className="flex items-center space-x-2 text-slate-300">
                <Phone className="h-3.5 w-3.5 text-emerald-400" />
                <span>WhatsApp: <strong>+92 316 4467464</strong></span>
              </div>
              <div className="flex items-center space-x-2 text-slate-300">
                <Mail className="h-3.5 w-3.5 text-sky-400" />
                <span className="truncate">digiformation.info@digiformation.co.uk</span>
              </div>
              <div className="flex items-center space-x-2 text-slate-300">
                <Globe className="h-3.5 w-3.5 text-indigo-400" />
                <span>www.digiformation.co.uk</span>
              </div>
            </div>

            <a
              href={waUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 flex w-full items-center justify-center space-x-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 px-4 py-2.5 font-semibold text-slate-950 transition-all shadow-lg shadow-emerald-500/20"
            >
              <span>Chat on WhatsApp</span>
              <ExternalLink className="h-4 w-4" />
            </a>
          </div>
        </div>
      )}

      <button
        onClick={() => setIsOpen(!isOpen)}
        className="group relative flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-tr from-emerald-600 to-teal-400 text-slate-950 shadow-xl shadow-emerald-500/25 transition-all hover:scale-105 active:scale-95"
        title="WhatsApp Support — 03164467464"
      >
        <span className="absolute -top-1 -right-1 flex h-4 w-4">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex h-4 w-4 rounded-full bg-emerald-300 border-2 border-[#080C14]"></span>
        </span>
        <MessageSquare className="h-7 w-7 text-slate-950 transition-transform group-hover:rotate-6" />
      </button>
    </div>
  );
};
