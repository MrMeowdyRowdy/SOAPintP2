# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install system dependencies for lxml
RUN apt-get update && apt-get install -y \
    libxml2-dev \
    libxslt-dev \
    && apt-get clean

# Install Python dependencies
RUN pip install --no-cache-dir flask flask-sqlalchemy requests spyne lxml

# Expose the application port
EXPOSE 5001

# Set the default command to run the app
CMD ["python", "app.py"]

