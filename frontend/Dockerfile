FROM node:20-slim

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

WORKDIR /app

COPY package.json pnpm-lock.yaml ./

RUN pnpm install --frozen-lockfile

COPY . .

ARG NUXT_BACKEND_API_BASE="http://backend:5000"
ENV NUXT_BACKEND_API_BASE=$NUXT_BACKEND_API_BASE

RUN pnpm run build

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
