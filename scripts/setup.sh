#!/bin/bash
# GiftOS Core Development Setup Script

set -e

echo "=== GiftOS Core Setup ==="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install in development mode
echo "Installing GiftOS Core..."
pip install -e ".[dev]"

# Setup pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install || true

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env from example..."
    cp .env.example .env
    echo "Please edit .env with your credentials"
fi

echo ""
echo "=== Setup Complete ==="
echo "Activate environment: source venv/bin/activate"
echo "Run tests: pytest"
echo "Start server: uvicorn giftos.main:app --reload"
echo "Run with Docker: docker-compose up --build"
