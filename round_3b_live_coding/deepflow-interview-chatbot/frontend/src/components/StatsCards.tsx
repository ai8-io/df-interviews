import type { EmployeeStats } from "../api/employees";

interface Props {
  stats: EmployeeStats;
}

function formatCurrency(val: number): string {
  return new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
    maximumFractionDigits: 0,
  }).format(val);
}

export default function StatsCards({ stats }: Props) {
  return (
    <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
      <Card label="Total Employees" value={stats.total_employees.toString()} />
      <Card label="Avg Salary" value={formatCurrency(stats.avg_salary)} />
      <Card label="Departments" value={stats.departments.length.toString()} />
      <Card
        label="Avg Review"
        value={stats.avg_review_rating.toFixed(1) + " / 5"}
      />

      <div className="col-span-2 rounded-xl border border-gray-200 bg-white p-4">
        <h3 className="mb-3 text-xs font-medium uppercase tracking-wide text-gray-500">
          By Department
        </h3>
        <div className="space-y-2">
          {stats.departments.slice(0, 8).map((d) => (
            <div key={d.department} className="flex items-center justify-between text-sm">
              <span className="text-gray-700">{d.department}</span>
              <div className="flex items-center gap-3">
                <span className="text-xs text-gray-400">{d.headcount} people</span>
                <span className="font-medium text-gray-900">
                  {formatCurrency(d.avg_salary)}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="col-span-2 rounded-xl border border-gray-200 bg-white p-4">
        <h3 className="mb-3 text-xs font-medium uppercase tracking-wide text-gray-500">
          By Location
        </h3>
        <div className="space-y-2">
          {stats.locations.slice(0, 8).map((l) => {
            const pct = Math.round((l.count / stats.total_employees) * 100);
            return (
              <div key={l.location} className="flex items-center gap-3 text-sm">
                <span className="w-32 truncate text-gray-700">{l.location}</span>
                <div className="flex-1">
                  <div className="h-2 rounded-full bg-gray-100">
                    <div
                      className="h-2 rounded-full bg-blue-500"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
                <span className="w-12 text-right text-xs text-gray-500">
                  {l.count}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

function Card({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
        {label}
      </p>
      <p className="mt-1 text-2xl font-semibold text-gray-900">{value}</p>
    </div>
  );
}
