FROM python:3.9-alpine as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN wget https://install.python-poetry.org -O install-poetry.py && python install-poetry.py --yes \
  && PATH="${PATH}:/root/.local/bin" poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

COPY fonts /root/.fonts

RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm requirements.txt \
  && apt-get update && apt-get install -y \
    fontconfig \
    libasound2 libatk-bridge2.0-0 \
	libcairo2 libcups2 \
	libgbm1 \
	libnss3 \
	libpango-1.0-0 \
    libwayland-client0 \
	libxkbcommon0 libxrandr2 \
	libxcomposite1 libxdamage1 libxfixes3 \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/fonts/ && fc-cache -fv
  
COPY src /app/
