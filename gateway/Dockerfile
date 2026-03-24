FROM python:3.14
WORKDIR /app

COPY gateway/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod -R o+rX /usr/local/lib/python3.14/site-packages

COPY shared/ ./shared

COPY gateway/ ./gateway
EXPOSE 8000

RUN useradd gateway
USER gateway

CMD ["uvicorn", "gateway.app.factory:create_app", "--host", "0.0.0.0", "--factory", "--port", "8000"]