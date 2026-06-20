"use client";

import { useAnalysis } from "@/context/AnalysisContext";
import JobRecommendations from "@/components/JobRecommendations";

export default function JobsPage() {
  const { analysis } = useAnalysis();

  if (!analysis) return null;

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-emerald-400">
          Recommendation Engine
        </p>

        <h1 className="mt-2 text-3xl font-bold text-white md:text-4xl">
          Job Recommendations
        </h1>

        <p className="mt-2 max-w-2xl text-slate-400">
          Relevant jobs generated using candidate profile matching, similarity scoring,
          candidate pooling, and diversity filtering.
        </p>
      </div>

      <JobRecommendations
        recommendations={analysis.recommendations}
      />
    </div>
  );
}