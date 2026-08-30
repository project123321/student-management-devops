FROM python:3.10-slim

WORKDIR /app

# Copy requirement definition and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and HTML templates
COPY . .

# Expose port 5000
EXPOSE 5000

# Default environment variable for application version
ENV APP_VERSION="v1.0.0"

# Start the Flask app
CMD ["python", "app.py"]