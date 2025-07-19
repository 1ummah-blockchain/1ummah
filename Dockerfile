# استخدم صورة Python خفيفة
FROM python:3.11-slim

# تثبيت أدوات البناء ومكتبات النظام اللازمة لـ pycairo و PyGObject
RUN apt-get update && apt-get install -y \
    build-essential gcc libffi-dev libssl-dev \
    libdbus-1-dev libglib2.0-dev pkg-config \
    libcairo2-dev libgirepository1.0-dev python3-gi gir1.2-gtk-3.0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# تحديد مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت الحزم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي المشروع
COPY . .

# فتح المنفذ
EXPOSE 8080

# أمر التشغيل
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
