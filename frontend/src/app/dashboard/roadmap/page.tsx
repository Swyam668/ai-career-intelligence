"use client";

import { useAnalysis } from "@/context/AnalysisContext";
import CareerRoadmap from "@/components/CareerRoadmap";
import { useState } from "react";

export default function RoadmapPage() {
  const { analysis } = useAnalysis();
  const [roadmap, setRoadmap] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (!analysis) return null;

  const generateRoadmap = async () => {
    if (!analysis) {
      setError("No analysis data found. Please upload and analyze a resume first.");
      console.error("No analysis data found");
      return;
    }

    try {
      setLoading(true);
      setError("");

      console.log("Sending roadmap request:", {
        profile: analysis.profile,
        recommendations: analysis.recommendations,
      });

      const res = await fetch("http://localhost:8000/generate-roadmap", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile: analysis.profile,
          recommendations: analysis.recommendations,
        }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Backend error: ${res.status} - ${errorText}`);
      }

      const data = await res.json();

      console.log("Roadmap response:", data);

      setRoadmap(data.roadmap);
    } catch (error: any) {
      console.error("Roadmap generation failed:", error);
      setError(error.message || "Something went wrong while generating roadmap.");
    } finally {
      setLoading(false);
    }
  };

  

  return (
  <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-6 md:p-10">
    <div className="mx-auto max-w-6xl">
      {/* Header */}
      <div className="mb-10">
        <div className="inline-flex items-center rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-1.5">
          <p className="text-sm font-semibold tracking-wide text-emerald-400">
            Personalized Growth Plan
          </p>
        </div>

        <h1 className="mt-5 bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-4xl font-extrabold text-transparent md:text-6xl">
          Career Roadmap
        </h1>

        <p className="mt-4 max-w-3xl text-lg leading-relaxed text-slate-400">
          A personalized learning and project roadmap based on your target role,
          missing skills, matched skills, and readiness score.
        </p>
      </div>

      {/* Error Messages */}
      {!analysis && (
        <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/10 p-4 backdrop-blur-sm">
          <p className="font-medium text-red-400">
            No resume analysis found. Please upload your resume first.
          </p>
        </div>
      )}

      {error && (
        <div className="mb-6 rounded-2xl border border-red-500/20 bg-red-500/10 p-4 backdrop-blur-sm">
          <p className="font-medium text-red-400">{error}</p>
        </div>
      )}

      {/* CTA Card */}
      <div className="mb-8 overflow-hidden rounded-3xl border border-slate-800 bg-slate-900/60 p-8 shadow-[0_0_50px_rgba(16,185,129,0.08)] backdrop-blur-xl">
        <div className="flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white">
              Generate Your Career Path
            </h2>

            <p className="mt-2 max-w-2xl text-slate-400">
              Get a structured roadmap with learning resources, project ideas,
              and milestones tailored to your profile.
            </p>
          </div>

          <button
            onClick={generateRoadmap}
            disabled={loading}
            className="group relative overflow-hidden rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-500 px-8 py-4 font-semibold text-white transition-all duration-300 hover:scale-[1.03] hover:shadow-[0_0_35px_rgba(16,185,129,0.45)] disabled:cursor-not-allowed disabled:opacity-60"
          >
            <span className="relative z-10">
              {loading ? "Generating..." : "Generate Career Roadmap"}
            </span>

            <div className="absolute inset-0 translate-y-full bg-white/10 transition-transform duration-300 group-hover:translate-y-0" />
          </button>
        </div>
      </div>

      {/* Content */}
      {roadmap ? (
        <div className="rounded-3xl border border-slate-800 bg-slate-900/40 p-4 backdrop-blur-xl">
          <CareerRoadmap roadmap={roadmap} />
        </div>
      ) : (
        <div className="rounded-3xl border border-dashed border-slate-700 bg-slate-900/40 p-12 text-center backdrop-blur-xl">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-800">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-8 w-8 text-slate-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={1.8}
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>

          <h3 className="text-xl font-semibold text-white">
            No Roadmap Generated Yet
          </h3>

          <p className="mt-3 text-slate-400">
            Generate a personalized roadmap to see recommended skills,
            projects, and career milestones.
          </p>
        </div>
      )}
    </div>
  </div>
);
}