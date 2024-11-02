FROM python:3.11-slim-bookworm

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy application code
COPY ./server /app/server

# Make sure uvicorn is installed (as a fallback)
RUN pip install uvicorn

# Command to run the application
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000","--reload"]