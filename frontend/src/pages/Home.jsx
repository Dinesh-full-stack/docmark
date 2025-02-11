import { useState } from "react";
import FileUploader from "../components/FileUploader";
import HtmlInput from "../components/HtmlInput";
import MarkdownOutput from "../components/MarkdownOutput";

const TABS = [{ id: "csv", label: "CSV / Excel" }, { id: "docx", label: "Word (.docx)" }, { id: "html", label: "HTML" }];
const CSV_TYPES = { "text/csv": [".csv"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"] };
const DOCX_TYPES = { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"] };

export default function Home() {
  const [activeTab, setActiveTab] = useState("csv");
  const [markdown, setMarkdown] = useState(""); const [filename, setFilename] = useState("output");
  const handleResult = (md, name = "output") => { setMarkdown(md); setFilename(name); };
  const switchTab = (id) => { setActiveTab(id); setMarkdown(""); };
  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-indigo-700 mb-2">DocMark</h1>
        <p className="text-center text-gray-500 mb-8">Convert files & HTML to clean Markdown</p>
        <div className="flex border-b border-gray-200 mb-6">
          {TABS.map((tab) => (<button key={tab.id} onClick={() => switchTab(tab.id)} className={`px-5 py-2 text-sm font-medium transition-colors ${activeTab === tab.id ? "border-b-2 border-indigo-600 text-indigo-600" : "text-gray-500 hover:text-indigo-500"}`}>{tab.label}</button>))}
        </div>
        {activeTab === "csv" && <FileUploader endpoint="/api/convert/csv-excel" acceptedTypes={CSV_TYPES} onResult={handleResult} />}
        {activeTab === "docx" && <FileUploader endpoint="/api/convert/docx" acceptedTypes={DOCX_TYPES} onResult={handleResult} />}
        {activeTab === "html" && <HtmlInput onResult={handleResult} />}
        <MarkdownOutput markdown={markdown} filename={filename} />
      </div>
    </div>
  );
}
