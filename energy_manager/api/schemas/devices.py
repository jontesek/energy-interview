import datetime

from pydantic import BaseModel, ConfigDict


class DeviceCreate(BaseModel):
    site_id: int
    name: str
    description: str | None = None


class DeviceUpdate(BaseModel):
    site_id: int | None = None
    name: str | None = None
    description: str | None = None


class DeviceCreateResponse(BaseModel):
    id: int


class Device(DeviceCreate):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
