import logging
from collections import defaultdict

from app.clients.repository import ClientRepository
from app.employees.schemas import (
    ContractBreakdown,
    DepartmentStats,
    EmployeeRow,
    EmployeeStats,
    LocationCount,
    PaginatedEmployees,
)
from app.utils.tokens import count_tokens

logger = logging.getLogger(__name__)


class EmployeeService:
    def __init__(self) -> None:
        self._repo = ClientRepository()

    def list_employees(
        self,
        page: int = 1,
        page_size: int = 25,
        search: str | None = None,
        department: str | None = None,
        location: str | None = None,
        contract_type: str | None = None,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> PaginatedEmployees:
        employees = self._repo.get_all_employees()

        if search:
            q = search.lower()
            employees = [
                e
                for e in employees
                if q in e.get("first_name", "").lower()
                or q in e.get("last_name", "").lower()
                or q in e.get("email", "").lower()
                or q in e.get("role", "").lower()
                or q in e.get("skills", "").lower()
            ]
        if department:
            employees = [
                e
                for e in employees
                if e.get("department", "").lower() == department.lower()
            ]
        if location:
            employees = [
                e
                for e in employees
                if e.get("location", "").lower() == location.lower()
            ]
        if contract_type:
            employees = [
                e
                for e in employees
                if e.get("contract_type", "").lower() == contract_type.lower()
            ]

        reverse = sort_order.lower() == "desc"
        if sort_by == "salary":
            employees.sort(
                key=lambda e: _parse_salary(e.get("salary", "0")), reverse=reverse
            )
        elif sort_by in ("first_name", "last_name", "department", "location", "role"):
            employees.sort(key=lambda e: e.get(sort_by, "").lower(), reverse=reverse)
        else:
            employees.sort(key=lambda e: int(e.get("id", "0")), reverse=reverse)

        total = len(employees)
        total_pages = max(1, (total + page_size - 1) // page_size)
        start = (page - 1) * page_size
        page_items = employees[start : start + page_size]

        logger.info(
            "list_employees total=%d page=%d/%d results=%d est_tokens=%d",
            total,
            page,
            total_pages,
            len(page_items),
            count_tokens(str(page_items)),
        )

        return PaginatedEmployees(
            items=[EmployeeRow(**_normalize_row(e)) for e in page_items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        )

    def get_stats(self) -> EmployeeStats:
        employees = self._repo.get_all_employees()

        dept_data: dict[str, list[float]] = defaultdict(list)
        location_counts: dict[str, int] = defaultdict(int)
        contract_counts: dict[str, int] = defaultdict(int)
        all_salaries: list[float] = []
        all_ratings: list[float] = []

        for e in employees:
            salary = _parse_salary(e.get("salary", "0"))
            dept = e.get("department", "Unknown")
            dept_data[dept].append(salary)
            all_salaries.append(salary)
            location_counts[e.get("location", "Unknown")] += 1
            contract_counts[e.get("contract_type", "Unknown")] += 1

            try:
                rating = float(e.get("last_review_rating", "0"))
                if rating > 0:
                    all_ratings.append(rating)
            except ValueError:
                pass

        departments = [
            DepartmentStats(
                department=dept,
                headcount=len(salaries),
                avg_salary=sum(salaries) / len(salaries) if salaries else 0,
                min_salary=min(salaries) if salaries else 0,
                max_salary=max(salaries) if salaries else 0,
            )
            for dept, salaries in sorted(dept_data.items())
        ]

        locations = [
            LocationCount(location=loc, count=count)
            for loc, count in sorted(location_counts.items(), key=lambda x: -x[1])
        ]

        contracts = [
            ContractBreakdown(contract_type=ct, count=count)
            for ct, count in sorted(contract_counts.items(), key=lambda x: -x[1])
        ]

        return EmployeeStats(
            total_employees=len(employees),
            departments=departments,
            locations=locations,
            contract_types=contracts,
            avg_salary=sum(all_salaries) / len(all_salaries) if all_salaries else 0,
            avg_review_rating=sum(all_ratings) / len(all_ratings) if all_ratings else 0,
        )

    def get_departments(self) -> list[str]:
        employees = self._repo.get_all_employees()
        return sorted(
            {e.get("department", "") for e in employees if e.get("department")}
        )

    def get_locations(self) -> list[str]:
        employees = self._repo.get_all_employees()
        return sorted({e.get("location", "") for e in employees if e.get("location")})


def _parse_salary(val: str) -> float:
    try:
        cleaned = (
            val.replace(",", "")
            .replace("£", "")
            .replace("$", "")
            .replace("€", "")
            .strip()
        )
        return float(cleaned) if cleaned else 0.0
    except ValueError:
        return 0.0


def _normalize_row(row: dict[str, str]) -> dict[str, str]:
    return {
        "id": row.get("id", ""),
        "first_name": row.get("first_name", ""),
        "last_name": row.get("last_name", ""),
        "email": row.get("email", ""),
        "role": row.get("role", ""),
        "department": row.get("department", ""),
        "salary": row.get("salary", ""),
        "currency": row.get("currency", ""),
        "location": row.get("location", ""),
        "start_date": row.get("start_date", ""),
        "contract_type": row.get("contract_type", ""),
        "manager": row.get("manager", ""),
        "phone": row.get("phone", ""),
        "skills": row.get("skills", ""),
        "last_review_rating": row.get("last_review_rating", ""),
        "annual_bonus_pct": row.get("annual_bonus_pct", ""),
    }
