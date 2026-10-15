#!/usr/bin/env bash
# Daily routine: re-check every tool URL (dead ones are dropped from tools.json and printed), then rebuild.
set -euo pipefail; cd "$(dirname "$0")"
python3 check_urls.py
python3 build.py
