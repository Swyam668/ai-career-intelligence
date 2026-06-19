type SalaryCardProps = {
  predictedSalary: number;
  predictedSalaryLpa?: number;
  profile: {
    company_size: string;
    location: string;
    remote_work: string;
  };
};

export default function SalaryCard({
  predictedSalary,
  predictedSalaryLpa,
  profile,
}: SalaryCardProps) {
  const salaryLpa =
    predictedSalary

  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">
      <h2 className="text-xl font-semibold text-gray-900">
        Predicted Salary
      </h2>

      <p className="mt-4 text-4xl font-bold text-green-600">
        ₹{salaryLpa} LPA
      </p>

      <p className="mt-2 text-sm text-gray-500">
        Estimated annual salary based on your resume profile.
      </p>

      {/* <div className="mt-5 rounded-xl bg-gray-50 p-4">
        <p className="text-sm font-medium text-gray-700">
          Assumptions used
        </p>

        <div className="mt-3 space-y-2 text-sm text-gray-600">
          <p>Company Size: {profile.company_size}</p>
          <p>Location: {profile.location}</p>
          <p>Remote Work: {profile.remote_work}</p>
        </div>
      </div> */}
    </div>
  );
}