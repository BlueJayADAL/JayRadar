#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../../client
npm install
npm run build
cd ../../api
python -m venv .venv
source ./.venv/Scripts/Activate.ps1
pip install -r ./requirements.txt