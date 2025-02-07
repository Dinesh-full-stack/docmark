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
