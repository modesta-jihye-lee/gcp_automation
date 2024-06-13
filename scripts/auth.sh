#!/bin/bash

TARGET_PATH="/app/scripts/google-cloud-sdk"

if [ -f "$TARGET_PATH" ]; then
    echo "google-cloud-cli already installed!"
else
    echo "download google-cloud-cli..."
    # https://cloud.google.com/sdk/docs/install?hl=ko#linux
    curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-478.0.0-linux-x86_64.tar.gz
    tar -xf google-cloud-cli-478.0.0-linux-x86_64.tar.gz
    rm google-cloud-cli-478.0.0-linux-x86_64.tar.gz
    ./google-cloud-sdk/install.sh
    source /root/.bashrc
fi

gcloud init
gcloud auth application-default login