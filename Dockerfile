FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        mupdf \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py download_and_convert.py entrypoint.sh ./
COPY templates/ templates/
COPY manifest.json sw.js icon.svg ./

RUN chmod +x entrypoint.sh && mkdir -p img

EXPOSE 5023

ENTRYPOINT ["./entrypoint.sh"]
