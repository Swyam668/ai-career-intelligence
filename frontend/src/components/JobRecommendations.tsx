import { Recommendation } from "@/types";

interface JobRecommendationsProps {
  recommendations: Recommendation[];
}

export default function JobRecommendations({
  recommendations,
}: JobRecommendationsProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg backdrop-blur text-slate-200">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">
          Job Recommendations
        </h2>

        <span className="rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-sm font-medium text-indigo-200">
          {recommendations.length} Results
        </span>
      </div>

      <div className="space-y-6">
        {recommendations.map((job, index) => (
          <div
            key={`${job.role}-${index}`}
            className="rounded-xl border border-slate-800 bg-slate-950/40 p-5 shadow-sm"
          >
            {/* Header */}
            <div className="mb-4 flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold text-white">
                  {job.role}
                </h3>

                <p className="text-sm text-slate-400">
                  {job.job_title}
                </p>
              </div>

              <div className="text-right">
                <p className="text-lg font-bold text-emerald-400">
                  {job.match_percentage}%
                </p>

                <p className="text-xs text-slate-500">
                  Match
                </p>
              </div>
            </div>

            {/* Match Bar */}
            <div className="mb-4">
              <div className="h-2 w-full rounded-full bg-slate-800">
                <div
                  className="h-2 rounded-full bg-emerald-500"
                  style={{
                    width: `${job.match_percentage}%`,
                  }}
                />
              </div>
            </div>

            {/* Details */}
            <div className="mb-4 grid gap-3 md:grid-cols-2">
              <div>
                <p className="text-sm text-slate-500">
                  Qualification
                </p>

                <p className="font-medium text-slate-200">
                  {job.qualifications}
                </p>
              </div>

              <div>
                <p className="text-sm text-slate-500">
                  Experience Required
                </p>

                <p className="font-medium text-slate-200">
                  {job.experience}
                </p>
              </div>

              <div>
                <p className="text-sm text-slate-500">
                  Similarity Score
                </p>

                <p className="font-medium text-slate-200">
                  {job.similarity_score.toFixed(4)}
                </p>
              </div>
            </div>

            {/* Matched Skills */}
            <div className="mb-4">
              <h4 className="mb-2 font-semibold text-emerald-300">
                Matched Skills
              </h4>

              <div className="flex flex-wrap gap-2">
                {job.matched_skills.map((skill) => (
                  <span
                    key={skill}
                    className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-sm text-emerald-200"
                  >
                    ✓ {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Missing Skills */}
            {job.missing_skills.length > 0 && (
              <div>
                <h4 className="mb-2 font-semibold text-rose-300">
                  Missing Skills
                </h4>

                <div className="flex flex-wrap gap-2">
                  {job.missing_skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full border border-rose-500/20 bg-rose-500/10 px-3 py-1 text-sm text-rose-200"
                    >
                      ✗ {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}