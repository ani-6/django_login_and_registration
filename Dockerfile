# Stage 1: Builder with build dependencies
FROM python:3.12-slim as builder

WORKDIR /app

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Stage 2: Final image with runtime dependencies only
FROM python:3.12-slim

WORKDIR /app

# Set Python environment and path
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=base.settings

# Copy virtual environment and application
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app


EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "base.asgi:application"]