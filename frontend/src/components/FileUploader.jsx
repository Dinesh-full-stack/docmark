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
