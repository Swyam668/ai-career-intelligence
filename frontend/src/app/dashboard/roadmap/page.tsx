"use client";

import { useAnalysis } from "@/context/AnalysisContext";
import CareerRoadmap from "@/components/CareerRoadmap";

export default function RoadmapPage() {
  const { analysis } = useAnalysis();

  if (!analysis) return null;

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-emerald-400">
          Personalized Growth Plan
        </p>

        <h1 className="mt-2 text-3xl font-bold text-white md:text-4xl">
          Career Roadmap
        </h1>

        <p className="mt-2 max-w-2xl text-slate-400">
          A personalized learning and project roadmap based on your target role,
          missing skills, matched skills, and readiness score.
        </p>
      </div>

      {analysis.career_roadmap ? (
        <CareerRoadmap roadmap={analysis.career_roadmap} />
      ) : (
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 text-slate-400">
          Career roadmap was not generated for this analysis.
        </div>
      )}
    </div>
  );
}