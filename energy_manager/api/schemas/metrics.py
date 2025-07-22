import datetime

from pydantic import BaseModel


class MetricValueResponse(BaseModel):
    name: str
    unit: str
    value: float
    measured_at: datetime.datetime


class SubscriptionCreate(BaseModel):
    name: str
    description: str | None = None
    metric_ids: list[int]


class SubscriptionCreateResponse(BaseModel):
    id: int
