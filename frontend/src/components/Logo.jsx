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
