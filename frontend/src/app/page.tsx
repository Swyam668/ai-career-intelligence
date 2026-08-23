"use client";

import ResumeUpload from "@/components/ResumeUpload";
import { useAnalysis } from "@/context/AnalysisContext";
import { AnalysisResponse } from "@/types";
import { useRouter } from "next/navigation";

export default function Home() {
  // context for sent json (predictions) from backend - making it available to all components without passing as props
  const { setAnalysis } = useAnalysis();
  const router = useRouter();

  const handleSuccess = (data: AnalysisResponse) => {
    setAnalysis(data);

    router.push("/dashboard");
  };

  return (
    <main className="flex min-h-screen items-center justify-center">
      <ResumeUpload onSuccess={handleSuccess} />
    </main>
  );
}