#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../ client
npm run dev
cd ../api
python ./main.py