#!/usr/bin/env python3
"""
Test Render API authentication with detailed debugging
"""

import requests
import json

# Test the API key
RENDER_API_KEY = "rnd_vGJvIxrJzJO1k3JlHSU7clSOIZv"

print("🔍 Testing Render API authentication...\n")

# Test 1: Basic API test
print("Test 1: Basic API connection")
print(f"API Key: {RENDER_API_KEY[:10]}...{RENDER_API_KEY[-4:]}")
print(f"Full Key Length: {len(RENDER_API_KEY)} characters\n")

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

# Try different endpoints
endpoints = [
    "/v1/services",
    "/v1/owners",
    "/v1/regions"
]

for endpoint in endpoints:
    print(f"\n📍 Testing endpoint: {endpoint}")
    try:
        response = requests.get(
            f"https://api.render.com{endpoint}",
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers.get('X-Request-Id', 'N/A')}")
        
        if response.status_code == 200:
            print("✅ Success!")
            data = response.json()
            if isinstance(data, list):
                print(f"Response contains {len(data)} items")
            else:
                print(f"Response type: {type(data)}")
        elif response.status_code == 401:
            print("❌ Unauthorized - Invalid API key")
            print(f"Response: {response.text}")
        else:
            print(f"⚠️ Unexpected status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

# Test 2: Try without Bearer prefix
print("\n\nTest 2: Testing without Bearer prefix")
headers_alt = {
    "Accept": "application/json",
    "Authorization": RENDER_API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.render.com/v1/services",
    headers=headers_alt
)
print(f"Status Code: {response.status_code}")

# Test 3: Try as API-Key header
print("\n\nTest 3: Testing as API-Key header")
headers_api = {
    "Accept": "application/json",
    "API-Key": RENDER_API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(
    "https://api.render.com/v1/services",
    headers=headers_api
)
print(f"Status Code: {response.status_code}")

print("\n\n📝 Summary:")
print("If all tests return 401, you need a new API key from:")
print("https://dashboard.render.com/account/api-keys")
print("\nMake sure to:")
print("1. Sign in to Render")
print("2. Go to Account Settings → API Keys")
print("3. Click 'Create API Key'")
print("4. Copy the FULL key (it's only shown once!)")