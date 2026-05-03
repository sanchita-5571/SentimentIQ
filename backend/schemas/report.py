from datetime import datetime

from pydantic import BaseModel


class ReportExportRequest(BaseModel):
    format: str = "csv"
    search: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    source: str | None = None
    category: str | None = None
    sentiment_label: str | None = None
    language: str | None = None
    product: str | None = None
