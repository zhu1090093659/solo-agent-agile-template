# Frontend Dockerfile - React with Bun
FROM oven/bun:1 as base

WORKDIR /app

# Install dependencies
COPY package.json bun.lockb* ./
RUN bun install --frozen-lockfile

# Copy application code
COPY . .

# Development stage
FROM base as dev
EXPOSE 3000
CMD ["bun", "run", "dev", "--host"]

# Build stage
FROM base as build
RUN bun run build

# Production stage with nginx
FROM nginx:alpine as prod
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
