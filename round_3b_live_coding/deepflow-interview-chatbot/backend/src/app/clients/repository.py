import csv
import logging
from pathlib import Path

from app.config import settings

logger = logging.getLogger(__name__)


class ClientRepository:
    """Reads employee data from the CSV file on disk.

    Each call re-reads the file from disk — there is no caching layer.
    """

    def _csv_path(self) -> Path:
        return settings.DB_DATA_DIR / "employees.csv"

    def get_all_employees(self) -> list[dict[str, str]]:
        path = self._csv_path()
        logger.info("reading employee CSV path=%s", path)
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        logger.info("loaded %d employee records", len(rows))
        return rows
