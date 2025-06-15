FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir Django djangorestframework django-cors-headers neo4j
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
