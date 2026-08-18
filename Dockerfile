FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for MCP
RUN apt-get update && apt-get install -y curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install npx and mcp-grafana globally
RUN npm install -g @grafana/mcp-grafana

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install Flask gunicorn

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120", "app:app"]
