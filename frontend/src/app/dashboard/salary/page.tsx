"use client";

import { useAnalysis } from "@/context/AnalysisContext";
import SalaryCard from "@/components/SalaryCard";

export default function SalaryPage() {
  const { analysis } = useAnalysis();

  if (!analysis) return null;

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-emerald-400">
          ML Salary Estimation
        </p>

        <h1 className="mt-2 text-3xl font-bold text-white md:text-4xl">
          Salary Prediction
        </h1>

        <p className="mt-2 max-w-2xl text-slate-400">
          Estimated salary insights based on resume-derived features and the trained ML model.
        </p>
      </div>

      <SalaryCard
        result={analysis.salary}
        profile={analysis.profile}
      />
    </div>
  );
}