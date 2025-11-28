# Base Image python 3.12
FROM python:3.12-slim

# Copy uv from astral-sh/uv and install inside the container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and uv.lock files to the working directory
COPY pyproject.toml . uv.lock ./

# Install the dependencies without dev dependencies
RUN uv sync --frozen --no-dev

# Copy the source code to the working directory
COPY src/ ./src/

# Expose the FASTAPI port 8001
EXPOSE 8001

# Run the application
CMD ["uv", "run", "uvicorn", "notification_producer_api.main:app", "--host", "0.0.0.0", "--port", "8001"]