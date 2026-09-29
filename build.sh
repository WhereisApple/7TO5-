#!/bin/bash
set -e

# Upgrade pip first
python -m pip install --upgrade pip

# Install with --prefer-binary to avoid Rust builds
pip install --prefer-binary -r requirements.txt

# Verify imports work
python -c "import fastapi; import uvicorn; import jinja2; import pydantic; print('✓ All deps OK')"
