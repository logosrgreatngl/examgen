#!/usr/bin/env bash
set -o errexit

# Install wkhtmltopdf
apt-get update && apt-get install -y wkhtmltopdf

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
