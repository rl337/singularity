# Use an official Node runtime as a parent image
FROM node:current-alpine

ARG PROJECT_DIR
ARG CONFIG_DIR

RUN apk update && apk add util-linux

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /usr/src/app
COPY ${PROJECT_DIR} /app
COPY ${CONFIG_DIR} /app/config

# Install any needed packages specified in package.json
RUN npm install

# build the Parcel dist
RUN npm run build

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.js when the container launches
CMD ["node", "app.js"]

