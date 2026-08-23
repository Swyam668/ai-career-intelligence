import { SalaryResult } from "@/types";

type SalaryCardProps = {
  result: SalaryResult;
  profile: {
    company_size: string;
    location: string;
    remote_work: string;
  };
};



function formatCurrency(value: number) {
  // indian currency formatting
  // Intl - Internationalization js object
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}



export default function SalaryCard({
  result,
  profile,
}: SalaryCardProps) {


  return (
    // <div className="rounded-2xl border bg-white p-6 shadow-sm">
    //   <h2 className="text-xl font-semibold text-gray-900">
    //     Predicted Salary
    //   </h2>

    //   <p className="mt-4 text-4xl font-bold text-green-600">
    //     ₹ {salaryLpa}
    //   </p>

    //   <p className="mt-2 text-sm text-gray-500">
    //     Estimated annual salary based on your resume profile.
    //   </p>
    // </div>

    <div>
  {result.predicted_salary && (
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-8 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)]">
      {/* Background Glow */}
      <div className="absolute -top-20 -right-20 h-64 w-64 rounded-full bg-emerald-500/10 blur-3xl" />
      <div className="absolute -bottom-20 -left-20 h-64 w-64 rounded-full bg-cyan-500/10 blur-3xl" />

      <div className="relative mb-8">
        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-emerald-400">
          Salary Prediction
        </p>

        <h2 className="mt-3 text-5xl font-black tracking-tight text-white">
          {formatCurrency(result.predicted_salary)}
        </h2>

        <p className="mt-3 text-sm text-slate-400">
          Baseline estimate:
          <span className="ml-2 font-semibold text-slate-200">
            {formatCurrency(result.base_salary)}
          </span>
        </p>
      </div>

      <div className="relative rounded-2xl border border-white/10 bg-white/5 p-5 backdrop-blur-xl">
        <p className="text-sm font-semibold text-white">
          Why this salary was predicted
        </p>

        <p className="mt-2 text-sm text-slate-400">
          These factors explain how the model adjusted the estimate from the
          baseline.
        </p>

        <div className="mt-5 space-y-4">
          {result.explanation.map((item) => (
            <div
              key={item.feature}
              className="group flex items-start justify-between gap-4 rounded-2xl border border-white/10 bg-slate-900/50 p-5 transition-all duration-300 hover:border-emerald-500/30 hover:bg-slate-900"
            >
              <div>
                <p className="font-semibold text-white">
                  {item.title}
                </p>

                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {item.message}
                </p>
              </div>

              <span
                className={`shrink-0 rounded-full px-4 py-2 text-sm font-bold shadow-lg ${
                  item.effect === "positive"
                    ? "border border-emerald-500/30 bg-emerald-500/15 text-emerald-300"
                    : "border border-rose-500/30 bg-rose-500/15 text-rose-300"
                }`}
              >
                {item.impact > 0 ? "+" : "-"}
                {formatCurrency(Math.abs(item.impact))}
              </span>
            </div>
          ))}
        </div>
      </div>

    </section>
  )}
</div>

  );
}