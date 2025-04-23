#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y \
    python3-dev \
    zlib1g-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev

# Install Python packages
pip install -r requirements.txt 