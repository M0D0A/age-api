FROM python:3.11-slim

# ENV HTTP_PROXY="http://10.0.20.6:80"
# ENV HTTPS_PROXY="http://10.0.20.6:80"
ENV NO_PROXY="localhost,127.0.0.1"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY  requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "age_api:app", "--host", "0.0.0.0", "--port", "8000"]
