#!/usr/bin/env bash
# Build script for Render.com deployment

set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Build completed successfully!"
