FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput
EXPOSE 8000

CMD ["gunicorn", "find.wsgi:application", "--bind", "0.0.0.0:8000"]