FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    p7zip-full \
    clinfo \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN wget -O hashcat.7z https://github.com/hashcat/hashcat/releases/download/v6.2.6/hashcat-6.2.6.7z \
    && 7z x hashcat.7z -o/usr/local/bin/ \
    && rm hashcat.7z \
    && chmod +x /usr/local/bin/hashcat-6.2.6/hashcat.bin

ENV PATH="/usr/local/bin/hashcat-6.2.6:${PATH}"

COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
