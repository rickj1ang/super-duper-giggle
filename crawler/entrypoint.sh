#!/bin/sh
set -e

echo "[entrypoint] Starting crawler at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
python -m src.crawler


