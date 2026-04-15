import { useEffect, useState } from "react";
import { fetchEmployeeStats, type EmployeeStats } from "../api/employees";
import StatsCards from "../components/StatsCards";
import EmployeeTable from "../components/EmployeeTable";

export default function Dashboard() {
  const [stats, setStats] = useState<EmployeeStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchEmployeeStats()
      .then(setStats)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="mx-auto max-w-6xl px-8 py-8">
        <div className="mb-6">
          <h1 className="text-xl font-semibold text-gray-900">
            Employee Directory
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Browse and search the Acme Corp employee database
          </p>
        </div>

        {loading && (
          <div className="py-12 text-center text-gray-400">Loading stats...</div>
        )}

        {stats && (
          <div className="mb-8">
            <StatsCards stats={stats} />
          </div>
        )}

        <div className="mb-4">
          <h2 className="text-base font-semibold text-gray-900">All Employees</h2>
        </div>
        <EmployeeTable />
      </div>
    </div>
  );
}
