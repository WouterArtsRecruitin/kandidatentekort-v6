#!/usr/bin/env python3
"""
Find FOMO campaigns with new token across all accessible accounts
"""

import requests
import json

# New token from credentials
ACCESS_TOKEN = "EAASX9Iy8fL8BPYsXtZBnl8nCHRZBFirORx0H6fe9ColghZC2ZCLtWISBnP8fYdkICv9cbTPl9YYLmcKI4sZB42l9PjIr6bj9gD74X0E6qtGMETAfAcEo50bNnqiEZB8S0hZBDVNsmwumHjLXn31ptOCoZCQWZBiCiR2HhJ6iDrqOsNlZB6Ew0ALCuF9tFEJA0IgQZDZD"
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# Known account IDs to check
ACCOUNT_IDS_TO_CHECK = [
    'act_1236576254450117',  # Recruitin account (waar ze zouden moeten staan)
    'act_1443564313411457',  # New account from credentials
    'act_1386399691657486',  # Other known account
    'act_6856944711035374',  # Euromaster
]

def check_account(account_id):
    """Check a specific account for campaigns"""
    print(f"\n🔍 Checking {account_id}...")
    
    url = f"{BASE_URL}/{account_id}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,created_time',
        'limit': 100
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'error' in data:
            print(f"   ❌ Error: {data['error'].get('message', 'Unknown error')}")
            return []
        
        campaigns = data.get('data', [])
        fomo_campaigns = []
        
        for campaign in campaigns:
            name = campaign.get('name', '')
            if 'FOMO' in name or 'fomo' in name.lower():
                fomo_campaigns.append(campaign)
                print(f"   ✅ FOUND: {name} (ID: {campaign['id']})")
        
        if not fomo_campaigns and campaigns:
            print(f"   📊 Has {len(campaigns)} campaigns but no FOMO campaigns")
            # Show first few campaign names
            for i, campaign in enumerate(campaigns[:5]):
                print(f"      - {campaign.get('name', 'Unnamed')}")
            if len(campaigns) > 5:
                print(f"      ... and {len(campaigns) - 5} more")
        elif not campaigns:
            print(f"   📭 No campaigns found")
            
        return fomo_campaigns
        
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return []

def get_accessible_accounts():
    """Get all accounts this token can access"""
    print("📋 Getting all accessible accounts...")
    
    url = f"{BASE_URL}/me/adaccounts"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'account_id,id,name',
        'limit': 100
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'data' in data:
            accounts = data['data']
            print(f"✅ Found {len(accounts)} accessible accounts:")
            for acc in accounts:
                print(f"   - {acc.get('name', 'Unnamed')} ({acc['id']})")
            return [acc['id'] for acc in accounts]
        else:
            print(f"❌ Error: {data.get('error', {}).get('message', 'Unknown')}")
            return []
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []

def main():
    print("🚀 SEARCHING FOR FOMO CAMPAIGNS")
    print("=" * 60)
    
    # First get all accessible accounts
    accessible_accounts = get_accessible_accounts()
    
    # Add accessible accounts to check list
    all_accounts_to_check = list(set(ACCOUNT_IDS_TO_CHECK + accessible_accounts))
    
    print(f"\n📊 Checking {len(all_accounts_to_check)} accounts for FOMO campaigns...")
    print("=" * 60)
    
    all_fomo_campaigns = []
    
    # Check each account
    for account_id in all_accounts_to_check:
        fomo_campaigns = check_account(account_id)
        if fomo_campaigns:
            all_fomo_campaigns.extend(fomo_campaigns)
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    if all_fomo_campaigns:
        print(f"\n✅ Found {len(all_fomo_campaigns)} FOMO campaigns:")
        for campaign in all_fomo_campaigns:
            print(f"\n   Campaign: {campaign['name']}")
            print(f"   ID: {campaign['id']}")
            print(f"   Status: {campaign['status']}")
            print(f"   Created: {campaign.get('created_time', 'Unknown')}")
    else:
        print("\n❌ No FOMO campaigns found in any accessible account!")
        print("\nPossible reasons:")
        print("1. Campaigns were created with a different token")
        print("2. Campaigns are in an account this token can't access")
        print("3. Campaigns were deleted")
        print("\nYou may need to recreate them with the current token.")

if __name__ == "__main__":
    main()