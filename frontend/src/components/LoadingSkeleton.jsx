export default function LoadingSkeleton() {
  return (
    <div className="animate-pulse space-y-3 mt-4">
      {[...Array(5)].map((_, i) => (
        <div key={i} className="h-4 bg-gray-200 rounded" style={{ width: `${80 - i * 10}%` }} />
      ))}
    </div>
  );
}
