#!/bin/bash
# This script is designed for jetson nano install with U20
# It has apt install for npm
# Parse command line arguments
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -v|--venv)
        CREATE_VENV=true
        shift
        ;;
        *)
        shift
        ;;
    esac
done

sudo apt install npm
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../../client
npm install
sudo npm run build
cd ../api
# Install requirements
if [ "$CREATE_VENV" = true ]; then
    # Create and activate virtual environment
    python3 -m venv venv
    source venv/bin/activate
fi

# Install requirements
pip3 install -r requirements.txt

# Deactivate virtual environment
if [ "$CREATE_VENV" = true ]; then
    deactivate
fi