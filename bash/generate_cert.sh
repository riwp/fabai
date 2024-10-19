#!/bin/bash

# Define the filenames for the key and certificate
KEY_FILE="private.key"
CERT_FILE="certificate.crt"

# Check if the key and certificate already exist
if [[ -f "$KEY_FILE" ]] || [[ -f "$CERT_FILE" ]]; then
    echo "Error: $KEY_FILE or $CERT_FILE already exists. Please remove them or rename them before running this script."
    exit 1
fi

# Generate the self-signed SSL certificate and private key
#openssl req -x509 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -days 365 -nodes
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -subj "/CN=192.168.23.10" -addext "subjectAltName=DNS:pi,IP:192.168.23.10"


# Check if the command succeeded
if [[ $? -eq 0 ]]; then
    echo "Successfully generated $CERT_FILE and $KEY_FILE."
else
    echo "Error: Failed to generate the certificate and key."
    exit 1
fi

