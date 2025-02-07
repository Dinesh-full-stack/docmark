import { useState } from "react";
export default function MarkdownOutput({ markdown, filename }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => { navigator.clipboard.writeText(markdown); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  const handleDownload = () => {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename.replace(/\.(csv|xlsx)$/, ".md"); a.click(); URL.revokeObjectURL(url);
  };
  if (!markdown) return null;
  return (
    <div className="mt-6">
      <div className="flex justify-between items-center mb-2">
        <h2 className="text-lg font-semibold text-gray-700">Markdown Output</h2>
        <div className="flex gap-2">
          <button onClick={handleCopy} className="px-3 py-1 text-sm bg-indigo-500 text-white rounded hover:bg-indigo-600">{copied ? "Copied!" : "Copy"}</button>
          <button onClick={handleDownload} className="px-3 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-600">Download .md</button>
        </div>
      </div>
      <textarea readOnly value={markdown} className="w-full h-64 font-mono text-sm bg-gray-900 text-green-300 p-4 rounded-xl border border-gray-700 resize-y" />
    </div>
  );
}
