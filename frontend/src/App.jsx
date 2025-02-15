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
