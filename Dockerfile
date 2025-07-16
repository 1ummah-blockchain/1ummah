# استخدام صورة Python رسمية خفيفة
FROM python:3.11-slim

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات أولاً
COPY requirements.txt .

# تثبيت الحزم
RUN pip install --no-cache-dir -r requirements.txt

# نسخ بقية ملفات المشروع
COPY . .

# فتح المنفذ 8080 لتشغيل التطبيق
EXPOSE 8080

# أمر التشغيل الافتراضي
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
