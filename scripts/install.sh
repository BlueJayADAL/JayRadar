#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../client
npm install
npm run build
cd ../api
pip install -r ./requirements.txt