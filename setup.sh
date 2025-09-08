#!/bin/bash

# Mumble UxPlay Bot Setup Script
# This script automatically downloads and sets up the Mumble UxPlay Bot

set -e

REPO_URL="https://github.com/GameOneDev/mumble-uxplay-bot.git"
REPO_NAME="mumble-uxplay-bot"

echo "=== Mumble UxPlay Bot Setup ==="
echo

# Check if running as root for system packages
if [[ $EUID -eq 0 ]]; then
    echo "Please do not run this script as root. It will use sudo when needed."
    exit 1
fi

# Check if we're already in the repository directory
if [[ -f "main.py" && -f "requirements.txt" && -f "setup.sh" ]]; then
    echo "Already in repository directory. Continuing with setup..."
else
    echo "Downloading Mumble UxPlay Bot repository..."
    if [[ -d "$REPO_NAME" ]]; then
        echo "Repository directory already exists. Pulling latest changes..."
        cd "$REPO_NAME"
        git pull
    else
        git clone "$REPO_URL"
        cd "$REPO_NAME"
    fi
fi

echo "Repository ready. Continuing with setup..."
echo


echo "Updating package list..."
sudo apt update


echo "Installing system dependencies..."
sudo apt install -y alsa-utils python3-venv python3-pip git curl


echo "Setting up Python environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo
echo "=== Setup Complete! ==="
echo
echo "Repository downloaded to: $(pwd)"
echo
echo "IMPORTANT: You need to install UxPlay separately before running the bot."
echo
echo "To use the bot:"
echo "1. Edit main.py with your Mumble server details"
echo "2. Run: python main.py"
echo "3. Connect your Apple device to AirPlay"
echo
echo "Enjoy streaming music from your Apple device to Mumble!"
