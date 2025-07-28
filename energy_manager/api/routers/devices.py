from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ...db.connection import get_db
from ...db.repository import DeviceRepository
from ...db.repository_errors import UnauthorizedError
from ..schemas.devices import Device, DeviceCreate, DeviceCreateResponse, DeviceUpdate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=DeviceCreateResponse)
def create_device(
    data: DeviceCreate,
    user_id: int = Header(alias="X-User-ID"),
    db: Session = Depends(get_db),
):
    repo = DeviceRepository(db, user_id=user_id)

    try:
        device_id = repo.create_device(data)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    db.commit()  # safer here
    return DeviceCreateResponse(id=device_id)


@router.get("/{device_id}", response_model=Device)
def get_device(
    device_id: int,
    user_id: int = Header(alias="X-User-ID"),
    db: Session = Depends(get_db),
):
    repo = DeviceRepository(db, user_id=user_id)

    try:
        device = repo.get_device(device_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.put("/{device_id}", response_model=Device)
def update_device(
    device_id: int,
    data: DeviceUpdate,
    user_id: int = Header(alias="X-User-ID"),
    db: Session = Depends(get_db),
):
    repo = DeviceRepository(db, user_id=user_id)

    try:
        device = repo.update_device(device_id, data)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    db.commit()
    return device


@router.delete("/{device_id}", response_model=Device)
def delete_device(
    device_id: int,
    user_id: int = Header(alias="X-User-ID"),
    db: Session = Depends(get_db),
):
    repo = DeviceRepository(db, user_id=user_id)

    try:
        device = repo.delete_device(device_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    db.commit()
    return device
