#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

echo "Downloading NLTK data (punkt)..."
python -m nltk.downloader -d /usr/share/nltk_data punkt

echo "Clearing pip cache..."
pip cache purge

echo "Build complete!"
