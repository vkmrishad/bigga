FROM node:10.16.3-jessie-slim
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build:ssr
