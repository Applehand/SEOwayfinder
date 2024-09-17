# Use a simple Ubuntu base image
FROM ubuntu:20.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=web:create_app \
    FLASK_RUN_PORT=8081

# Install system dependencies and Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-dev build-essential \
    libnss3 libatk1.0-0 libcups2 libxcomposite1 libxrandr2 libxdamage1 \
    libgbm1 libasound2 libxshmfence1 libpangocairo-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*


# Install Playwright dependencies
RUN pip3 install --upgrade pip && pip3 install playwright pytest-playwright flask lxml pydantic aiohttp requests beautifulsoup4 pyperclip Jinja2

# Install Playwright browsers
RUN python3 -m playwright install

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Expose the Flask app port
EXPOSE 8081

# Command to start the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=8081"]
