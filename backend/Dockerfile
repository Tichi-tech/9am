FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5050

# Run application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5050", "--workers", "4"]
