"use client";

import { useAnalysis } from "@/context/AnalysisContext";
import ProfileCard from "@/components/ProfileCard";

export default function DashboardPage() {
  const { analysis } = useAnalysis();

  if (!analysis) return null;

  const topMatch =
    analysis.recommendations.length > 0
      ? Math.max(
        // spread syntax to dissemble array and pass individually to Mathmax function
          ...analysis.recommendations.map(
            (job) => job.match_percentage
          )
        )
      : 0;

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-emerald-400">
          Overview
        </p>

        <h1 className="mt-2 text-3xl font-bold text-white md:text-4xl">
          Candidate Profile
        </h1>

        <p className="mt-2 max-w-2xl text-slate-400">
          Extracted profile information from the uploaded resume.
        </p>
      </div>

      <div className="mb-8 grid gap-4 md:grid-cols-3">
        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-sm">
          <p className="text-sm text-slate-400">
            Recommendations
          </p>

          <p className="mt-2 text-3xl font-bold text-white">
            {analysis.recommendations.length}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-sm">
          <p className="text-sm text-slate-400">
            Skills Detected
          </p>

          <p className="mt-2 text-3xl font-bold text-white">
            {analysis.profile.skills.length}
          </p>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5 shadow-sm">
          <p className="text-sm text-slate-400">
            Best Match
          </p>

          <p className="mt-2 text-3xl font-bold text-emerald-400">
            {topMatch}%
          </p>
        </div>
      </div>

      <ProfileCard profile={analysis.profile} />
    </div>
  );
}