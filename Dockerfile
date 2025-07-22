# Use small base image with python installed
FROM python:3.13-slim-bullseye

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:0.8.0 /uv /uvx /bin/

# Update system packages and install init system
RUN \
    apt-get update &&\
    apt-get install -y --no-install-recommends tini

# Create dir for app and switch to it
WORKDIR /app

# Install dependencies first (for docker layer caching)
COPY uv.lock pyproject.toml ./
RUN uv sync --no-install-project

# Add source code
COPY . .

# Install again with my code as package (for absolute imports)
RUN uv sync

# Documents that the container listens on port 8000 
EXPOSE 8000 

# Avoid root access (not working for uv)
# USER nobody

# Init system: signal forwarding for graceful shutdowns, zombie process reaping
ENTRYPOINT [ "tini", "--" ]
