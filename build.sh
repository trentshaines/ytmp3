#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg using the system package manager
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    apt-get update
    apt-get install -y ffmpeg
elif [ -f /etc/redhat-release ]; then
    # RHEL/CentOS
    yum install -y ffmpeg
else
    # For other systems, try to use the package manager
    if command -v apk &> /dev/null; then
        apk add --no-cache ffmpeg
    elif command -v brew &> /dev/null; then
        brew install ffmpeg
    else
        echo "Could not install FFmpeg automatically. Please install it manually."
        exit 1
    fi
fi 