# Gunakan image Python
FROM python:3.11

# Set folder kerja di dalam container
WORKDIR /app

# Salin semua file project ke dalam container
COPY . /app

# Upgrade pip dan install dependensi
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Jalankan server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
