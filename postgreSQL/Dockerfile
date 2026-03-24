FROM python:3.14
WORKDIR /app

RUN useradd -m bootstrap
ENV PATH="/home/bootstrap/.local/bin:${PATH}"

COPY postgreSQL/requirements.txt ./
RUN apt-get update \
	&& apt-get install -y --no-install-recommends postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

USER bootstrap

RUN python -m pip install --no-cache-dir --user -r requirements.txt

COPY --chown=bootstrap:bootstrap shared/ ./shared
COPY --chown=bootstrap:bootstrap tools/ ./tools