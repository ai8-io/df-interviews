from pydantic import BaseModel


class EmployeeRow(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    role: str
    department: str
    salary: str
    currency: str
    location: str
    start_date: str
    contract_type: str
    manager: str
    phone: str
    skills: str
    last_review_rating: str
    annual_bonus_pct: str


class PaginatedEmployees(BaseModel):
    items: list[EmployeeRow]
    total: int
    page: int
    page_size: int
    total_pages: int


class DepartmentStats(BaseModel):
    department: str
    headcount: int
    avg_salary: float
    min_salary: float
    max_salary: float


class LocationCount(BaseModel):
    location: str
    count: int


class ContractBreakdown(BaseModel):
    contract_type: str
    count: int


class EmployeeStats(BaseModel):
    total_employees: int
    departments: list[DepartmentStats]
    locations: list[LocationCount]
    contract_types: list[ContractBreakdown]
    avg_salary: float
    avg_review_rating: float
