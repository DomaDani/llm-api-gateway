FROM python:3.14
WORKDIR /app

COPY postgreSQL/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ ./shared
COPY tools/ ./tools

RUN useradd bootstrap
USER bootstrap