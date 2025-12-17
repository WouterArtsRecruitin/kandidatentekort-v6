#!/bin/bash

# Deploy old design with correct pixel to Netlify
echo "🚀 Deploying kandidatentekort.nl old design with fixed pixel..."

# Navigate to project directory
cd /Users/wouterarts/projects/kandidatentekort-automation/kandidatentekort-automation

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found in current directory"
    exit 1
fi

# Verify pixel is correct
echo "✅ Checking pixel ID..."
if grep -q "238226887541404" index.html; then
    echo "✅ Correct pixel ID found: 238226887541404"
else
    echo "❌ Pixel ID not correct!"
    exit 1
fi

# Create a temporary git repo for deployment
echo "📦 Preparing for deployment..."
git init
git add .
git commit -m "Deploy old design with fixed pixel ID 238226887541404"

# Deploy to Netlify
echo "🌐 Deploying to Netlify..."
echo ""
echo "MANUAL STEPS REQUIRED:"
echo "====================="
echo "1. Go to: https://app.netlify.com/sites/kandidatentekort/deploys"
echo "2. Drag and drop this folder: /Users/wouterarts/projects/kandidatentekort-automation/kandidatentekort-automation"
echo "3. Or use Netlify CLI: netlify deploy --prod --dir=."
echo ""
echo "ENVIRONMENT VARIABLES TO SET:"
echo "============================="
echo "FACEBOOK_PIXEL_ID=238226887541404"
echo "REACT_APP_FB_PIXEL_ID=238226887541404"
echo "NEXT_PUBLIC_FB_PIXEL_ID=238226887541404"
echo ""
echo "✅ Files are ready for deployment!"