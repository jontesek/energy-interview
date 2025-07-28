import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ...db.connection import get_db
from ...db.repository import MetricRepository
from ...db.repository_errors import EntityNotFoundError
from ..schemas.metrics import (
    MetricValueResponse,
    SubscriptionCreate,
    SubscriptionCreateResponse,
)

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/{metric_id}/latest-value", response_model=MetricValueResponse | None)
def get_latest_metric_value(metric_id: int, db: Session = Depends(get_db)):
    repo = MetricRepository(db)

    try:
        metric_value = repo.get_latest_metric_value(metric_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return metric_value


@router.post("/subscriptions", response_model=SubscriptionCreateResponse)
def create_subscription(
    payload: SubscriptionCreate,
    user_id: int = Header(alias="X-User-ID"),
    db: Session = Depends(get_db),
):
    repo = MetricRepository(db)

    try:
        response = repo.create_subscription(payload, user_id)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=404, detail="Some metric(s) you provided don't exist in DB."
        ) from e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    db.commit()
    return response


@router.get("/{metric_id}/history", response_model=list[float])
def get_metric_history(
    metric_id: int,
    start_dt: datetime.datetime,
    end_dt: datetime.datetime,
    db: Session = Depends(get_db),
):
    repo = MetricRepository(db)

    try:
        metric_values = repo.get_metric_history(metric_id, start_dt, end_dt)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return metric_values
