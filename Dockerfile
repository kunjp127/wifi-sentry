FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 \
    wireless-tools \
    net-tools \
    iw \
    aircrack-ng \
    tcpdump \
    libpcap-dev \
    pciutils \
    kmod \
    procps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /wifi-sentry

COPY . .

RUN pip install -r requirements.txt

RUN chmod +x run.sh mon-up.sh mon-down.sh

CMD ["bash" , "./run.sh"]
