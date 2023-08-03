# FROM node:lts

# # make the 'app' folder the current working directory
# WORKDIR /app

# # copy both 'package.json' and 'package-lock.json' (if available)
# COPY package.json ./

# # install project dependencies
# RUN npm install

# # copy project files and folders to the current working directory (i.e. 'app' folder)
# COPY . .

# EXPOSE 8080
# CMD ["npm", "run", "dev"]

FROM node:lts as develop-stage
WORKDIR /app
COPY package*.json ./
RUN yarn install
COPY . .
# build stage
FROM develop-stage as build-stage
RUN yarn build
# production stage
FROM nginx:1.15.7-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]