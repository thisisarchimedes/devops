FROM ubuntu:20.04

WORKDIR /app

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entry_point.sh entry_point.sh

# Make sure your file has execute permissions
RUN chmod +x entry_point.sh

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["./entry_point.sh"]
