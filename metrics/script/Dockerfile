# Use an official Python runtime as a parent image
FROM python:3.12

# Install git. The python image is based on Debian, so use apt-get to install packages.
RUN apt-get update && apt-get install -y git

# Set the working directory in the container to /app
WORKDIR /app

# Clone the specific git repository
RUN git clone https://github.com/thisisarchimedes/devops.git

COPY requirements.txt /app/
COPY .env /app/

COPY script/entry_point.sh /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install awscli

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
#CMD ["gunicorn", "-b", "0.0.0.0:8000", "src.event_processor.entry_flask:app"]
ENTRYPOINT ["/app/entry_point.sh"]