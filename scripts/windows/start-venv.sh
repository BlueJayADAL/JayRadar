#!/bin/bash
cd "$(dirname "${BASH_SOURCE[0]}")"
cd ../../api
source ./.venv/Scripts/Activate.ps1
python ./main.py