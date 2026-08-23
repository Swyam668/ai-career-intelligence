
type RoadmapPhase = {
  phase: string;
  duration: string;
  focus: string;
  skills: string[];
  action_items: string[];
};

type CareerRoadmapData = {
  target_role: string;
  readiness_score: number;
  current_strengths: string[];
  priority_skills: string[];
  estimated_timeline: string;
  roadmap: RoadmapPhase[];
  project_suggestions: string[];
};

type CareerRoadmapProps = {
  roadmap: CareerRoadmapData;
};

export default function CareerRoadmap({ roadmap }: CareerRoadmapProps) {
  if (!roadmap) return null;

  return (
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 p-8 shadow-[0_20px_80px_rgba(0,0,0,0.35)] backdrop-blur-xl">
      <div className="mb-6">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-blue-400">
          Personalized Career Roadmap
        </p>

        <div className="mt-2 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-white">
              {roadmap.target_role}
            </h2>

            <p className="mt-2 text-sm text-slate-400">
              Estimated timeline: {roadmap.estimated_timeline}
            </p>
          </div>

          <div className="rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-violet-500/10 px-6 py-4 text-center backdrop-blur-sm">
            <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
              Readiness Score
            </p>

            <p className="text-3xl font-bold text-white">
              {roadmap.readiness_score}%
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5 backdrop-blur-sm">
          <h3 className="font-semibold text-emerald-400">
            Current Strengths
          </h3>

          {roadmap.current_strengths?.length > 0 ? (
            <div className="mt-3 flex flex-wrap gap-2">
              {roadmap.current_strengths.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-sm font-medium text-emerald-300 transition-all hover:bg-emerald-500/20"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="mt-2 text-sm text-emerald-300">
              No strong matched skills found yet.
            </p>
          )}
        </div>

        <div className="rounded-2xl border border-amber-500/20 bg-amber-500/5 p-5 backdrop-blur-sm">
          <h3 className="font-semibold text-amber-400">
            Priority Skills
          </h3>

          {roadmap.priority_skills?.length > 0 ? (
            <div className="mt-3 flex flex-wrap gap-2">
              {roadmap.priority_skills.map((skill) => (
                <span
                  key={skill}
                  className="rounded-full border border-amber-500/20 bg-amber-500/10 px-3 py-1.5 text-sm font-medium text-amber-300 transition-all hover:bg-amber-500/20"
                >
                  {skill}
                </span>
              ))}
            </div>
          ) : (
            <p className="mt-2 text-sm text-amber-300">
              No major missing skills detected.
            </p>
          )}
        </div>
      </div>

      <div className="mt-6">
        <h3 className="mb-5 text-xl font-semibold text-white">
          Roadmap Phases
        </h3>

        <div className="space-y-4">
          {roadmap.roadmap?.map((phase, index) => (
            <div
              key={`${phase.phase}-${index}`}
              className="group relative overflow-hidden rounded-2xl border border-slate-800 bg-slate-900/60 p-6 pl-8 before:absolute before:left-3 before:top-0 before:h-full before:w-px before:bg-gradient-to-b before:from-blue-500 before:via-violet-500 before:to-transparent after:absolute after:left-[7px] after:top-7 after:h-3 after:w-3 after:rounded-full after:bg-blue-400 transition-all duration-300 hover:border-blue-500/30 hover:bg-slate-900 hover:shadow-[0_0_40px_rgba(59,130,246,0.12)]"
            >
              <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <h4 className="text-lg font-semibold text-white">
                    {phase.phase}
                  </h4>

                  <p className="mt-2 text-sm leading-relaxed text-slate-400">
                    {phase.focus}
                  </p>
                </div>

                <span className="w-fit rounded-full border border-blue-500/20 bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-300">
                  {phase.duration}
                </span>
              </div>

              {phase.skills?.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {phase.skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full border border-slate-700 bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-300 transition-all hover:border-blue-500/30 hover:text-blue-300"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              )}

              {phase.action_items?.length > 0 && (
                <ul className="mt-5 space-y-3">
                  {phase.action_items.map((item, itemIndex) => (
                    <li
                      key={`${item}-${itemIndex}`}
                      className="flex gap-3 text-sm text-slate-300"
                    >
                      <span className="font-semibold text-blue-400">
                        {itemIndex + 1}.
                      </span>

                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>

      {roadmap.project_suggestions?.length > 0 && (
        <div className="mt-8 rounded-2xl border border-violet-500/20 bg-linear-to-br from-violet-500/10 to-blue-500/10 p-5 backdrop-blur-sm">
          <h3 className="font-semibold text-violet-300">
            Suggested Portfolio Projects
          </h3>

          <ul className="mt-4 space-y-3">
            {roadmap.project_suggestions.map((project, index) => (
              <li
                key={`${project}-${index}`}
                className="flex gap-3 text-sm text-slate-200"
              >
                <span className="font-semibold text-violet-400">
                  {index + 1}.
                </span>

                <span>{project}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
