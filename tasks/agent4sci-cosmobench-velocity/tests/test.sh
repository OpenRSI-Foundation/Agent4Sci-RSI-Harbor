#!/bin/bash
set -euo pipefail
cd /workspace
exec /usr/bin/python3 -I /tests/verifier.py
