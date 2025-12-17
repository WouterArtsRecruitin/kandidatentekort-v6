#!/usr/bin/env python3
"""
Check Netlify site configuration and environment variables
"""

import requests
import json

# Netlify sites
SITE_IDS = {
    'kandidatentekort': '3c89912a-f1be-4c6c-ba73-03ba7fdc8dc7',
    'ab_test': '9a753352-210d-4a12-934f-48bd5e0ed3ed'
}

def check_site_status(site_url):
    """Check what version is deployed"""
    print(f"\n🌐 Checking {site_url}")
    
    try:
        response = requests.get(site_url)
        
        # Check for specific markers
        if 'Gratis Analyse' in response.text:
            print("✅ Shows 'Gratis Analyse' button")
        else:
            print("❌ Missing 'Gratis Analyse' button")
            
        # Check pixel IDs
        if '517991158551582' in response.text:
            print("❌ Contains WRONG pixel: 517991158551582")
        if '238226887541404' in response.text:
            print("✅ Contains CORRECT pixel: 238226887541404")
            
        # Check for design elements
        if 'assessment-form' in response.text:
            print("📋 Has assessment form")
        if 'hero-section' in response.text:
            print("🏠 Has hero section")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def main():
    print("🔍 KANDIDATENTEKORT.NL SITE STATUS CHECK")
    print("=" * 60)
    
    # Check main domain
    check_site_status("https://kandidatentekort.nl")
    
    # Check Netlify domain
    print("\n📍 Checking Netlify direct URL:")
    check_site_status("https://kandidatentekort.netlify.app")
    
    print("\n\n💡 PIXEL FIX NEEDED:")
    print("1. Remove pixel ID: 517991158551582")
    print("2. Keep only pixel ID: 238226887541404")
    print("\n📁 Check these files:")
    print("- index.html")
    print("- _app.tsx or _app.js") 
    print("- Any analytics config files")
    print("- Netlify environment variables")

if __name__ == "__main__":
    main()