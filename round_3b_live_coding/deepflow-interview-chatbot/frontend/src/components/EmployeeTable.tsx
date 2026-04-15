import { useCallback, useEffect, useState } from "react";
import {
  fetchEmployees,
  fetchDepartments,
  fetchLocations,
  type EmployeeRow,
  type EmployeeFilters,
  type PaginatedEmployees,
} from "../api/employees";

export default function EmployeeTable() {
  const [data, setData] = useState<PaginatedEmployees | null>(null);
  const [departments, setDepartments] = useState<string[]>([]);
  const [locations, setLocations] = useState<string[]>([]);
  const [filters, setFilters] = useState<EmployeeFilters>({
    page: 1,
    page_size: 20,
    sort_by: "id",
    sort_order: "asc",
  });
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const result = await fetchEmployees(filters);
      setData(result);
    } catch {
      /* handled by empty state */
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    Promise.all([fetchDepartments(), fetchLocations()]).then(
      ([depts, locs]) => {
        setDepartments(depts);
        setLocations(locs);
      },
    );
  }, []);

  const updateFilter = (key: keyof EmployeeFilters, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value || undefined,
      ...(key !== "page" ? { page: 1 } : {}),
    }));
  };

  const handleSort = (col: string) => {
    setFilters((prev) => ({
      ...prev,
      sort_by: col,
      sort_order:
        prev.sort_by === col && prev.sort_order === "asc" ? "desc" : "asc",
      page: 1,
    }));
  };

  const sortIndicator = (col: string) => {
    if (filters.sort_by !== col) return "";
    return filters.sort_order === "asc" ? " \u2191" : " \u2193";
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <input
          type="text"
          placeholder="Search name, email, role, skills..."
          className="w-64 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-900 placeholder-gray-400 outline-none focus:border-blue-300 focus:ring-2 focus:ring-blue-100"
          onChange={(e) => updateFilter("search", e.target.value)}
        />
        <select
          className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 outline-none"
          onChange={(e) => updateFilter("department", e.target.value)}
          defaultValue=""
        >
          <option value="">All departments</option>
          {departments.map((d) => (
            <option key={d} value={d}>
              {d}
            </option>
          ))}
        </select>
        <select
          className="rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm text-gray-700 outline-none"
          onChange={(e) => updateFilter("location", e.target.value)}
          defaultValue=""
        >
          <option value="">All locations</option>
          {locations.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
        {data && (
          <span className="ml-auto text-xs text-gray-500">
            {data.total} employees found
          </span>
        )}
      </div>

      <div className="overflow-hidden rounded-xl border border-gray-200 bg-white">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-gray-100 bg-gray-50">
                {COLUMNS.map((col) => (
                  <th
                    key={col.key}
                    className="cursor-pointer whitespace-nowrap px-4 py-3 text-xs font-medium uppercase tracking-wide text-gray-500 hover:text-gray-700"
                    onClick={() => handleSort(col.key)}
                  >
                    {col.label}
                    {sortIndicator(col.key)}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr>
                  <td colSpan={COLUMNS.length} className="px-4 py-8 text-center text-gray-400">
                    Loading...
                  </td>
                </tr>
              )}
              {!loading && data?.items.length === 0 && (
                <tr>
                  <td colSpan={COLUMNS.length} className="px-4 py-8 text-center text-gray-400">
                    No employees match your filters
                  </td>
                </tr>
              )}
              {!loading &&
                data?.items.map((emp) => (
                  <tr
                    key={emp.id}
                    className="border-b border-gray-50 transition-colors hover:bg-gray-50"
                  >
                    <td className="px-4 py-3 font-medium text-gray-900">
                      {emp.first_name} {emp.last_name}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{emp.role}</td>
                    <td className="px-4 py-3 text-gray-600">{emp.department}</td>
                    <td className="px-4 py-3 text-gray-600">{emp.location}</td>
                    <td className="px-4 py-3 text-gray-600">
                      {emp.currency === "GBP" ? "£" : emp.currency}{" "}
                      {Number(emp.salary).toLocaleString()}
                    </td>
                    <td className="px-4 py-3 text-gray-600">{emp.contract_type}</td>
                    <td className="px-4 py-3 text-gray-600">{emp.start_date}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>

      {data && data.total_pages > 1 && (
        <div className="flex items-center justify-between">
          <button
            disabled={data.page <= 1}
            onClick={() => updateFilter("page", String(data.page - 1))}
            className="rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 transition-colors hover:bg-gray-50 disabled:opacity-40"
          >
            Previous
          </button>
          <span className="text-sm text-gray-500">
            Page {data.page} of {data.total_pages}
          </span>
          <button
            disabled={data.page >= data.total_pages}
            onClick={() => updateFilter("page", String(data.page + 1))}
            className="rounded-lg border border-gray-200 px-3 py-1.5 text-sm text-gray-600 transition-colors hover:bg-gray-50 disabled:opacity-40"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}

const COLUMNS = [
  { key: "first_name", label: "Name" },
  { key: "role", label: "Role" },
  { key: "department", label: "Department" },
  { key: "location", label: "Location" },
  { key: "salary", label: "Salary" },
  { key: "contract_type", label: "Contract" },
  { key: "start_date", label: "Start Date" },
];
