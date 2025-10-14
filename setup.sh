#!/bin/bash
# Quick setup script for local testing

echo "🎙️  Spotify Podcast Chart Tracker - Setup"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Python packages installed"
echo ""

# Install Playwright browsers
echo "🌐 Installing Playwright browser (Chromium)..."
playwright install chromium
echo "✅ Browser installed"
echo ""

echo "================================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Set your API key: export ANTHROPIC_API_KEY='your_key_here'"
echo "2. Run the tracker: python track_ranking.py"
echo ""
echo "Or for GitHub Actions:"
echo "1. Add ANTHROPIC_API_KEY to your repository secrets"
echo "2. Push this repo to GitHub"
echo "3. Enable GitHub Actions"
echo ""
echo "See README.md for detailed instructions."
echo "================================================"

