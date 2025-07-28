FROM python:3.13-slim-bullseye

COPY --from=ghcr.io/astral-sh/uv:0.8.0 /uv /uvx /bin/

RUN \
    apt-get update &&\
    apt-get install -y --no-install-recommends tini

WORKDIR /app

# Install dependencies first (for docker layer caching)
COPY uv.lock pyproject.toml ./
RUN uv sync --no-install-project

COPY . .

# Install again with my code as package (for absolute imports)
RUN uv sync

EXPOSE 8000 

# Avoid root access (not working for uv)
# USER nobody

# Init system: signal forwarding for graceful shutdowns, zombie process reaping
ENTRYPOINT [ "tini", "--" ]
