import { useState } from "react";
import FileUploader from "../components/FileUploader";
import HtmlInput from "../components/HtmlInput";
import TextInput from "../components/TextInput";
import MarkdownOutput from "../components/MarkdownOutput";
import ConversionHistory from "../components/ConversionHistory";

const TABS = [
  {
    id: "csv",
    icon: (
      <svg viewBox="0 0 24 24" className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <rect x="3" y="3" width="18" height="18" rx="2" />
        <path d="M3 9h18M3 15h18M9 3v18" />
      </svg>
    ),
    label: "CSV / Excel",
    hint: ".csv · .xlsx",
    color: "text-emerald-600",
    bg: "bg-emerald-50",
  },
  {
    id: "docx",
    icon: (
      <svg viewBox="0 0 24 24" className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
        <line x1="16" y1="13" x2="8" y2="13" />
        <line x1="16" y1="17" x2="8" y2="17" />
        <polyline points="10 9 9 9 8 9" />
      </svg>
    ),
    label: "Word",
    hint: ".docx",
    color: "text-blue-600",
    bg: "bg-blue-50",
  },
  {
    id: "html",
    icon: (
      <svg viewBox="0 0 24 24" className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <polyline points="16 18 22 12 16 6" />
        <polyline points="8 6 2 12 8 18" />
      </svg>
    ),
    label: "HTML",
    hint: "paste HTML",
    color: "text-orange-600",
    bg: "bg-orange-50",
  },
  {
    id: "text",
    icon: (
      <svg viewBox="0 0 24 24" className="w-5 h-5" fill="none" stroke="currentColor" strokeWidth={1.8}>
        <line x1="17" y1="10" x2="3" y2="10" />
        <line x1="21" y1="6" x2="3" y2="6" />
        <line x1="21" y1="14" x2="3" y2="14" />
        <line x1="17" y1="18" x2="3" y2="18" />
      </svg>
    ),
    label: "Plain Text",
    hint: "paste text",
    color: "text-violet-600",
    bg: "bg-violet-50",
  },
];

const CSV_TYPES  = { "text/csv": [".csv"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"] };
const DOCX_TYPES = { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] };

const FEATURES = [
  { icon: "⚡", title: "Instant conversion", desc: "Results in under a second — no waiting, no queues." },
  { icon: "🔒", title: "Private by default", desc: "Files are never stored. Everything processes in memory." },
  { icon: "📋", title: "Copy or download",   desc: "One click to copy Markdown or save as a .md file." },
  { icon: "👁️", title: "Live preview",       desc: "Toggle between raw Markdown and rendered preview." },
];

export default function Home() {
  const [activeTab, setActiveTab] = useState("csv");
  const [markdown, setMarkdown]   = useState("");
  const [filename, setFilename]   = useState("output");
  const [history, setHistory]     = useState([]);

  const handleResult = (md, name = "output", type = activeTab) => {
    setMarkdown(md);
    setFilename(name);
    const entry = { filename: name, type, markdown: md, timestamp: new Date().toLocaleTimeString() };
    setHistory((prev) => [entry, ...prev].slice(0, 10));
  };

  const switchTab = (id) => { setActiveTab(id); setMarkdown(""); };
  const activeTabData = TABS.find((t) => t.id === activeTab);

  return (
    <>
      {/* ── Hero ─────────────────────────────────────────────── */}
      <section className="bg-gradient-to-b from-indigo-50 via-white to-white pt-16 pb-10 px-4 text-center">
        <span className="inline-block bg-indigo-100 text-indigo-700 text-xs font-semibold px-3 py-1 rounded-full mb-4 tracking-wide uppercase">
          Free · No sign-up required
        </span>
        <h1 className="text-4xl sm:text-5xl font-extrabold text-gray-900 leading-tight mb-4">
          Convert Any Document to
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
            {" "}Markdown
          </span>
        </h1>
        <p className="text-gray-500 text-lg max-w-xl mx-auto mb-8">
          Drop an Excel file, paste HTML, upload a Word doc, or type plain text —
          get clean, copy-ready Markdown in seconds.
        </p>
        <a
          href="#converter"
          className="inline-block bg-indigo-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-indigo-700 transition-colors shadow-md shadow-indigo-200"
        >
          Start converting →
        </a>
      </section>

      {/* ── Converter ────────────────────────────────────────── */}
      <section id="converter" className="max-w-3xl mx-auto px-4 py-10">
        <div className="grid grid-cols-4 gap-2 mb-6">
          {TABS.map((tab) => {
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => switchTab(tab.id)}
                className={`flex flex-col items-center gap-1.5 py-3 px-2 rounded-xl border text-xs font-medium transition-all
                  ${active
                    ? `${tab.bg} ${tab.color} border-current shadow-sm`
                    : "bg-white text-gray-400 border-gray-200 hover:border-gray-300 hover:text-gray-600"}`}
              >
                <span className={active ? tab.color : "text-gray-400"}>{tab.icon}</span>
                <span className="font-semibold">{tab.label}</span>
                <span className={`font-normal hidden sm:block ${active ? "opacity-70" : "text-gray-300"}`}
                  style={{ fontSize: "10px" }}>
                  {tab.hint}
                </span>
              </button>
            );
          })}
        </div>

        <div className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-4">
            {activeTabData?.label} → Markdown
          </p>
          {activeTab === "csv"  && <FileUploader endpoint="/api/convert/csv-excel" acceptedTypes={CSV_TYPES}  onResult={(md, n) => handleResult(md, n, "csv")} />}
          {activeTab === "docx" && <FileUploader endpoint="/api/convert/docx"      acceptedTypes={DOCX_TYPES} onResult={(md, n) => handleResult(md, n, "docx")} />}
          {activeTab === "html" && <HtmlInput  onResult={(md, n) => handleResult(md, n, "html")} />}
          {activeTab === "text" && <TextInput  onResult={(md, n) => handleResult(md, n, "text")} />}
        </div>

        <MarkdownOutput markdown={markdown} filename={filename} />

        <ConversionHistory
          history={history}
          onLoad={(item) => { setMarkdown(item.markdown); setFilename(item.filename); }}
          onClear={() => setHistory([])}
        />
      </section>

      {/* ── Features ─────────────────────────────────────────── */}
      <section className="bg-gray-50 border-t border-gray-100 py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold text-center text-gray-900 mb-10">
            Everything you need, nothing you don't
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
            {FEATURES.map((f) => (
              <div key={f.title} className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm text-center">
                <div className="text-3xl mb-3">{f.icon}</div>
                <h3 className="font-semibold text-gray-900 text-sm mb-1">{f.title}</h3>
                <p className="text-xs text-gray-500 leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Supported formats ────────────────────────────────── */}
      <section className="py-12 px-4 text-center">
        <p className="text-sm text-gray-400 mb-4 uppercase tracking-widest font-semibold">Supported formats</p>
        <div className="flex flex-wrap justify-center gap-3">
          {[
            { label: ".csv",       color: "bg-emerald-50 text-emerald-700" },
            { label: ".xlsx",      color: "bg-emerald-50 text-emerald-700" },
            { label: ".docx",      color: "bg-blue-50 text-blue-700" },
            { label: ".html",      color: "bg-orange-50 text-orange-700" },
            { label: "Plain text", color: "bg-violet-50 text-violet-700" },
          ].map((f) => (
            <span key={f.label} className={`text-sm px-4 py-1.5 rounded-full font-mono ${f.color}`}>
              {f.label}
            </span>
          ))}
        </div>
      </section>
    </>
  );
}
