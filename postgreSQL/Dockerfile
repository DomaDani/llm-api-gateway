FROM python:3.14
WORKDIR /app

COPY postgreSQL/requirements.txt ./
RUN apt-get update \
	&& apt-get install -y --no-install-recommends postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R o+rX /usr/local/lib/python3.14/site-packages

COPY shared/ ./shared
COPY tools/ ./tools

RUN useradd bootstrap
USER bootstrap