import os

# Database
DB_CONN = "sqlite:///energy.db"
# Runtime
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
# Helpers
IS_LOCAL = ENVIRONMENT == "local"
