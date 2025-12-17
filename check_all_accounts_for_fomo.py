#!/usr/bin/env python3
"""
Check all accessible accounts for FOMO campaigns
"""

import requests
import json
from datetime import datetime

# Use the old working token
ACCESS_TOKEN = "EAAYqzG39fnoBQNZBYHaznmpZBd39yH7gZAOwFM6ZCZCNRWQLWN1JlL8khNjFK6gDIsFKHyO2ODd2KhTmWjrNZAMaQimTm9ZCZAvLAZBXeM8SDcWK48Rf80EZCEYSsM6JTFABio02gnCPcQ2gUBdzY3BueVv2dONiuDMz26brmGnd7ZCpawdHt0PCIaOcKkZChepul4ilYWejHZCGO8iZApKKiPZCgmASqyNKOa65MZAXlLZCL7uUk9UGRFMGD4FoROVIDWLaMxEfsZC1q0ZCm3pll1CGOyrhjN3aDBV7OZAefAZDZD"
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

def get_all_accounts():
    """Get all ad accounts accessible by this token"""
    url = f"{BASE_URL}/me/adaccounts"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'account_id,id,name',
        'limit': 100
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' in data:
        return data['data']
    else:
        print(f"Error getting accounts: {data.get('error', {}).get('message', 'Unknown')}")
        return []

def get_campaigns_for_account(account_id, account_name):
    """Get all campaigns for an account"""
    url = f"{BASE_URL}/{account_id}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status,created_time,updated_time',
        'limit': 100
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    campaigns = []
    if 'data' in data:
        campaigns = data['data']
    
    return campaigns

def main():
    print("🔍 SEARCHING FOR FOMO CAMPAIGNS ACROSS ALL ACCOUNTS")
    print("=" * 60)
    
    # Get all accessible accounts
    accounts = get_all_accounts()
    print(f"\n📊 Found {len(accounts)} accessible accounts")
    
    all_fomo_campaigns = []
    all_kt_campaigns = []
    
    # Check each account
    for account in accounts:
        account_id = account['id']
        account_name = account.get('name', 'Unnamed')
        
        print(f"\n🏢 Checking: {account_name} ({account_id})")
        
        campaigns = get_campaigns_for_account(account_id, account_name)
        
        if campaigns:
            print(f"   📁 Total campaigns: {len(campaigns)}")
            
            # Filter for FOMO and KT campaigns
            for campaign in campaigns:
                name = campaign.get('name', '')
                if 'FOMO' in name:
                    all_fomo_campaigns.append({
                        'account': account_name,
                        'account_id': account_id,
                        'campaign': campaign
                    })
                    print(f"   ✅ FOMO: {name}")
                elif 'KT' in name or 'Kandidaten' in name.lower():
                    all_kt_campaigns.append({
                        'account': account_name,
                        'account_id': account_id,
                        'campaign': campaign
                    })
                    print(f"   📌 KT: {name}")
        else:
            print(f"   📭 No campaigns")
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    
    if all_fomo_campaigns:
        print(f"\n✅ Found {len(all_fomo_campaigns)} FOMO campaigns:")
        for item in all_fomo_campaigns:
            campaign = item['campaign']
            print(f"\n   Campaign: {campaign['name']}")
            print(f"   Account: {item['account']} ({item['account_id']})")
            print(f"   ID: {campaign['id']}")
            print(f"   Status: {campaign['status']}")
    else:
        print("\n❌ NO FOMO CAMPAIGNS FOUND!")
        
    if all_kt_campaigns:
        print(f"\n📌 Also found {len(all_kt_campaigns)} other KT campaigns:")
        for item in all_kt_campaigns[:5]:  # Show first 5
            campaign = item['campaign']
            print(f"   - {campaign['name']} in {item['account']}")
        if len(all_kt_campaigns) > 5:
            print(f"   ... and {len(all_kt_campaigns) - 5} more")
    
    print("\n\n💡 CONCLUSION:")
    if not all_fomo_campaigns:
        print("The FOMO campaigns appear to have been:")
        print("1. Deleted")
        print("2. Created in a different account") 
        print("3. Never successfully created")
        print("\nYou'll need to create them again.")

if __name__ == "__main__":
    main()