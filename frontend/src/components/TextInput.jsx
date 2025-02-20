import { useState } from "react";
import axios from "axios";

export default function TextInput({ onResult }) {
  const [text, setText]       = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState("");

  const handleConvert = async () => {
    if (!text.trim()) { setError("Please enter some text."); return; }
    setLoading(true);
    setError("");
    try {
      const res = await axios.post("/api/convert/text", { text });
      onResult(res.data.markdown, "text-conversion");
    } catch (err) {
      setError(err.response?.data?.detail || "Conversion failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">Paste plain text</label>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={"SECTION HEADING\n\n- Bullet point one\n- Bullet point two\n\n1. Numbered item\n2. Another item\n\n    indented code block"}
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
