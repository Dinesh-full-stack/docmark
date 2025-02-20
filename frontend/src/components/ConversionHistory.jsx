export default function ConversionHistory({ history, onLoad, onClear }) {
  if (history.length === 0) return null;

  return (
    <div className="mt-10">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-sm font-semibold text-gray-600 uppercase tracking-wide">
          Recent Conversions
        </h3>
        <button
          onClick={onClear}
          className="text-xs text-red-400 hover:text-red-600 transition-colors"
        >
          Clear all
        </button>
      </div>
      <ul className="space-y-2">
        {history.map((item, idx) => (
          <li
            key={idx}
            onClick={() => onLoad(item)}
            className="flex justify-between items-center bg-white border border-gray-100 rounded-xl px-4 py-2 hover:border-indigo-200 hover:shadow-sm cursor-pointer transition-all"
          >
            <div>
              <span className="text-sm font-medium text-gray-700">{item.filename}</span>
              <span className="ml-2 text-xs text-gray-400 bg-gray-100 px-1.5 py-0.5 rounded">
                {item.type}
              </span>
            </div>
            <span className="text-xs text-gray-400">{item.timestamp}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
