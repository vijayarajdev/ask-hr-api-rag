# Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

# Set working directory
WORKDIR /code

# Install system dependencies (needed for some vector DBs/PDF parsers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./app /code/app

# Copy the pre-built databases and policies
COPY ./data /code/data

# Create a non-root user for security and grant ownership of the directory
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /code
USER appuser

# Expose the FastAPI port (matches image_f09a06.png)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]