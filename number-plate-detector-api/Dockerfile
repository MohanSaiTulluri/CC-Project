FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Use Cloud Run port
ENV PORT=8002
EXPOSE 8002

# Let Cloud Run define the port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]