FROM node:24-alpine AS build
WORKDIR /app

COPY dashboard/frontend/package.json ./
COPY dashboard/frontend/package-lock.json ./
RUN npm install

COPY dashboard/frontend/ ./

ARG FRONTEND_ADDRESS=http://localhost
ENV FRONTEND_ADDRESS=${FRONTEND_ADDRESS}

RUN npm run build

FROM nginxinc/nginx-unprivileged:1.28-alpine

COPY dashboard/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
