# Use an Ubuntu-based image with Python 3.11 pre-installed
FROM python:3.11-slim-buster

# Set environment variables for Python to ensure output is logged (not buffered)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the Flask app environment variable
ENV FLASK_APP=web:create_app
ENV FLASK_RUN_PORT=8081

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright dependencies
RUN apt-get update && apt-get install -y \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 \
    libgbm1 libasound2 libxshmfence1 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 \
    libcurl4 libharfbuzz0b libx11-xcb1 libxcomposite1 libxrandr2 libxss1 \
    libgtk-3-0 libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install .

# Run Playwright install (from setup.py post-installation)
RUN python -m playwright install

# Expose the port that Flask will run on
EXPOSE 8081

# Command to create tables and run the web server
CMD ["sh", "-c", "python -c 'from spider.storage import create_tables; create_tables()' && flask run --host=0.0.0.0 --port=8081"]
