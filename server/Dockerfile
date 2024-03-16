FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

ENV GNUPGHOME=/app/gnupg

RUN mkdir -p $GNUPGHOME && \
    chmod 700 $GNUPGHOME

RUN if ! gpg --list-keys muclicat@deiteriy.com > /dev/null 2>&1; then \
    echo "Key-Type: RSA\n\
Key-Length: 2048\n\
Subkey-Type: RSA\n\
Subkey-Length: 2048\n\
Name-Real: Multicat Bot\n\
Name-Comment: with passphrase\n\
Name-Email: muclicat@deiteriy.com\n\
Expire-Date: 0\n\
Passphrase: secretpassphrase\n\
%no-protection\n\
%commit" > $GNUPGHOME/gen-key-script && \
    gpg --batch --generate-key $GNUPGHOME/gen-key-script; \
    fi
