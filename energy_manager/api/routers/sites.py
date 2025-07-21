from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from ...db.connection import get_db
from ...db.repositories import Repository, UnauthorizedError

router = APIRouter(prefix="/sites", tags=["devices"])


@router.get("/")
def get_sites(user_id: int = Header(alias="X-User-ID"), db: Session = Depends(get_db)):
    repo = Repository(db, user_id)
    return repo.get_sites()


@router.get("/{site_id}")
def get_site(
    site_id: int,
    user_id: int = Header(alias="X-User-ID"),
    db: Session = Depends(get_db),
):
    repo = Repository(db, user_id)
    try:
        return repo.get_site(site_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
