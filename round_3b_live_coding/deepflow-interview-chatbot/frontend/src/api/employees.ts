export interface EmployeeRow {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  role: string;
  department: string;
  salary: string;
  currency: string;
  location: string;
  start_date: string;
  contract_type: string;
  manager: string;
  phone: string;
  skills: string;
  last_review_rating: string;
  annual_bonus_pct: string;
}

export interface PaginatedEmployees {
  items: EmployeeRow[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface DepartmentStats {
  department: string;
  headcount: number;
  avg_salary: number;
  min_salary: number;
  max_salary: number;
}

export interface LocationCount {
  location: string;
  count: number;
}

export interface ContractBreakdown {
  contract_type: string;
  count: number;
}

export interface EmployeeStats {
  total_employees: number;
  departments: DepartmentStats[];
  locations: LocationCount[];
  contract_types: ContractBreakdown[];
  avg_salary: number;
  avg_review_rating: number;
}

export interface EmployeeFilters {
  page?: number;
  page_size?: number;
  search?: string;
  department?: string;
  location?: string;
  contract_type?: string;
  sort_by?: string;
  sort_order?: string;
}

export async function fetchEmployees(
  filters: EmployeeFilters = {},
): Promise<PaginatedEmployees> {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== "") {
      params.set(key, String(val));
    }
  });
  const res = await fetch(`/api/employees?${params}`);
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchEmployeeStats(): Promise<EmployeeStats> {
  const res = await fetch("/api/employees/stats");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchDepartments(): Promise<string[]> {
  const res = await fetch("/api/employees/departments");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}

export async function fetchLocations(): Promise<string[]> {
  const res = await fetch("/api/employees/locations");
  if (!res.ok) throw new Error(`Failed: ${res.status}`);
  return res.json();
}
