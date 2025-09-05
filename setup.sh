#!/bin/bash

# Enhanced RL Controlled Agent Setup Script
echo "🤖 Setting up Enhanced RL Controlled Agent..."
echo "================================================"

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data
echo "✅ Data directory created"

# Run demo to verify installation
echo ""
echo "🧪 Running system verification..."
python3 demo.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "🚀 Ready to use! Choose your interface:"
    echo "  • CLI Mode: python3 -m agent.main"
    echo "  • Web Mode: streamlit run streamlit_app.py"
    echo ""
    echo "📚 Documentation:"
    echo "  • README.md - User guide"
    echo "  • TECHNICAL_REPORT.md - Technical details"
else
    echo "❌ Setup verification failed"
    exit 1
fi