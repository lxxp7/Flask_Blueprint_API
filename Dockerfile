# Dockerfile for FlaskAPI (Flask + Waitress)
FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port (default Flask port, can be changed)
EXPOSE 5000

# Entrypoint: serves the app with Waitress
CMD ["python", "app.py"]
