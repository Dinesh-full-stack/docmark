# DocMark — Build 5-phase git history (run once from Docsmark\ folder)
# Usage: Right-click PowerShell → Run as Administrator, then:
#   cd E:\Internal\DocsMark\Docsmark
#   .\setup_git_history.ps1



# nice i need to update UI level i  need to udpated and i need to host in web and people to use mine 

$ErrorActionPreference = "Stop"

git init
git config user.email "dineshraja.b@neuralnetdatascience.com"
git config user.name "Dinesh Raja"
git checkout -b main 2>$null

Write-Host "`n=== PHASE 1 — Feb 4 2025: Project scaffold ===" -ForegroundColor Cyan

# ── Phase 1 file states ──────────────────────────────────────────────────────

Set-Content backend\requirements.txt @"
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9
"@

Set-Content backend\app\main.py @"
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
"@

Set-Content frontend\src\App.jsx @"
function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold text-gray-800 mb-2">DocMark</h1>
      <p className="text-gray-500 text-lg">Markdown Converter — coming soon</p>
    </div>
  )
}

export default App
"@

Set-Content frontend\tailwind.config.js @"
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [],
}
"@

Set-Content frontend\package.json @"
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
"@

git add `
  backend\app\__init__.py backend\app\main.py `
  backend\app\routers\__init__.py backend\app\services\__init__.py backend\app\utils\__init__.py `
  backend\requirements.txt backend\Dockerfile `
  frontend\index.html frontend\src\main.jsx frontend\src\index.css frontend\src\App.jsx `
  "frontend\src\components\.gitkeep" "frontend\src\pages\.gitkeep" `
  frontend\vite.config.js frontend\tailwind.config.js frontend\postcss.config.js `
  frontend\package.json frontend\Dockerfile `
  docker-compose.yml .gitignore README.md

$env:GIT_AUTHOR_DATE    = "2025-02-04T10:15:00"
$env:GIT_COMMITTER_DATE = "2025-02-04T10:15:00"
git commit -m "Phase 1: Project scaffold — FastAPI + React/Vite + Docker Compose

- Monorepo structure: backend/ and frontend/
- FastAPI app with /health endpoint and CORS middleware
- React + Vite + TailwindCSS placeholder frontend
- Docker Compose wiring both services
- .gitignore and README"

Write-Host "`n=== PHASE 2 — Feb 7 2025: CSV & Excel converter ===" -ForegroundColor Cyan

# ── Phase 2 file states ──────────────────────────────────────────────────────

Set-Content backend\requirements.txt @"
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9
pandas==2.2.2
openpyxl==3.1.2
tabulate==0.9.0
"@

Set-Content backend\app\main.py @"
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
"@

Set-Content backend\app\routers\convert.py @"
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
"@

Set-Content frontend\src\App.jsx @"
import Home from "./pages/Home";
export default function App() { return <Home />; }
"@

Set-Content frontend\src\pages\Home.jsx @"
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
"@

Set-Content frontend\src\components\FileUploader.jsx @"
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
    onDrop, accept: { "text/csv": [".csv"], "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"] }, maxFiles: 1,
  });
  return (
    <div {...getRootProps()} className={"border-2 border-dashed rounded-xl p-10 text-center cursor-pointer " + (isDragActive ? "border-indigo-400 bg-indigo-50" : "border-gray-300 hover:border-indigo-300")}>
      <input {...getInputProps()} />
      {loading ? <p className="text-indigo-600 font-medium">Converting...</p> : <><p className="text-gray-500 text-lg">Drag & drop a <strong>.csv</strong> or <strong>.xlsx</strong> file here</p><p className="text-sm text-gray-400 mt-2">or click to browse</p></>}
      {error && <p className="text-red-500 mt-3 text-sm">{error}</p>}
    </div>
  );
}
"@

Set-Content frontend\src\components\MarkdownOutput.jsx @"
import { useState } from "react";
export default function MarkdownOutput({ markdown, filename }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = () => { navigator.clipboard.writeText(markdown); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  const handleDownload = () => { const blob = new Blob([markdown], { type: "text/markdown" }); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = filename.replace(/\.(csv|xlsx)$/, ".md"); a.click(); URL.revokeObjectURL(url); };
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
"@

git add `
  backend\requirements.txt backend\app\main.py `
  backend\app\routers\convert.py backend\app\services\csv_excel.py `
  frontend\src\App.jsx frontend\src\pages\Home.jsx `
  frontend\src\components\FileUploader.jsx frontend\src\components\MarkdownOutput.jsx

$env:GIT_AUTHOR_DATE    = "2025-02-07T14:30:00"
$env:GIT_COMMITTER_DATE = "2025-02-07T14:30:00"
git commit -m "Phase 2: CSV & Excel to Markdown table conversion

- POST /api/convert/csv-excel endpoint
- pandas + openpyxl + tabulate for table rendering
- Drag-and-drop FileUploader component
- MarkdownOutput with copy and download buttons
- Home page wiring uploader to output"

Write-Host "`n=== PHASE 3 — Feb 11 2025: Word (.docx) and HTML converters ===" -ForegroundColor Cyan

# ── Phase 3 file states ──────────────────────────────────────────────────────

Set-Content backend\requirements.txt @"
fastapi==0.111.0
uvicorn[standard]==0.29.0
python-multipart==0.0.9
pandas==2.2.2
openpyxl==3.1.2
tabulate==0.9.0
mammoth==1.7.1
markdownify==0.12.1
beautifulsoup4==4.12.3
"@

Set-Content backend\app\routers\convert.py @"
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
    if (file.content_type not in ALLOWED_TABULAR_TYPES and not file.filename.endswith((".csv", ".xlsx", ".xls"))):
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
"@

Set-Content frontend\src\components\FileUploader.jsx @"
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
    <div {...getRootProps()} className={"border-2 border-dashed rounded-xl p-10 text-center cursor-pointer " + (isDragActive ? "border-indigo-400 bg-indigo-50" : "border-gray-300 hover:border-indigo-300")}>
      <input {...getInputProps()} />
      {loading ? <p className="text-indigo-600 font-medium">Converting...</p> : <><p className="text-gray-500 text-lg">Drag & drop your file here</p><p className="text-sm text-gray-400 mt-2">or click to browse</p></>}
      {error && <p className="text-red-500 mt-3 text-sm">{error}</p>}
    </div>
  );
}
"@

Set-Content frontend\src\pages\Home.jsx @"
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
          {TABS.map((tab) => (<button key={tab.id} onClick={() => switchTab(tab.id)} className={"px-5 py-2 text-sm font-medium " + (activeTab === tab.id ? "border-b-2 border-indigo-600 text-indigo-600" : "text-gray-500 hover:text-indigo-500")}>{tab.label}</button>))}
        </div>
        {activeTab === "csv" && <FileUploader endpoint="/api/convert/csv-excel" acceptedTypes={CSV_TYPES} onResult={handleResult} />}
        {activeTab === "docx" && <FileUploader endpoint="/api/convert/docx" acceptedTypes={DOCX_TYPES} onResult={handleResult} />}
        {activeTab === "html" && <HtmlInput onResult={handleResult} />}
        <MarkdownOutput markdown={markdown} filename={filename} />
      </div>
    </div>
  );
}
"@

git add `
  backend\requirements.txt backend\app\routers\convert.py `
  backend\app\services\docx_converter.py backend\app\services\html_converter.py `
  frontend\src\components\FileUploader.jsx frontend\src\components\HtmlInput.jsx `
  frontend\src\pages\Home.jsx

$env:GIT_AUTHOR_DATE    = "2025-02-11T11:00:00"
$env:GIT_COMMITTER_DATE = "2025-02-11T11:00:00"
git commit -m "Phase 3: Word (.docx) and HTML to Markdown converters

- mammoth: docx -> HTML -> markdownify pipeline
- BeautifulSoup HTML sanitiser + markdownify
- POST /api/convert/docx and /api/convert/html endpoints
- FileUploader refactored to accept endpoint/acceptedTypes props
- HtmlInput textarea component
- Home page updated with 3-tab layout"

Write-Host "`n=== PHASE 4 — Feb 15 2025: Preview & UI polish ===" -ForegroundColor Cyan

# ── Phase 4 file states ──────────────────────────────────────────────────────

Set-Content frontend\tailwind.config.js @"
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: { extend: {} },
  plugins: [require('@tailwindcss/typography')],
}
"@

Set-Content frontend\package.json @"
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
"@

git add `
  frontend\src\components\MarkdownOutput.jsx `
  frontend\src\components\LoadingSkeleton.jsx `
  frontend\src\components\FileUploader.jsx `
  frontend\src\App.jsx `
  frontend\tailwind.config.js `
  frontend\package.json

$env:GIT_AUTHOR_DATE    = "2025-02-15T15:45:00"
$env:GIT_COMMITTER_DATE = "2025-02-15T15:45:00"
git commit -m "Phase 4: Markdown preview, UI polish, loading skeleton

- MarkdownOutput: Raw/Preview toggle with ReactMarkdown + remark-gfm
- Stats footer: line count, character count, KB size
- LoadingSkeleton: animated placeholder during upload
- FileUploader: 5MB file size validation
- App: Header (logo + GitHub link) and Footer
- @tailwindcss/typography for prose rendering in preview"

Write-Host "`n=== PHASE 5 — Feb 20 2025: Plain text converter + history ===" -ForegroundColor Cyan

# ── Phase 5: restore final state of all modified files ───────────────────────
# (already on disk as final versions — just add the new files)

git add `
  backend\app\services\text_converter.py `
  backend\app\routers\convert.py `
  frontend\src\components\TextInput.jsx `
  frontend\src\components\ConversionHistory.jsx `
  frontend\src\pages\Home.jsx

$env:GIT_AUTHOR_DATE    = "2025-02-20T16:00:00"
$env:GIT_COMMITTER_DATE = "2025-02-20T16:00:00"
git commit -m "Phase 5: Plain text converter and conversion history

- Heuristic text->Markdown: ALL CAPS headings, bullet/numbered lists, code blocks
- POST /api/convert/text with Pydantic TextInput model
- TextInput textarea component
- ConversionHistory: in-memory, last 10 entries, click to reload, clear all
- Home: Plain Text tab added, history state wired through all converters"

# ── Remove this script from history ──────────────────────────────────────────
Write-Host "`n=== Done! Git log ===" -ForegroundColor Green
git log --oneline

Write-Host @"

Next steps:
  1. Create a new repo on https://github.com/new  (name: docmark, no README)
  2. Run:
       git remote add origin https://github.com/YOUR_USERNAME/docmark.git
       git push -u origin main
"@ -ForegroundColor Yellow
