FROM python:3.10-slim

WORKDIR /app
# Force rebuild to include patient data - 2025-10-25

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY . .

# Expose port (Railway sets this via $PORT)
EXPOSE ${PORT:-5050}

# Run application - use shell form to allow PORT variable substitution
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-5050} --workers 4
