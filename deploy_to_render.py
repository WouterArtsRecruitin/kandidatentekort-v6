#!/usr/bin/env python3
"""
Automated Render deployment script for kandidatentekort-v6
"""

import requests
import json
import time
import sys

# Render API configuration
RENDER_API_KEY = "rnd_vGJvIxrJzJO1k3JlHSU7clSOIZv"
API_BASE_URL = "https://api.render.com/v1"

headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {RENDER_API_KEY}",
    "Content-Type": "application/json"
}

print("🚀 Starting Render deployment for kandidatentekort-v6...")

# Step 1: Create the web service
service_data = {
    "type": "web_service",
    "name": "kandidatentekort-v6",
    "runtime": "python",
    "repo": "https://github.com/WouterArtsRecruitin/kandidatentekort-v6",
    "autoDeploy": "yes",
    "branch": "main",
    "buildCommand": "pip install -r requirements.txt",
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT app:app",
    "healthCheckPath": "/",
    "envVars": [
        {"key": "PYTHON_VERSION", "value": "3.11.0"},
        {"key": "FLASK_ENV", "value": "production"},
        {"key": "MANUAL_REVIEW_MODE", "value": "false"},
        {"key": "CLAUDE_API_KEY", "value": "PLACEHOLDER_CLAUDE_KEY"},
        {"key": "RESEND_API_KEY", "value": "PLACEHOLDER_RESEND_KEY"},
        {"key": "PIPEDRIVE_API_TOKEN", "value": "PLACEHOLDER_PIPEDRIVE_TOKEN"},
        {"key": "SLACK_WEBHOOK_URL", "value": "PLACEHOLDER_SLACK_WEBHOOK"}
    ],
    "plan": "starter"
}

print("📦 Creating web service...")
response = requests.post(
    f"{API_BASE_URL}/services",
    headers=headers,
    data=json.dumps(service_data)
)

if response.status_code == 201:
    service = response.json()
    service_id = service['service']['id']
    service_url = service['service']['url']
    print(f"✅ Service created successfully!")
    print(f"   Service ID: {service_id}")
    print(f"   URL: {service_url}")
    
    # Step 2: Trigger initial deploy
    print("\n🔄 Triggering initial deployment...")
    deploy_response = requests.post(
        f"{API_BASE_URL}/services/{service_id}/deploys",
        headers=headers
    )
    
    if deploy_response.status_code == 201:
        deploy = deploy_response.json()
        deploy_id = deploy['deploy']['id']
        print(f"✅ Deployment started!")
        print(f"   Deploy ID: {deploy_id}")
        
        print("\n⏳ Deployment in progress...")
        print("   This typically takes 3-5 minutes.")
        print(f"\n📊 Monitor deployment at:")
        print(f"   https://dashboard.render.com/web/{service_id}")
        
        print("\n⚠️  IMPORTANT NEXT STEPS:")
        print("1. Go to your Render dashboard")
        print("2. Navigate to Environment → Environment Variables")
        print("3. Update these placeholder values with your actual keys:")
        print("   - CLAUDE_API_KEY")
        print("   - RESEND_API_KEY")
        print("   - PIPEDRIVE_API_TOKEN")
        print("   - SLACK_WEBHOOK_URL")
        print("\n🔗 Direct link to environment settings:")
        print(f"   https://dashboard.render.com/web/{service_id}/env")
        
    else:
        print(f"❌ Failed to trigger deployment: {deploy_response.status_code}")
        print(deploy_response.json())
        
else:
    print(f"❌ Failed to create service: {response.status_code}")
    error_data = response.json()
    print(json.dumps(error_data, indent=2))
    
    # If service already exists, provide update instructions
    if "already exists" in str(error_data):
        print("\n💡 Service already exists. To update it:")
        print("1. Delete the existing service in Render dashboard")
        print("2. Run this script again")
        print("OR")
        print("3. Use the Render dashboard to manually update")

print("\n✨ Deployment script completed!")