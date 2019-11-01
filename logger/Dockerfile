FROM node:10.13-alpine

WORKDIR /app

COPY ["package.json", "yarn.lock*", "./"]
RUN yarn --pure-lockfile && mv node_modules ../

COPY . .

CMD yarn start

EXPOSE 3000
