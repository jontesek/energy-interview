import os

# Database
DB_CONN = os.getenv("DB_CONN", "sqlite:///energy.db")
ECHO_SQL = os.getenv("ECHO_SQL", 0)
# Runtime
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
# Helpers
IS_LOCAL = ENVIRONMENT == "local"
