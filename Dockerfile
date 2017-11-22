# Pull base image
FROM resin/rpi-raspbian:wheezy

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-virtualenv \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt

RUN git clone https://github.com/Brian--/CompileBot

WORKDIR CompileBot

RUN pip3 install -r requirements.txt

# Define working directory
WORKDIR /data

# Define default command
CMD ["python -m disco.cli --config config.yaml"]

