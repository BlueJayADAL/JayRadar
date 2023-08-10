#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../ client
npm run dev
cd ../api
source ./.venv/bin/activate
python ./main.py