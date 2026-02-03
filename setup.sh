#!/bin/bash
# Setup script for medical-lay repository

set -e  # Exit on error

echo "🚀 Setting up medical-lay repository..."

# Check if Python 3.11+ is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "📦 Poetry not found. Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    echo "✓ Poetry installed"
else
    echo "✓ Poetry is already installed"
fi

# Install dependencies
echo "📦 Installing dependencies..."
poetry install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys and dataset paths"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating data directories..."
mkdir -p data/TLC_v01
mkdir -p data/WUMLS
mkdir -p data/tlc_json
mkdir -p caches

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "   - Get UMLS API key from: https://uts.nlm.nih.gov/uts/profile"
echo "   - Get DeepL API key from: https://www.deepl.com/pro-api"
echo "2. Obtain and place the required datasets:"
echo "   - TLC-UMLS dataset in data/TLC_v01/"
echo "   - WUMLS dataset in data/WUMLS/"
echo "3. Activate the virtual environment:"
echo "   poetry shell"
echo "4. Run tests to verify setup:"
echo "   pytest tests/"
echo ""
