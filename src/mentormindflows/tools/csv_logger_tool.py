import csv
import os
from typing import Optional, Type

from pydantic import BaseModel, PrivateAttr
from crewai.tools import BaseTool


class CSVLoggerInput(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    location: Optional[str] = None
    category_incident: Optional[str] = None
    time: Optional[str] = None
    severity: Optional[str] = None
    issue_msg: Optional[str] = None


class CSVLoggerTool(BaseTool):
    name: str = "CSVLoggerTool"
    description: str = "Logs incident details to a CSV file in outputs."
    args_schema: Type[BaseModel] = CSVLoggerInput
    _file_path: str = PrivateAttr()

    def __init__(self, filename: str = "fire_incidents_log.csv"):
        super().__init__()
        self._file_path = os.path.join(os.path.dirname(__file__), "..", "outputs", filename)
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)

    def _run(self, **kwargs) -> str:
        fieldnames = [
            "id",
            "username",
            "location",
            "category_incident",
            "time",
            "severity",
            "issue_msg",
        ]

        row = {key: kwargs.get(key, "") for key in fieldnames}

        file_exists = os.path.isfile(self._file_path)

        with open(self._file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)

        return f"Incident logged to {self._file_path}"
