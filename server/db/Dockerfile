FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8003

CMD ["python", "db_create.py"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]