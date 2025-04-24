FROM python:3.10-slim

# Install system dependencies for numpy and pandas
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_APP=app.py 
ENV FLASK_RUN_HOST=0.0.0.0 
ENV FLASK_RUN_PORT=8080 
ENV FLASK_DEBUG=0

CMD ["flask", "run"]