FROM python:3.14
WORKDIR /app

RUN useradd -m dashboard-backend
ENV PATH="/home/dashboard-backend/.local/bin:${PATH}"

COPY dashboard/backend/requirements.txt ./
USER dashboard-backend

RUN python -m pip install --no-cache-dir --user -r requirements.txt

COPY --chown=dashboard-backend:dashboard-backend shared/ ./shared

COPY --chown=dashboard-backend:dashboard-backend dashboard/backend/ ./dashboard/backend
EXPOSE 8081

CMD ["uvicorn", "dashboard.backend.app.factory:create_app", "--host", "0.0.0.0", "--factory", "--port", "8081"]