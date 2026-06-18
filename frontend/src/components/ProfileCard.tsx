import { Profile } from "@/types";

interface ProfileCardProps {
  profile: Profile;
}

export default function ProfileCard({
  profile,
}: ProfileCardProps) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg backdrop-blur">
      <h2 className="mb-4 text-xl font-bold text-white">
        Candidate Profile
      </h2>

      <div className="space-y-2 text-slate-300">
        <p>
          <strong className="text-slate-100">Job Title:</strong>{" "}
          {profile.job_title}
        </p>

        <p>
          <strong className="text-slate-100">Experience:</strong>{" "}
          {profile.experience_years} years
        </p>

        <p>
          <strong className="text-slate-100">Industry:</strong>{" "}
          {profile.industry}
        </p>

        <p>
          <strong className="text-slate-100">Location:</strong>{" "}
          {profile.location}
        </p>

        <p>
          <strong className="text-slate-100">Remote Work:</strong>{" "}
          {profile.remote_work}
        </p>

        <p>
          <strong className="text-slate-100">Certifications:</strong>{" "}
          {profile.certifications}
        </p>
      </div>

      <div className="mt-5">
        <h3 className="mb-2 font-semibold text-white">
          Skills
        </h3>

        <div className="flex flex-wrap gap-2">
          {profile.skills.map((skill) => (
            <span
              key={skill}
              className="rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-sm text-indigo-200 transition hover:bg-indigo-500/20"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}