#!/usr/bin/env python3
"""
Analyze FOMO campaign structure and image assignments
"""

import os
import json
import requests
from collections import defaultdict

# Configuration
ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
AD_ACCOUNT_ID = 'act_1236576254450117'
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# FOMO Campaign IDs
CAMPAIGN_IDS = {
    'COLD': '120241127981990536',
    'WARM': '120241127982370536', 
    'HOT': '120241127983150536'
}

def get_campaign_details(campaign_id, campaign_type):
    """Get detailed info about a campaign"""
    print(f"\n📊 Analyzing {campaign_type} Campaign (ID: {campaign_id})")
    print("=" * 60)
    
    # Get ad sets
    url = f"{BASE_URL}/{campaign_id}/adsets"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,daily_budget,status'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if 'data' not in data:
        print(f"❌ Error getting ad sets: {data.get('error', {}).get('message', 'Unknown')}")
        return
    
    adsets = data['data']
    print(f"\n📁 Found {len(adsets)} Ad Sets:")
    
    total_ads = 0
    image_usage = defaultdict(int)
    
    for adset in adsets:
        print(f"\n  Ad Set: {adset['name']}")
        print(f"  ID: {adset['id']}")
        print(f"  Budget: €{int(adset.get('daily_budget', 0))/100:.2f}/day")
        print(f"  Status: {adset['status']}")
        
        # Get ads for this ad set
        ads_url = f"{BASE_URL}/{adset['id']}/ads"
        ads_params = {
            'access_token': ACCESS_TOKEN,
            'fields': 'id,name,status,creative{object_story_spec,asset_feed_spec}'
        }
        
        ads_response = requests.get(ads_url, params=ads_params)
        ads_data = ads_response.json()
        
        if 'data' in ads_data:
            ads = ads_data['data']
            print(f"  Ads: {len(ads)}")
            total_ads += len(ads)
            
            for ad in ads:
                print(f"\n    🎯 Ad: {ad['name']}")
                print(f"       ID: {ad['id']}")
                print(f"       Status: {ad['status']}")
                
                # Check for image hash
                if 'creative' in ad and 'object_story_spec' in ad['creative']:
                    story_spec = ad['creative']['object_story_spec']
                    
                    # Check different places where image might be
                    image_hash = None
                    if 'link_data' in story_spec and 'image_hash' in story_spec['link_data']:
                        image_hash = story_spec['link_data']['image_hash']
                    elif 'video_data' in story_spec and 'image_hash' in story_spec['video_data']:
                        image_hash = story_spec['video_data']['image_hash']
                    
                    if image_hash:
                        print(f"       Image: {image_hash}")
                        image_usage[image_hash] += 1
                    else:
                        print(f"       Image: ❌ No image found")
    
    # Summary for this campaign
    print(f"\n  📊 Campaign Summary:")
    print(f"  - Total Ad Sets: {len(adsets)}")
    print(f"  - Total Ads: {total_ads}")
    print(f"  - Unique Images: {len(image_usage)}")
    
    if len(image_usage) < total_ads:
        print(f"  ⚠️  ISSUE: Same image used across multiple ads!")
        print(f"  Image usage breakdown:")
        for img_hash, count in image_usage.items():
            print(f"    - {img_hash[:8]}...: used {count} times")

def main():
    print("🔍 FOMO CAMPAIGN STRUCTURE ANALYSIS")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("❌ No Facebook access token found!")
        return
    
    # Analyze each campaign
    for campaign_type, campaign_id in CAMPAIGN_IDS.items():
        get_campaign_details(campaign_id, campaign_type)
    
    print("\n\n" + "="*60)
    print("💡 RECOMMENDATIONS:")
    print("="*60)
    print("\n1. Each ad should have a unique, relevant image")
    print("2. Images should match the ad copy theme:")
    print("   - COLD: Focus on €500/day loss visuals")
    print("   - WARM: Show social proof (127 companies)")
    print("   - HOT: Urgency/countdown elements")
    print("\n3. Use professional images from:")
    print("   /Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/")

if __name__ == "__main__":
    main()