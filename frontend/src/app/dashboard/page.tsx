"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { useAnalysis } from "@/context/AnalysisContext";

import ProfileCard from "@/components/ProfileCard";
import JobRecommendations from "@/components/JobRecommendations";
import SalaryCard from "@/components/SalaryCard";

export default function DashboardPage() {
  const { analysis } = useAnalysis();
  const router = useRouter();

  useEffect(() => {
    // if no json from backend found, send em back
    if (!analysis) {
      router.replace("/");
    }
  }, [analysis, router]);

  if (!analysis) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-200">
        <p className="text-slate-400">Loading...</p>
      </main>
    );
  }

  const topMatch =
    analysis.recommendations.length > 0
      ? Math.max(
          ...analysis.recommendations.map(
            (job) => job.match_percentage
          )
        )
      : 0;

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white">
            Career Intelligence Dashboard
          </h1>

          <p className="mt-2 text-slate-400">
            Personalized recommendations generated
            from your resume.
          </p>
        </div>

        {/* Stats */}
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

        {/* Content */}
        <div className="space-y-8">

          <ProfileCard
            profile={analysis.profile}
          />

          <SalaryCard
            result={analysis.salary}
            profile={analysis.profile}
          />

          <JobRecommendations
            recommendations={
              analysis.recommendations
            }
          />
          
        </div>
      </div>
    </main>
  );
}