FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
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
    && apt-get clean

WORKDIR /wifi-sentry
COPY . /wifi-sentry

RUN pip3 install -r requirements.txt

RUN chmod +x run.sh mon-up.sh mon-down.sh

CMD ["bash"]