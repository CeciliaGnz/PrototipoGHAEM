FROM python:3.12-slim
 
WORKDIR /app
 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
COPY . .
 
EXPOSE 8000
 
# Recolecta archivos estáticos (opcional, solo si usas staticfiles)
RUN python manage.py collectstatic --noinput || true
 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]