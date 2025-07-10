FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=index.py

# Expose the port Flask runs on
EXPOSE 5001

# Optional: load .env if used in app.py via python-dotenv
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "wsgi:app"]

