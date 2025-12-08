FROM node:20-alpine AS base
WORKDIR /app

# Install root dev deps
COPY package.json ./
RUN npm install

COPY server/package.json ./server/
COPY client/package.json ./client/

RUN npm --prefix server install
RUN npm --prefix client install

# Build client
COPY client ./client
RUN npm --prefix client run build

# Bundle server
COPY server ./server

EXPOSE 4000 5173

CMD ["node", "server/src/server.js"]
