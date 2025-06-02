# Gunakan base image Python 3.9
FROM python:3.9-slim

# Set folder kerja di dalam container
WORKDIR /code

# Salin file requirements terlebih dahulu
COPY ./requirements.txt /code/requirements.txt

# Install semua library yang dibutuhkan
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Salin semua file proyekmu ke dalam container
# Pastikan semua file yang dibutuhkan (main.py, digitalBase.txt, folder db)
# berada di level yang sama dengan Dockerfile ini saat proses build.
COPY . /code/

# (Opsional tapi direkomendasikan jika menggunakan path seperti /data/db untuk Chroma)
# Jika Anda memutuskan untuk menggunakan path /data/db untuk persistensi ChromaDB di platform tertentu,
# baris ini akan membuat direktori tersebut dan mengatur izinnya.
# Jika ChromaDB Anda disimpan relatif terhadap /code (misalnya di /code/db), baris ini tidak terlalu kritikal.
#mkdir -p /data/db && chown -R 1000:1000 /data

# Buka port 8000 agar bisa diakses
EXPOSE 8000

# Perintah untuk menjalankan server saat container dimulai
# Pastikan 'main:app' sesuai dengan nama file Python utama Anda (main.py)
# dan nama objek FastAPI di dalamnya (app = FastAPI()).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
