#!/usr/bin/env python3
"""
Find kandidatentekort campaigns across all ad accounts
"""

import os
import json
import requests

# Facebook API configuration
ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

def get_ad_accounts():
    """Get all ad accounts"""
    url = f"{BASE_URL}/me/adaccounts"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'name,account_id',
        'limit': 100
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'data' in data:
            return data['data']
        else:
            print(f"Error: {data.get('error', {}).get('message', 'Unknown error')}")
            return []
    except Exception as e:
        print(f"Exception: {str(e)}")
        return []

def get_campaigns_for_account(account_id):
    """Get campaigns for a specific ad account"""
    url = f"{BASE_URL}/{account_id}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,created_time',
        'limit': 100
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        campaigns = []
        if 'data' in data:
            for campaign in data['data']:
                # Check if campaign is related to kandidatentekort
                name_lower = campaign.get('name', '').lower()
                if any(term in name_lower for term in ['kandidaten', 'fomo', 'cold', 'warm', 'hot']):
                    campaigns.append(campaign)
        
        return campaigns
    except Exception as e:
        return []

def main():
    print("🔍 Searching for Kandidatentekort campaigns across all ad accounts")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("❌ No Facebook access token found!")
        return
    
    # Get all ad accounts
    ad_accounts = get_ad_accounts()
    print(f"\n📊 Found {len(ad_accounts)} ad accounts")
    
    all_campaigns = []
    
    # Check each account
    for account in ad_accounts:
        account_id = account['id']
        account_name = account.get('name', 'Unnamed')
        
        print(f"\n🔍 Checking: {account_name} ({account_id})")
        
        campaigns = get_campaigns_for_account(account_id)
        if campaigns:
            print(f"   ✅ Found {len(campaigns)} relevant campaigns:")
            for campaign in campaigns:
                print(f"      - {campaign['name']} (ID: {campaign['id']}, Status: {campaign['status']})")
                all_campaigns.append({
                    'account_id': account_id,
                    'account_name': account_name,
                    'campaign': campaign
                })
        else:
            print(f"   ❌ No relevant campaigns found")
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"\nTotal relevant campaigns found: {len(all_campaigns)}")
    
    # Save results
    if all_campaigns:
        with open('found_campaigns.json', 'w') as f:
            json.dump(all_campaigns, f, indent=2)
        print("\n✅ Results saved to found_campaigns.json")
        
        # Group by account
        print("\n📋 Campaigns by Account:")
        accounts_with_campaigns = {}
        for item in all_campaigns:
            account_id = item['account_id']
            if account_id not in accounts_with_campaigns:
                accounts_with_campaigns[account_id] = {
                    'name': item['account_name'],
                    'campaigns': []
                }
            accounts_with_campaigns[account_id]['campaigns'].append(item['campaign'])
        
        for account_id, data in accounts_with_campaigns.items():
            print(f"\n🏢 {data['name']} ({account_id}):")
            for campaign in data['campaigns']:
                print(f"   - {campaign['name']}")
                print(f"     ID: {campaign['id']}")
                print(f"     Status: {campaign['status']}")

if __name__ == "__main__":
    main()