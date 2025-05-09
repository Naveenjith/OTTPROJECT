# Use official Python base image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies for MySQL and others
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    netcat-openbsd \
    pkg-config \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ Just to make sure gunicorn is installed
RUN pip install gunicorn

# Copy project files into container
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start Gunicorn server
#CMD ["gunicorn", "OTTPROJECT.wsgi:application", "--bind", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
