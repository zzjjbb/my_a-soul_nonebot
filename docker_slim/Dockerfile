FROM python:3.9 as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN curl -sSL https://install.python-poetry.org -o install-poetry.py && python install-poetry.py --yes \
  && PATH="${PATH}:/root/.local/bin" poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

COPY ./ /app/

RUN rm -rf /usr/share/fonts/ && mv /app/fonts /root/.fonts && fc-cache -fv
RUN pip install --no-cache-dir --upgrade -r requirements.txt && rm requirements.txt \
  && apt-get update && apt-get install -y \
    fontconfig \
    libasound2 libatk-bridge2.0-0 \
	libcups2 \
	libgbm1 \
	libnss3 \
    libwayland-client0 \
	libxkbcommon0 libxrandr2 \
	libxcomposite1 libxdamage1 libxfixes3 \
  && rm -rf /var/lib/apt/lists/*
  
