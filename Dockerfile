# Gunakan base image Python
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Salin file ke container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Command untuk menjalankan aplikasi
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
