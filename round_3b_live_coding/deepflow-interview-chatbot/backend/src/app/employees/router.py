import logging

from fastapi import APIRouter, Query

from app.employees.schemas import EmployeeStats, PaginatedEmployees
from app.employees.service import EmployeeService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/employees", tags=["employees"])

_service = EmployeeService()


@router.get("", response_model=PaginatedEmployees)
async def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    search: str | None = Query(None),
    department: str | None = Query(None),
    location: str | None = Query(None),
    contract_type: str | None = Query(None),
    sort_by: str = Query("id"),
    sort_order: str = Query("asc"),
) -> PaginatedEmployees:
    logger.info(
        "GET /api/employees page=%d search=%s department=%s location=%s",
        page,
        search,
        department,
        location,
    )
    return _service.list_employees(
        page=page,
        page_size=page_size,
        search=search,
        department=department,
        location=location,
        contract_type=contract_type,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get("/stats", response_model=EmployeeStats)
async def get_stats() -> EmployeeStats:
    logger.info("GET /api/employees/stats")
    return _service.get_stats()


@router.get("/departments")
async def get_departments() -> list[str]:
    return _service.get_departments()


@router.get("/locations")
async def get_locations() -> list[str]:
    return _service.get_locations()
