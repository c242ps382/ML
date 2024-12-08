# Gunakan image Python sebagai base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin semua file ke container
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
