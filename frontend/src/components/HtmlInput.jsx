import { useState } from "react";
import axios from "axios";

export default function HtmlInput({ onResult }) {
  const [html, setHtml]       = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const handleConvert = async () => {
    if (!html.trim()) { setError("Please paste some HTML."); return; }
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("/api/convert/html", { html });
      onResult(res.data.markdown, "converted");
    } catch (err) {
      setError(err.response?.data?.detail || "Conversion failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">Paste your HTML</label>
      <textarea
        value={html}
        onChange={(e) => setHtml(e.target.value)}
        placeholder={'<h1>Title</h1>\n<p>Paragraph text</p>\n<ul><li>Item</li></ul>'}
        className="w-full h-48 font-mono text-sm border border-gray-200 rounded-xl p-4 resize-y focus:outline-none focus:ring-2 focus:ring-indigo-400 bg-gray-50"
      />
      {error && (
        <p className="mt-2 text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-4 py-2">
          {error}
        </p>
      )}
      <button
        onClick={handleConvert}
        disabled={loading}
        className="mt-3 w-full py-2.5 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 disabled:opacity-50 transition-colors font-medium"
      >
        {loading ? "Converting..." : "Convert to Markdown →"}
      </button>
    </div>
  );
}
