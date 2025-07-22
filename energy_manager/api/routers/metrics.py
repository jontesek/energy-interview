from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...db.connection import get_db
from ...db.repositories import EntityNotFoundError, Repository
from ..schemas.metrics import MetricValueResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/{metric_id}/latest-value", response_model=MetricValueResponse | None)
def get_latest_metric_value(metric_id: int, db: Session = Depends(get_db)):
    repo = Repository(db, user_id=0)

    try:
        metric_value = repo.get_latest_metric_value(metric_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

    return metric_value
