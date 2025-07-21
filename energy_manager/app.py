from fastapi import FastAPI, Header, HTTPException
from sqlalchemy.orm import Session

from .db.connection import create_db, get_db_session
from .db.repositories import Repository, UnauthorizedError
from .logs import get_logger
from .settings import DB_CONN, IS_LOCAL


# API object
def create_app(db_session: Session, is_debug: bool):
    # Define working objects
    logger = get_logger("app", is_debug=is_debug)
    app = FastAPI(
        title="Energy manager",
        description="System for managing electricity grid",
        version="0.1.0",
        debug=is_debug,
    )
    logger.debug("FastAPI app created")

    # API routes
    @app.get("/sites")
    def get_sites(user_id: int = Header(alias="X-User-ID")):
        repo = Repository(db_session, user_id)
        return repo.get_sites()

    @app.get("/site/{site_id}")
    def get_site(site_id: int, user_id: int = Header(alias="X-User-ID")):
        repo = Repository(db_session, user_id)
        try:
            return repo.get_site(site_id)
        except UnauthorizedError as e:
            raise HTTPException(status_code=403, detail=str(e)) from e

    return app


if __name__ == "__main__":
    is_debug = IS_LOCAL
    create_db(DB_CONN)
    db_session = get_db_session(DB_CONN)
    app = create_app(db_session=db_session, is_debug=is_debug)
