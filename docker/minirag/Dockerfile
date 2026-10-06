FROM astral/uv:0.12.23-python3.10-trixie-slim

WORKDIR /app

ENV PYTHONPATH="/app:/app/src"

RUN apt-get update && apt-get install -y \
    build-essential \
    libavif-dev pkg-config \
    libjpeg-dev \
    gcc unzip zip \
    python3-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .

RUN uv pip install \
    --default-index https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt \
    --system

COPY src ./src

RUN mkdir -p /app/src/models/db_schemas/minirag
COPY docker/minirag/alembic.ini /app/src/models/db_schemas/minirag/alembic.ini

COPY docker/minirag/entrypoints.sh /entrypoints.sh
RUN chmod +x /entrypoints.sh 

ENTRYPOINT [ "/entrypoints.sh" ]

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4" ]