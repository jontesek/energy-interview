from fastapi import FastAPI

from .api.routers import devices, metrics, sites
from .db.connection import create_db
from .logs import get_logger
from .settings import DB_CONN, IS_LOCAL

# Make sure DB exists (add drop_first for cleanup)
create_db(db_conn=DB_CONN)

# Setup app
is_debug = IS_LOCAL
logger = get_logger("app", is_debug=is_debug)
app = FastAPI(
    title="Energy manager",
    description="System for managing electricity grid",
    version="0.1.0",
    debug=is_debug,
)
logger.debug("FastAPI app created")

# Add API routes
app.include_router(sites.router)
app.include_router(devices.router)
app.include_router(metrics.router)

logger.debug("FastAPI routers added")

# For local debugging
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
