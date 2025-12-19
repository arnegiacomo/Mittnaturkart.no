FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY VERSION /app/VERSION

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]
