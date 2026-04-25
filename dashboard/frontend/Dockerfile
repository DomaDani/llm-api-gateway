FROM node:24-alpine AS build
WORKDIR /app

COPY dashboard/frontend/package.json ./
COPY dashboard/frontend/package-lock.json ./
RUN npm install

COPY dashboard/frontend/ ./

ARG FRONTEND_ADDRESS=http://localhost
ARG DASHBOARD_BACKEND_PORT=8080
ENV FRONTEND_ADDRESS=${FRONTEND_ADDRESS}
ENV DASHBOARD_BACKEND_PORT=${DASHBOARD_BACKEND_PORT}

RUN npm run build

FROM nginxinc/nginx-unprivileged:1.28-alpine
ARG DASHBOARD_FRONTEND_PORT=5173
ENV DASHBOARD_FRONTEND_PORT=${DASHBOARD_FRONTEND_PORT}

COPY dashboard/frontend/nginx.conf /etc/nginx/conf.d/default.conf
RUN sed -i "s/listen 5173;/listen ${DASHBOARD_FRONTEND_PORT};/" /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE ${DASHBOARD_FRONTEND_PORT}

CMD ["nginx", "-g", "daemon off;"]
