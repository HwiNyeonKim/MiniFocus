# 1. 빌드 단계
FROM node:20-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY .env ./
RUN npm install
COPY . .
RUN npm run build

# 2. 정적 파일 서빙 (nginx)
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
