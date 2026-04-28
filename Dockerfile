FROM python:3.11-slim

# System dependencies for PDF parsing and local builds
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt pyproject.toml README.md LICENSE ./

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .

RUN python -m pip install -e .

CMD ["tail", "-f", "/dev/null"]
