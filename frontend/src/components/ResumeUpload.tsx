"use client";

import { useState } from "react";
import { Upload, FileText, Loader2 } from "lucide-react";
import api from "@/services/api";
import { AnalysisResponse } from "@/types";

// explains shape of props passed to this component
interface ResumeUploadProps {
  onSuccess: (data: any) => void;
}

export default function ResumeUpload({
  onSuccess,
}: ResumeUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const selectedFile = e.target.files?.[0];

    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {
      setError("Please upload a PDF file.");
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a resume.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();

      formData.append("file", file);

      const response = await api.post(
        "/recommend-pdf",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      onSuccess(response.data);
    } catch (err) {
      console.error(err);

      setError(
        "Failed to analyze resume. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-xl rounded-2xl border bg-white p-8 shadow-lg">
      <h2 className="mb-6 text-center text-2xl font-bold">
        Upload Your Resume
      </h2>

      <label
        htmlFor="resume"
        className="flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-gray-300 p-10 transition hover:border-blue-500"
      >
        <Upload className="mb-3 h-10 w-10 text-gray-500" />

        <p className="font-medium">
          Drag & Drop Resume
        </p>

        <p className="text-sm text-gray-500">
          PDF only
        </p>

        <input
          id="resume"
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={handleFileChange}
        />
      </label>

      {file && (
        <div className="mt-4 flex items-center gap-2 rounded-lg bg-gray-100 p-3">
          <FileText className="h-5 w-5" />

          <span className="truncate">
            {file.name}
          </span>
        </div>
      )}

      {error && (
        <p className="mt-3 text-sm text-red-500">
          {error}
        </p>
      )}

      <button
        onClick={handleUpload}
        disabled={loading}
        className="mt-6 flex w-full items-center justify-center rounded-xl bg-blue-600 py-3 font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-gray-400"
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 h-5 w-5 animate-spin" />
            Analyzing...
          </>
        ) : (
          "Analyze Resume"
        )}
      </button>
    </div>
  );
}