FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=10000

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Flask tylko do prostego healthcheck / HTTP endpointu dla Rendera
RUN pip install --no-cache-dir flask

# Jeśli repo ma requirements.txt, odkomentuj:
# RUN pip install --no-cache-dir -r requirements.txt

COPY render/health_server.py /app/render/health_server.py

EXPOSE 10000

CMD ["python", "/app/render/health_server.py"]
