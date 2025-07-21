from fastapi import FastAPI, Header, HTTPException

from .db.connection import get_db_session
from .db.repositories import Repository, UnauthorizedError
from .logs import get_logger
from .settings import DB_CONN, IS_LOCAL


# API object
def create_app(is_debug):
    app = FastAPI(
        title="Energy manager",
        description="System for managing electricity grid",
        version="0.1.0",
        debug=is_debug,
    )

    return app


# Main objects
is_debug = IS_LOCAL
app = create_app(is_debug=is_debug)
db_session = get_db_session(DB_CONN)
logger = get_logger("app", is_debug=is_debug)


# API routes
@app.get("/sites")
def get_sites(user_id: int = Header(alias="X-User-ID")):
    repo = Repository(db_session, user_id)
    return repo.get_sites()


@app.get("/site/{site_id}")
def get_site(site_id: int, user_id: int = Header(alias="X-User-ID")):
    repo = Repository(db_session, user_id)
    try:
        site = repo.get_site(site_id)
    except UnauthorizedError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    return site
