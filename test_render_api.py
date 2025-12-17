#!/usr/bin/env python3
"""
Test Render API connectivity
"""

import requests

# Test the API key
RENDER_API_KEY = "rnd_vGJvIxrJzJO1k3JlHSU7clSOIZv"

print("🔍 Testing Render API connection...")

# Test basic API access
response = requests.get(
    "https://api.render.com/v1/services",
    headers={
        "Accept": "application/json",
        "Authorization": f"Bearer {RENDER_API_KEY}"
    }
)

print(f"Status Code: {response.status_code}")
print(f"Headers: {dict(response.headers)}")

if response.status_code == 200:
    print("✅ API Key is valid!")
    services = response.json()
    print(f"Found {len(services)} existing services")
elif response.status_code == 401:
    print("❌ API Key is invalid or expired")
    print("Please get a new API key from: https://dashboard.render.com/account/api-keys")
else:
    print(f"❌ Unexpected error: {response.status_code}")
    print(response.text)