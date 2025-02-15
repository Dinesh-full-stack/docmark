import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function MarkdownOutput({ markdown, filename }) {
  const [mode, setMode] = useState("raw");
  const [copied, setCopied] = useState(false);
  const handleCopy = () => {
    navigator.clipboard.writeText(markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  const handleDownload = () => {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = (filename || "output").replace(/\.(csv|xlsx|docx|html)$/, "") + ".md";
    a.click();
    URL.revokeObjectURL(url);
  };
  if (!markdown) return null;
  const lines = markdown.split("\n").length;
  const chars = markdown.length;
  const kb = (new Blob([markdown]).size / 1024).toFixed(1);
  return (
    <div className="mt-6 border border-gray-200 rounded-2xl overflow-hidden">
      <div className="flex justify-between items-center px-4 py-2 bg-gray-50 border-b border-gray-200">
        <div className="flex gap-1">
          <button onClick={() => setMode("raw")}
            className={`px-3 py-1 text-xs rounded-lg font-medium ${mode === "raw" ? "bg-white border border-gray-300 shadow-sm" : "text-gray-500"}`}>
            ⌨ Raw
          </button>
          <button onClick={() => setMode("preview")}
            className={`px-3 py-1 text-xs rounded-lg font-medium ${mode === "preview" ? "bg-white border border-gray-300 shadow-sm" : "text-gray-500"}`}>
            👁 Preview
          </button>
        </div>
        <div className="flex gap-2">
          <button onClick={handleCopy} className="px-3 py-1 text-xs bg-indigo-500 text-white rounded-lg hover:bg-indigo-600">
            {copied ? "Copied!" : "Copy"}
          </button>
          <button onClick={handleDownload} className="px-3 py-1 text-xs bg-green-500 text-white rounded-lg hover:bg-green-600">
            Download .md
          </button>
        </div>
      </div>
      {mode === "raw" ? (
        <textarea readOnly value={markdown}
          className="w-full h-64 font-mono text-sm bg-gray-900 text-green-300 p-4 resize-y border-0 outline-none" />
      ) : (
        <div className="prose prose-sm max-w-none p-4 overflow-auto max-h-96">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
        </div>
      )}
      <div className="px-4 py-2 bg-gray-50 border-t border-gray-200 text-xs text-gray-400 flex gap-4">
        <span>{lines} lines</span><span>{chars} chars</span><span>{kb} KB</span>
      </div>
    </div>
  );
}
