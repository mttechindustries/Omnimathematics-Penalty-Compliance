#!/bin/bash
# Script to install dependencies and generate commit images for the Omnimathematics Penalty Framework

echo "Setting up environment for commit image generation..."

# Install required Python packages
pip install matplotlib numpy

echo "Generating commit images..."
python scripts/generate_commit_images.py

echo "Commit images have been generated in the commit_images/ directory."
echo "View the README.md file in that directory for information about each visualization."