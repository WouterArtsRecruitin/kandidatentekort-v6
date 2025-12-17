#!/bin/bash
# Setup script for Meta Ads UTM Fix Tool

echo "🚀 Setting up Meta Ads UTM Fix Tool..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Facebook Business SDK
echo "📥 Installing facebook-business SDK..."
pip install facebook-business

# Make the script executable
chmod +x meta_ads_utm_fix.py

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Get your access token from: https://developers.facebook.com/tools/explorer"
echo "2. Run analysis: python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117"
echo "3. Fix ads (dry run): python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117 --fix"
echo "4. Fix ads (live): python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117 --fix --live"