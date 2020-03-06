FROM python:3.8-alpine

COPY requirements.txt /requirements.txt
COPY gtmetrix-bq.py /app/gtmetrix-bq.py
WORKDIR /app

RUN apk --no-cache add git && \
    pip --no-cache-dir install -r /requirements.txt && \
    apk del git

ENTRYPOINT ["/app/gtmetrix-bq.py"]
