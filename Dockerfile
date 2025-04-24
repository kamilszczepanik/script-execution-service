FROM debian:bookworm-slim AS nsjail-builder

RUN apt-get update && apt-get install -y \
    bison \
    flex \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /nsjail
RUN git clone https://github.com/google/nsjail.git . && \
    make -j8

FROM python:3.12-slim AS python-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libprotobuf32 \
    libnl-route-3-200 \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /tmp/scripts /sandbox && \
    chmod 1777 /tmp/scripts && \
    chmod 1777 /sandbox

COPY --from=nsjail-builder /nsjail/nsjail /usr/bin/nsjail

COPY --from=python-builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY . .

EXPOSE 8080
ENV PORT=8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app