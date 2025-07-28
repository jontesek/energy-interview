import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, model_validator


class DeviceCreate(BaseModel):
    site_id: int
    name: str
    description: str | None = None


class DeviceUpdate(BaseModel):
    site_id: int | None = None
    name: str | None = None
    description: str | None = None

    @model_validator(mode="after")
    def at_least_one_field_required(self) -> Self:
        # Dynamically get all field names
        field_names = self.__annotations__.keys()

        # Check if all fields are None
        if all(getattr(self, field) is None for field in field_names):
            raise ValueError("At least one field must be provided.")

        return self


class DeviceCreateResponse(BaseModel):
    id: int


class Device(DeviceCreate):
    id: int
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)
