FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a .env file if one doesn't exist (will be overridden by mounted volume in prod)
RUN touch .env

# Expose the port
EXPOSE 8002

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"] 