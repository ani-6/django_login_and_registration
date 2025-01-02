# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the application code
COPY . /app/

# Run collectstatic and copy files to /app/static
RUN python3 manage.py collectstatic --noinput

# Set appropriate permissions on the static files
RUN chmod -R 755 /app/static

# Expose Django's default port
EXPOSE 8000

# Command to run Django app
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "base.wsgi:application"]
