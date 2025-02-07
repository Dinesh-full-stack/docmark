import { useState } from "react";
import FileUploader from "../components/FileUploader";
import MarkdownOutput from "../components/MarkdownOutput";

export default function Home() {
  const [markdown, setMarkdown] = useState("");
  const [filename, setFilename] = useState("");
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-indigo-700 mb-2">DocMark</h1>
        <p className="text-center text-gray-500 mb-8">Convert Excel & CSV to Markdown instantly</p>
        <FileUploader onResult={(md, name) => { setMarkdown(md); setFilename(name); }} />
        <MarkdownOutput markdown={markdown} filename={filename} />
      </div>
    </div>
  );
}
