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
