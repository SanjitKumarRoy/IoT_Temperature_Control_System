# Use a lightweight Python image
FROM python:3.8-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY data_service.py .

# Expose port 5001
EXPOSE 5001

# Run the app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "data_service:app"]

