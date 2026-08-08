FROM ubuntu:26.04
WORKDIR /app

RUN apt update && \
    apt install -y python3 socat && \
    rm -rf /var/lib/apt/lists/*

COPY main /app
COPY flag.txt /app/flag.txt
CMD ["socat", "-T", "10", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/app/main"]
