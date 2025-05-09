FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Optional: load .env if used in app.py via python-dotenv
CMD ["flask", "run", "--host=0.0.0.0"]
