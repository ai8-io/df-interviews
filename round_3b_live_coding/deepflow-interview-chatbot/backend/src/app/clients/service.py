import logging

from app.clients.repository import ClientRepository

logger = logging.getLogger(__name__)


class ClientService:
    """Thin wrapper around the client data repository."""

    def __init__(self) -> None:
        self._repo = ClientRepository()

    def get_all_employees(self) -> list[dict[str, str]]:
        return self._repo.get_all_employees()

    def format_employee_context(self) -> str:
        """Format the entire employee dataset as a string for LLM context injection."""
        employees = self.get_all_employees()
        if not employees:
            logger.warning("no employee data found")
            return "No employee data available."

        headers = list(employees[0].keys())
        lines = [",".join(headers)]
        for emp in employees:
            lines.append(",".join(emp.get(h, "") for h in headers))
        context = "\n".join(lines)
        logger.info(
            "formatted employee context rows=%d chars=%d", len(employees), len(context)
        )
        return context
