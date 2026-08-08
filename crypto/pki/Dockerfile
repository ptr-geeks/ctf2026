FROM ubuntu:26.04
WORKDIR /app

RUN apt update && \
    apt install -y python3 socat && \
    rm -rf /var/lib/apt/lists/*

COPY pki.py /app/pki.py
COPY flag.txt /app/flag.txt
CMD ["socat", "-T", "120", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 /app/pki.py"]
