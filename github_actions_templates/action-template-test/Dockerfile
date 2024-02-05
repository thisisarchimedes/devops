FROM ubuntu:20.04

WORKDIR /app

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.sh entrypoint.sh

# Make sure your file has execute permissions
RUN chmod +x entrypoint.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["./entrypoint.sh"]
