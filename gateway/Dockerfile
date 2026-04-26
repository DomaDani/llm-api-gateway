FROM python:3.14
WORKDIR /app

RUN useradd -m gateway
ENV PATH="/home/gateway/.local/bin:${PATH}"

COPY gateway/requirements.txt ./
USER gateway

RUN python -m pip install --no-cache-dir --user -r requirements.txt

COPY --chown=gateway:gateway shared/ ./shared

COPY --chown=gateway:gateway gateway/ ./gateway
EXPOSE 8000

CMD ["sh", "-c", "uvicorn gateway.app.factory:create_app --host 0.0.0.0 --factory --port ${GATEWAY_PORT:-8000}"]