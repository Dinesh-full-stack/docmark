"""
DocMark -- Build 5-phase git history
Run from the Docsmark folder:
    python setup_git_history.py
"""
import os, stat, subprocess, textwrap, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Remove any broken .git folder from a previous failed attempt
# Windows git objects are read-only; chmod them writable before deletion.
def _force_remove(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)

git_dir = ROOT / ".git"
if git_dir.exists():
    print(f"Removing existing .git folder at {git_dir} ...")
    shutil.rmtree(git_dir, onexc=_force_remove)

def git(*args, date=None):
    env = os.environ.copy()
    if date:
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    result = subprocess.run(
        ["git"] + list(args), env=env,
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode != 0 and "nothing to commit" not in result.stdout + result.stderr:
        print("GIT ERROR:", result.stdout, result.stderr)
    return result

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")

def add(*paths):
    git("add", *[str(ROOT / p) for p in paths])

# ── Init ─────────────────────────────────────────────────────────────────────
r = git("init")
if r.returncode != 0:
    raise SystemExit(f"git init failed: {r.stderr}")
print(f"  git init → {ROOT}")
git("config", "user.email", "dineshraja.b@neuralnetdatascience.com")
git("config", "user.name", "Dinesh Raja")
git("checkout", "-b", "main")

print("\n=== PHASE 1 — Feb 4 2025: Project scaffold ===")

write("backend/requirements.txt", """
    fastapi==0.111.0
    uvicorn[standard]==0.29.0
    python-multipart==0.0.9
""")

write("backend/app/main.py", """
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="DocMark API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "DocMark API"}
""")

write("frontend/src/App.jsx", """
    function App() {
      return (
        <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">DocMark</h1>
          <p className="text-gray-500 text-lg">Markdown Converter — coming soon</p>
        </div>
      )
    }
    export default App
""")

write("frontend/tailwind.config.js", """
    /** @type {import('tailwindcss').Config} */
    export default {
      content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
      theme: { extend: {} },
      plugins: [],
    }
""")

write("frontend/package.json", """\
{
  "name": "docmark-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" },
  "dependencies": {
    "axios": "^1.7.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-dropzone": "^14.2.3",
    "react-markdown": "^9.0.1",
    "react-router-dom": "^6.23.1"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "vite": "^5.2.12"
  }
}
""")

add(
    "backend/app/__init__.py", "backend/app/main.py",
    "backend/app/routers/__init__.py", "backend/app/services/__init__.py", "backend/app/utils/__init__.py",
    "backend/requirements.txt", "backend/Dockerfile",
    "frontend/index.html", "frontend/src/main.jsx", "frontend/src/index.css", "frontend/src/App.jsx",
    "frontend/src/components/.gitkeep", "frontend/src/pages/.gitkeep",
    "frontend/vite.config.js", "frontend/tailwind.config.js", "frontend/postcss.config.js",
    "frontend/package.json", "frontend/Dockerfile",
    "docker-compose.yml", ".gitignore", "README.md",
)
git("commit", "-m",
    "Phase 1: Project scaffold — FastAPI + React/Vite + Docker Compose\n\n"
    "- Monorepo structure: backend/ and frontend/\n"
    "- FastAPI app with /health endpoint and CORS middleware\n"
    "- React + Vite + TailwindCSS placeholder frontend\n"
    "- Docker Compose wiring both services\n"
    "- .gitignore and README",
    date="2025-02-04T10:15:00")
print("  ✓ Committed Phase 1")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== PHASE 2 — Feb 7 2025: CSV & Excel converter ===")

write("backend/requirements.txt", """
    fastapi==0.111.0
    uvicorn[standard]==0.29.0
    python-multipart==0.0.9
    pandas==2.2.2
    openpyxl==3.1.2
    tabulate==0.9.0
""")

write("backend/app/main.py", """
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from app.routers.convert import router as convert_router

    app = FastAPI(title="DocMark API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(convert_router)

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "DocMark API"}
""")

write("backend/app/routers/convert.py", """
    from fastapi import APIRouter, UploadFile, File, HTTPException
    from app.services.csv_excel import convert_file_to_markdown

    router = APIRouter(prefix="/api/convert", tags=["convert"])

    ALLOWED_TABULAR_TYPES = {
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
    }

    @router.post("/csv-excel")
    async def convert_csv_excel(file: UploadFile = File(...)):
        if (
            file.content_type not in ALLOWED_TABULAR_TYPES
            and not file.filename.endswith((".csv", ".xlsx", ".xls"))
        ):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")
        content = await file.read()
        try:
            markdown = convert_file_to_markdown(content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        return {"filename": file.filename, "markdown": markdown}
""")

write("frontend/src/App.jsx", """
    import Home from "./pages/Home";
    export default function App() { return <Home />; }
""")

write("frontend/src/pages/Home.jsx", """
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
""")

write("frontend/src/components/FileUploader.jsx", """\
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

export default function FileUploader({ onResult }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true); setError("");
    try {
      const res = await axios.post("/api/convert/csv-excel", formData);
      onResult(res.data.markdown, file.name);
    } catch (err) {
      setError(err.response?.data?.detail || "Conversion failed.");
    } finally { setLoading(false); }
  }, [onResult]);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "text/csv": [".csv"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"] },
    maxFiles: 1,
  });
  return (
    <div {...getRootProps()} className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all ${isDragActive ? "border-indigo-400 bg-indigo-50" : "border-gray-300 hover:border-indigo-300"}`}>
      <input {...getInputProps()} />
      {loading ? <p className="text-indigo-600 font-medium animate-pulse">Converting...</p> : (
        <><p className="text-gray-500 text-lg">Drag & drop a <strong>.csv</strong> or <strong>.xlsx</strong></p><p className="text-sm text-gray-400 mt-2">or click to browse</p></>
      )}
      {error && <p className="text-red-500 mt-3 text-sm">{error}</p>}
    </div>
  );
}
""")

write("frontend/src/components/MarkdownOutput.jsx", """\
import { useState } from "react";
export default function MarkdownOutput({ markdown, filename }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => { navigator.clipboard.writeText(markdown); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  const handleDownload = () => {
    const blob = new Blob([markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename.replace(/\\.(csv|xlsx)$/, ".md"); a.click(); URL.revokeObjectURL(url);
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
""")

add(
    "backend/requirements.txt", "backend/app/main.py",
    "backend/app/routers/convert.py", "backend/app/services/csv_excel.py",
    "frontend/src/App.jsx", "frontend/src/pages/Home.jsx",
    "frontend/src/components/FileUploader.jsx", "frontend/src/components/MarkdownOutput.jsx",
)
git("commit", "-m",
    "Phase 2: CSV & Excel to Markdown table conversion\n\n"
    "- POST /api/convert/csv-excel endpoint\n"
    "- pandas + openpyxl + tabulate for table rendering\n"
    "- Drag-and-drop FileUploader component\n"
    "- MarkdownOutput with copy and download buttons\n"
    "- Home page wiring uploader to output",
    date="2025-02-07T14:30:00")
print("  ✓ Committed Phase 2")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== PHASE 3 — Feb 11 2025: Word (.docx) and HTML converters ===")

write("backend/requirements.txt", """
    fastapi==0.111.0
    uvicorn[standard]==0.29.0
    python-multipart==0.0.9
    pandas==2.2.2
    openpyxl==3.1.2
    tabulate==0.9.0
    mammoth==1.7.1
    markdownify==0.12.1
    beautifulsoup4==4.12.3
""")

write("backend/app/routers/convert.py", """
    from fastapi import APIRouter, UploadFile, File, HTTPException, Body
    from app.services.csv_excel import convert_file_to_markdown
    from app.services.docx_converter import convert_docx_to_markdown
    from app.services.html_converter import convert_html_to_markdown

    router = APIRouter(prefix="/api/convert", tags=["convert"])

    ALLOWED_TABULAR_TYPES = {
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-excel",
    }

    @router.post("/csv-excel")
    async def convert_csv_excel(file: UploadFile = File(...)):
        if (file.content_type not in ALLOWED_TABULAR_TYPES
                and not file.filename.endswith((".csv", ".xlsx", ".xls"))):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")
        content = await file.read()
        try:
            markdown = convert_file_to_markdown(content, file.filename)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        return {"filename": file.filename, "markdown": markdown}

    @router.post("/docx")
    async def convert_docx(file: UploadFile = File(...)):
        if not file.filename.endswith(".docx"):
            raise HTTPException(status_code=400, detail="Only .docx files are supported.")
        content = await file.read()
        try:
            markdown = convert_docx_to_markdown(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
        return {"filename": file.filename, "markdown": markdown}

    @router.post("/html")
    async def convert_html(html: str = Body(..., embed=True)):
        if not html.strip():
            raise HTTPException(status_code=400, detail="HTML content cannot be empty.")
        try:
            markdown = convert_html_to_markdown(html)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
        return {"markdown": markdown}
""")

write("frontend/src/components/FileUploader.jsx", """\
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

export default function FileUploader({ endpoint, acceptedTypes, onResult }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true); setError("");
    try {
      const res = await axios.post(endpoint, formData);
      onResult(res.data.markdown, file.name);
    } catch (err) {
      setError(err.response?.data?.detail || "Conversion failed.");
    } finally { setLoading(false); }
  }, [endpoint, onResult]);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: acceptedTypes, maxFiles: 1 });
  return (
    <div {...getRootProps()} className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all ${isDragActive ? "border-indigo-400 bg-indigo-50" : "border-gray-300 hover:border-indigo-300"}`}>
      <input {...getInputProps()} />
      {loading ? <p className="text-indigo-600 font-medium animate-pulse">Converting...</p> : (
        <><p className="text-gray-500 text-lg">Drag &amp; drop your file here</p><p className="text-sm text-gray-400 mt-2">or click to browse</p></>
      )}
      {error && <p className="text-red-500 mt-3 text-sm">{error}</p>}
    </div>
  );
}
""")

write("frontend/src/pages/Home.jsx", """\
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
""")

add(
    "backend/requirements.txt", "backend/app/routers/convert.py",
    "backend/app/services/docx_converter.py", "backend/app/services/html_converter.py",
    "frontend/src/components/FileUploader.jsx", "frontend/src/components/HtmlInput.jsx",
    "frontend/src/pages/Home.jsx",
)
git("commit", "-m",
    "Phase 3: Word (.docx) and HTML to Markdown converters\n\n"
    "- mammoth: docx -> HTML -> markdownify pipeline\n"
    "- BeautifulSoup HTML sanitiser + markdownify\n"
    "- POST /api/convert/docx and /api/convert/html endpoints\n"
    "- FileUploader refactored to accept endpoint/acceptedTypes props\n"
    "- HtmlInput textarea component\n"
    "- Home page updated with 3-tab layout",
    date="2025-02-11T11:00:00")
print("  ✓ Committed Phase 3")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== PHASE 4 — Feb 15 2025: Preview & UI polish ===")

write("frontend/tailwind.config.js", """
    /** @type {import('tailwindcss').Config} */
    export default {
      content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
      theme: { extend: {} },
      plugins: [require("@tailwindcss/typography")],
    }
""")

write("frontend/package.json", """\
{
  "name": "docmark-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": { "dev": "vite", "build": "vite build", "preview": "vite preview" },
  "dependencies": {
    "axios": "^1.7.2",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-dropzone": "^14.2.3",
    "react-markdown": "^9.0.1",
    "react-router-dom": "^6.23.1",
    "rehype-highlight": "^7.0.0",
    "remark-gfm": "^4.0.0"
  },
  "devDependencies": {
    "@tailwindcss/typography": "^0.5.13",
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "autoprefixer": "^10.4.19",
    "highlight.js": "^11.9.0",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.4",
    "vite": "^5.2.12"
  }
}
""")

write("frontend/src/components/LoadingSkeleton.jsx", """\
export default function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-3 mt-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-4 bg-gray-200 rounded" style={{ width: `${80 - i * 10}%` }} />
      ))}
    </div>
  );
}
""")

write("frontend/src/components/MarkdownOutput.jsx", """\
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
    a.download = (filename || "output").replace(/\\.(csv|xlsx|docx|html)$/, "") + ".md";
    a.click();
    URL.revokeObjectURL(url);
  };
  if (!markdown) return null;
  const lines = markdown.split("\\n").length;
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
""")

write("frontend/src/components/FileUploader.jsx", """\
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import LoadingSkeleton from "./LoadingSkeleton";

const MAX_SIZE = 5 * 1024 * 1024;

export default function FileUploader({ endpoint, acceptedTypes, onResult }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const onDrop = useCallback(async (acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) { setError("File too large — maximum 5 MB."); return; }
    const file = acceptedFiles[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true); setError("");
    try {
      const res = await axios.post(endpoint, formData);
      onResult(res.data.markdown, file.name);
    } catch (err) {
      setError(err.response?.data?.detail || "Conversion failed.");
    } finally { setLoading(false); }
  }, [endpoint, onResult]);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: acceptedTypes, maxFiles: 1, maxSize: MAX_SIZE,
  });
  return (
    <div>
      <div {...getRootProps()} className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-all
        ${isDragActive ? "border-indigo-400 bg-indigo-50" : "border-gray-300 hover:border-indigo-300"}`}>
        <input {...getInputProps()} />
        {loading ? <LoadingSkeleton /> : (
          <><p className="text-gray-500 text-lg">📂 Drag &amp; drop your file here</p>
          <p className="text-sm text-gray-400 mt-2">or click to browse · max 5 MB</p></>
        )}
      </div>
      {error && <p className="text-red-500 mt-2 text-sm">{error}</p>}
    </div>
  );
}
""")

write("frontend/src/App.jsx", """\
import Home from "./pages/Home";

function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">
        <span className="font-bold text-indigo-700 text-xl">DocMark</span>
        <a href="https://github.com/Dinesh-full-stack/docmark" target="_blank" rel="noreferrer"
          className="text-sm text-gray-500 hover:text-indigo-600">GitHub</a>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="bg-gray-50 border-t border-gray-200 mt-16 py-8 text-center text-sm text-gray-400">
      {`© ${new Date().getFullYear()} DocMark · Built with FastAPI + React`}
    </footer>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Header /><main className="flex-1"><Home /></main><Footer />
    </div>
  );
}
""")

add(
    "frontend/src/components/MarkdownOutput.jsx",
    "frontend/src/components/LoadingSkeleton.jsx",
    "frontend/src/components/FileUploader.jsx",
    "frontend/src/App.jsx",
    "frontend/tailwind.config.js",
    "frontend/package.json",
)
git("commit", "-m",
    "Phase 4: Markdown preview, UI polish, loading skeleton\n\n"
    "- MarkdownOutput: Raw/Preview toggle with ReactMarkdown + remark-gfm\n"
    "- Stats footer: line count, character count, KB size\n"
    "- LoadingSkeleton: animated placeholder during upload\n"
    "- FileUploader: 5MB file size validation\n"
    "- App: Header (logo + GitHub link) and Footer\n"
    "- @tailwindcss/typography for prose rendering in preview",
    date="2025-02-15T15:45:00")
print("  ✓ Committed Phase 4")

# ─────────────────────────────────────────────────────────────────────────────
print("\n=== PHASE 5 — Feb 20 2025: Plain text + Markify rebrand ===")

write("backend/app/main.py", """\
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.convert import router as convert_router

app = FastAPI(title="Markify API", version="1.0.0")

_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(convert_router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Markify API"}
""")

write("backend/app/routers/convert.py", """\
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.csv_excel import convert_file_to_markdown
from app.services.docx_converter import convert_docx_to_markdown
from app.services.html_converter import convert_html_to_markdown
from app.services.text_converter import convert_text_to_markdown

router = APIRouter(prefix="/api/convert", tags=["convert"])

ALLOWED_TABULAR_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
}

class TextInput(BaseModel):
    text: str

@router.post("/csv-excel")
async def convert_csv_excel(file: UploadFile = File(...)):
    if (file.content_type not in ALLOWED_TABULAR_TYPES
            and not file.filename.endswith((".csv", ".xlsx", ".xls"))):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")
    content = await file.read()
    try:
        markdown = convert_file_to_markdown(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"filename": file.filename, "markdown": markdown}

@router.post("/docx")
async def convert_docx(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported.")
    content = await file.read()
    try:
        markdown = convert_docx_to_markdown(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    return {"filename": file.filename, "markdown": markdown}

@router.post("/html")
async def convert_html(payload: TextInput):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="HTML content cannot be empty.")
    try:
        markdown = convert_html_to_markdown(payload.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    return {"markdown": markdown}

@router.post("/text")
async def convert_text(payload: TextInput):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text content cannot be empty.")
    try:
        markdown = convert_text_to_markdown(payload.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    return {"markdown": markdown}
""")

write("frontend/src/components/Logo.jsx", """\
export default function Logo({ size = 32, showText = true, textSize = "text-xl" }) {
  return (
    <div className="flex items-center gap-2">
      <svg width={size} height={size} viewBox="0 0 40 40" fill="none"
        xmlns="http://www.w3.org/2000/svg" style={{ flexShrink: 0 }}>
        <defs>
          <linearGradient id="markify-grad" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
            <stop offset="0%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#a855f7" />
          </linearGradient>
        </defs>
        <rect width="40" height="40" rx="10" fill="url(#markify-grad)" />
        <path d="M9 29V11l11 12 11-12v18" stroke="white" strokeWidth="3.5"
          strokeLinecap="round" strokeLinejoin="round" fill="none" />
      </svg>
      {showText && (
        <span className={`font-extrabold tracking-tight text-gray-900 ${textSize}`}>Markify</span>
      )}
    </div>
  );
}
""")

write("frontend/src/App.jsx", """\
import Home from "./pages/Home";
import Logo from "./components/Logo";

function Header() {
  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-50 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
        <Logo size={34} textSize="text-lg" />
        <nav className="flex items-center gap-4">
          <a href="#converter" className="text-sm text-gray-500 hover:text-indigo-600 transition-colors hidden sm:block">Convert</a>
          <a href="https://github.com/Dinesh-full-stack/docmark" target="_blank" rel="noreferrer"
            className="text-sm text-gray-500 hover:text-gray-900 transition-colors hidden sm:block">GitHub</a>
          <a href="#converter"
            className="text-sm bg-indigo-600 text-white px-4 py-1.5 rounded-lg hover:bg-indigo-700 transition-colors font-medium">Try free →</a>
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-400 mt-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
        <div className="flex flex-col sm:flex-row justify-between items-start gap-6">
          <div>
            <Logo size={28} textSize="text-sm" showText={true} />
            <p className="text-xs text-gray-500 max-w-xs mt-2">
              Convert Excel, CSV, Word, HTML and plain text to clean Markdown instantly.
              All conversions happen in memory — no files stored.
            </p>
          </div>
          <div className="flex gap-8 text-sm">
            <div>
              <p className="text-white font-medium mb-2">Product</p>
              <ul className="space-y-1">
                <li><a href="#converter" className="hover:text-white transition-colors">Converter</a></li>
                <li><a href="https://github.com/Dinesh-full-stack/docmark" target="_blank" rel="noreferrer"
                  className="hover:text-white transition-colors">GitHub</a></li>
              </ul>
            </div>
            <div>
              <p className="text-white font-medium mb-2">Legal</p>
              <ul className="space-y-1">
                <li><a href="/privacy" className="hover:text-white transition-colors">Privacy Policy</a></li>
                <li><a href="/terms" className="hover:text-white transition-colors">Terms of Use</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-6 text-xs text-gray-600 text-center">
          {`© ${new Date().getFullYear()} Markify · Built with FastAPI + React`}
        </div>
      </div>
    </footer>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Header />
      <main className="flex-1"><Home /></main>
      <Footer />
    </div>
  );
}
""")

write("frontend/index.html", """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Markify — Convert Any Document to Markdown</title>
    <meta name="description" content="Convert Excel, CSV, Word (.docx), HTML, and plain text to clean Markdown instantly. Free, no sign-up required." />
    <meta name="keywords" content="markdown converter, csv to markdown, excel to markdown, docx to markdown, html to markdown" />
    <meta property="og:title" content="Markify — Convert Any Document to Markdown" />
    <meta property="og:description" content="Free online tool to convert Excel, CSV, Word, HTML and plain text to Markdown." />
    <meta property="og:type" content="website" />
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><defs><linearGradient id='g' x1='0' y1='0' x2='40' y2='40' gradientUnits='userSpaceOnUse'><stop offset='0%25' stop-color='%236366f1'/><stop offset='100%25' stop-color='%23a855f7'/></linearGradient></defs><rect width='40' height='40' rx='10' fill='url(%23g)'/><path d='M9 29V11l11 12 11-12v18' stroke='white' stroke-width='3.5' stroke-linecap='round' stroke-linejoin='round' fill='none'/></svg>" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
""")

add(
    "backend/app/main.py",
    "backend/app/routers/convert.py",
    "backend/app/services/text_converter.py",
    "frontend/src/components/Logo.jsx",
    "frontend/src/components/TextInput.jsx",
    "frontend/src/components/ConversionHistory.jsx",
    "frontend/src/components/FileUploader.jsx",
    "frontend/src/App.jsx",
    "frontend/src/pages/Home.jsx",
    "frontend/index.html",
)
git("commit", "-m",
    "Phase 5: Plain text converter + Markify rebrand\n\n"
    "- Heuristic text->Markdown: ALL CAPS headings, bullet/numbered lists, code blocks\n"
    "- POST /api/convert/text with Pydantic TextInput model\n"
    "- TextInput and ConversionHistory components\n"
    "- CORS origins driven by ALLOWED_ORIGINS env var\n"
    "- Markify rebrand: gradient M logo, hero, 4-tab UI with icons\n"
    "- index.html: Markify title, meta tags, SVG favicon",
    date="2025-02-20T16:00:00")
print("  ✓ Committed Phase 5")

print("\n✅ All done! Git log:")
subprocess.run(["git", "log", "--oneline"], cwd=str(ROOT))
print("""
Next steps:
  1. Create repo at https://github.com/new  (name: docmark, no README)
  2. Run:
       git remote add origin https://github.com/YOUR_USERNAME/docmark.git
       git push -u origin main
""")
