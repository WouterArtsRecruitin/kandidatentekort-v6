#!/usr/bin/env python3
"""
Upload professional FOMO images to Facebook using direct API calls
"""

import os
import json
import requests
import time
from pathlib import Path

# Facebook API configuration
ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
AD_ACCOUNT_ID = 'act_1236576254450117'  # Recruitin account - waar de FOMO campaigns staan
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# Professional image mappings
IMAGE_MAPPINGS = {
    'cold': {
        'path': '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628/FEED_02_Gelderland_ROI_500perdag.png',
        'description': 'FOMO Cold - €500 per dag verlies'
    },
    'warm': {
        'path': '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628/FEED_03_Gelderland_SocialProof.png', 
        'description': 'FOMO Warm - 127 bedrijven geholpen'
    },
    'hot': {
        'path': '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628/FEED_07_Urgency_CTA.png',
        'description': 'FOMO Hot - 24 uur actie'
    }
}

def upload_image(image_path, description):
    """Upload an image to Facebook"""
    print(f"\n📸 Uploading: {os.path.basename(image_path)}")
    print(f"   Description: {description}")
    
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adimages"
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {'bytes': image_file}
            params = {
                'access_token': ACCESS_TOKEN
            }
            
            response = requests.post(url, params=params, files=files)
            result = response.json()
            
            if 'images' in result:
                image_name = os.path.basename(image_path)
                for img_key, img_data in result['images'].items():
                    if 'hash' in img_data:
                        print(f"✅ Successfully uploaded: {img_data['hash']}")
                        return img_data['hash']
            else:
                print(f"❌ Error: {result.get('error', {}).get('message', 'Unknown error')}")
                return None
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def get_fomo_campaigns():
    """Get all FOMO campaigns"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status',
        'effective_status': '["PAUSED","ACTIVE"]'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        fomo_campaigns = []
        if 'data' in data:
            for campaign in data['data']:
                if 'FOMO' in campaign.get('name', ''):
                    fomo_campaigns.append(campaign)
                    print(f"\n📊 Found FOMO Campaign: {campaign['name']}")
                    print(f"   ID: {campaign['id']}")
                    print(f"   Status: {campaign['status']}")
        
        return fomo_campaigns
    except Exception as e:
        print(f"❌ Error getting campaigns: {str(e)}")
        return []

def get_ads_for_campaign(campaign_id):
    """Get all ads for a campaign"""
    url = f"{BASE_URL}/{campaign_id}/ads"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,creative{id}',
        'effective_status': '["PAUSED","ACTIVE"]'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        ads = []
        if 'data' in data:
            for ad in data['data']:
                ads.append(ad)
        
        return ads
    except Exception as e:
        print(f"❌ Error getting ads: {str(e)}")
        return []

def update_ad_creative(ad_id, ad_name, image_hash):
    """Update an ad's creative with new image"""
    # First get the current creative
    url = f"{BASE_URL}/{ad_id}"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'creative{object_story_spec}'
    }
    
    try:
        response = requests.get(url, params=params)
        ad_data = response.json()
        
        if 'creative' not in ad_data:
            print(f"❌ No creative found for ad")
            return False
        
        # Get the object story spec
        object_story_spec = ad_data['creative'].get('object_story_spec', {})
        
        # Update the image hash in link_data
        if 'link_data' in object_story_spec:
            object_story_spec['link_data']['image_hash'] = image_hash
        
        # Create new creative
        create_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
        creative_data = {
            'access_token': ACCESS_TOKEN,
            'name': f"{ad_name}_updated_{int(time.time())}",
            'object_story_spec': json.dumps(object_story_spec)
        }
        
        create_response = requests.post(create_url, data=creative_data)
        create_result = create_response.json()
        
        if 'id' in create_result:
            new_creative_id = create_result['id']
            
            # Update the ad with new creative
            update_url = f"{BASE_URL}/{ad_id}"
            update_data = {
                'access_token': ACCESS_TOKEN,
                'creative': json.dumps({'creative_id': new_creative_id})
            }
            
            update_response = requests.post(update_url, data=update_data)
            update_result = update_response.json()
            
            if 'success' in update_result and update_result['success']:
                print(f"✅ Successfully updated ad creative")
                return True
            else:
                print(f"❌ Failed to update ad: {update_result.get('error', {}).get('message', 'Unknown error')}")
                return False
        else:
            print(f"❌ Failed to create new creative: {create_result.get('error', {}).get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception updating ad: {str(e)}")
        return False

def main():
    print("🚀 Professional FOMO Image Upload & Ad Update")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("❌ No Facebook access token found in environment")
        return
    
    # Track results
    uploaded_images = {}
    
    # Upload images
    print("\n📤 UPLOADING IMAGES")
    print("=" * 60)
    
    for campaign_type, config in IMAGE_MAPPINGS.items():
        image_hash = upload_image(config['path'], config['description'])
        if image_hash:
            uploaded_images[campaign_type] = image_hash
        time.sleep(1)  # Rate limiting
    
    # Get FOMO campaigns
    print("\n\n🔍 FINDING FOMO CAMPAIGNS")
    print("=" * 60)
    
    fomo_campaigns = get_fomo_campaigns()
    
    if not fomo_campaigns:
        print("\n❌ No FOMO campaigns found!")
        return
    
    # Update ads with new images
    print("\n\n🔄 UPDATING ADS WITH NEW IMAGES")
    print("=" * 60)
    
    total_updated = 0
    
    for campaign in fomo_campaigns:
        campaign_name = campaign['name'].lower()
        
        # Determine which image to use based on campaign name
        if 'cold' in campaign_name and 'cold' in uploaded_images:
            image_hash = uploaded_images['cold']
        elif 'warm' in campaign_name and 'warm' in uploaded_images:
            image_hash = uploaded_images['warm']
        elif 'hot' in campaign_name and 'hot' in uploaded_images:
            image_hash = uploaded_images['hot']
        else:
            continue
        
        print(f"\n📍 Processing campaign: {campaign['name']}")
        
        # Get ads for this campaign
        ads = get_ads_for_campaign(campaign['id'])
        
        for ad in ads:
            print(f"\n   🎯 Updating ad: {ad['name']}")
            if update_ad_creative(ad['id'], ad['name'], image_hash):
                total_updated += 1
            time.sleep(1)  # Rate limiting
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    print(f"\n✅ Images Uploaded: {len(uploaded_images)}")
    for campaign_type, hash_val in uploaded_images.items():
        print(f"   - {campaign_type}: {hash_val}")
    
    print(f"\n✅ Ads Updated: {total_updated}")
    
    print("\n\n⚡ NEXT STEPS:")
    print("1. Go to Facebook Ads Manager")
    print("2. Review the updated ads") 
    print("3. Activate the FOMO campaigns")
    print("4. Monitor performance")
    
    print("\n\n✨ Done!")

if __name__ == "__main__":
    main()