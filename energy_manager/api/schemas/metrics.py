import datetime

from pydantic import BaseModel


class MetricValueResponse(BaseModel):
    name: str
    unit: str
    value: float
    measured_at: datetime.datetime
