#!/usr/bin/env python3
"""
Update FOMO ads with unique professional images
"""

import os
import json
import requests
import time
from pathlib import Path

# Configuration
ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
AD_ACCOUNT_ID = 'act_1236576254450117'
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# Image folder
IMAGE_BASE_PATH = '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS'

# Ad to Image Mapping - Each ad gets a unique image
AD_IMAGE_MAPPING = {
    # COLD Campaign - Focus on pain/problem
    'FOMO-Cold-47dagen': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_02_Gelderland_ROI_500perdag.png',
    'FOMO-Cold-87procent': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_01_Overijssel_Problem_0reacties.png',
    'FOMO-Cold-Concurrent': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_05_Problem_Pain.png',
    'FOMO-Cold-30000weg': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_08_Zero_Shock.png',
    
    # WARM Campaign - Social proof & success
    'FOMO-Warm-47dagen': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_03_Gelderland_SocialProof.png',
    'FOMO-Warm-127bedrijven': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_11_Canva_Industry_Quote.jpg',
    'FOMO-Warm-Collega': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_06_Solution_Hope.png',
    'FOMO-Warm-Q1weg': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_12_Canva_Case_Study.jpg',
    
    # HOT Campaign - Urgency & CTA
    'FOMO-Hot-24uur': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_07_Urgency_CTA.png',
    'FOMO-Hot-Weekend': f'{IMAGE_BASE_PATH}/story_1080x1920/STORY_09_Urgency_CTA.png',  # Will be cropped
    'FOMO-Hot-Analyse': f'{IMAGE_BASE_PATH}/feed_1200x628/FEED_04_Waarom_Niemand_Reageert.png',
    'FOMO-Hot-Maandag': f'{IMAGE_BASE_PATH}/carousel_940x788/CAROUSEL_01_Dark_Blue_Transform.png'
}

def upload_image(image_path):
    """Upload an image to Facebook"""
    filename = os.path.basename(image_path)
    print(f"\n📸 Uploading: {filename}")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        # Try alternate paths
        if 'story_1080x1920' in image_path:
            # For story images, use feed version instead
            alt_path = image_path.replace('story_1080x1920/STORY_', 'feed_1200x628/FEED_')
            if os.path.exists(alt_path):
                print(f"   Using alternate: {os.path.basename(alt_path)}")
                image_path = alt_path
            else:
                return None
        else:
            return None
    
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adimages"
    
    try:
        with open(image_path, 'rb') as image_file:
            files = {'filename': (filename, image_file, 'image/png')}
            params = {'access_token': ACCESS_TOKEN}
            
            response = requests.post(url, params=params, files=files)
            result = response.json()
            
            if 'images' in result:
                for img_name, img_data in result['images'].items():
                    if 'hash' in img_data:
                        print(f"✅ Uploaded successfully: {img_data['hash']}")
                        return img_data['hash']
                    
            print(f"❌ Upload error: {result.get('error', {}).get('message', 'Unknown error')}")
            return None
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def get_all_fomo_ads():
    """Get all FOMO campaign ads"""
    # First get campaigns
    campaigns_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name',
        'effective_status': '["PAUSED","ACTIVE"]',
        'limit': 50
    }
    
    response = requests.get(campaigns_url, params=params)
    campaigns = response.json().get('data', [])
    
    all_ads = []
    
    for campaign in campaigns:
        if 'FOMO' in campaign.get('name', ''):
            # Get ads for this campaign
            ads_url = f"{BASE_URL}/{campaign['id']}/ads"
            ads_params = {
                'access_token': ACCESS_TOKEN,
                'fields': 'id,name,creative{id}',
                'limit': 50
            }
            
            ads_response = requests.get(ads_url, params=ads_params)
            ads_data = ads_response.json()
            
            if 'data' in ads_data:
                for ad in ads_data['data']:
                    ad['campaign_name'] = campaign['name']
                    all_ads.append(ad)
    
    return all_ads

def update_ad_with_image(ad_id, ad_name, image_hash, creative_id):
    """Update an ad's creative with new image"""
    print(f"\n🔄 Updating ad: {ad_name}")
    
    # Get current creative data
    creative_url = f"{BASE_URL}/{creative_id}"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'object_story_spec,name'
    }
    
    response = requests.get(creative_url, params=params)
    creative_data = response.json()
    
    if 'object_story_spec' not in creative_data:
        print(f"❌ No object_story_spec found")
        return False
    
    # Create new creative with updated image
    new_creative_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    object_story_spec = creative_data['object_story_spec']
    
    # Update image hash in link_data
    if 'link_data' in object_story_spec:
        object_story_spec['link_data']['image_hash'] = image_hash
    
    new_creative_data = {
        'access_token': ACCESS_TOKEN,
        'name': f"{ad_name}_unique_image_{int(time.time())}",
        'object_story_spec': json.dumps(object_story_spec)
    }
    
    create_response = requests.post(new_creative_url, data=new_creative_data)
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
        
        if update_result.get('success'):
            print(f"✅ Successfully updated with unique image")
            return True
        else:
            print(f"❌ Failed to update ad: {update_result.get('error', {}).get('message', 'Unknown error')}")
    else:
        print(f"❌ Failed to create new creative: {create_result.get('error', {}).get('message', 'Unknown error')}")
    
    return False

def main():
    print("🚀 FOMO ADS - UNIQUE IMAGE UPDATE")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("❌ No Facebook access token found!")
        return
    
    # Track uploaded images to avoid duplicates
    uploaded_images = {}
    
    # Get all FOMO ads
    print("\n📋 Getting all FOMO ads...")
    all_ads = get_all_fomo_ads()
    print(f"Found {len(all_ads)} FOMO ads")
    
    # Sort ads by campaign for organized processing
    ads_by_campaign = {}
    for ad in all_ads:
        campaign = ad['campaign_name']
        if campaign not in ads_by_campaign:
            ads_by_campaign[campaign] = []
        ads_by_campaign[campaign].append(ad)
    
    # Process each campaign
    success_count = 0
    
    for campaign_name, ads in ads_by_campaign.items():
        print(f"\n\n{'='*60}")
        print(f"📍 Processing {campaign_name}")
        print(f"{'='*60}")
        
        for ad in ads:
            ad_name = ad['name']
            ad_id = ad['id']
            creative_id = ad.get('creative', {}).get('id')
            
            if not creative_id:
                print(f"\n❌ No creative found for {ad_name}")
                continue
            
            # Get the mapped image for this ad
            if ad_name in AD_IMAGE_MAPPING:
                image_path = AD_IMAGE_MAPPING[ad_name]
                
                # Check if we already uploaded this image
                if image_path in uploaded_images:
                    image_hash = uploaded_images[image_path]
                    print(f"\n♻️  Reusing already uploaded image for {ad_name}")
                else:
                    # Upload new image
                    image_hash = upload_image(image_path)
                    if image_hash:
                        uploaded_images[image_path] = image_hash
                    time.sleep(1)  # Rate limiting
                
                if image_hash:
                    # Update the ad with the new image
                    if update_ad_with_image(ad_id, ad_name, image_hash, creative_id):
                        success_count += 1
                    time.sleep(1)  # Rate limiting
            else:
                print(f"\n⚠️  No image mapping found for {ad_name}")
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"\n✅ Successfully updated: {success_count}/{len(all_ads)} ads")
    print(f"✅ Unique images uploaded: {len(uploaded_images)}")
    
    if success_count < len(all_ads):
        print(f"\n⚠️  Some ads were not updated. Check the logs above.")
    
    print("\n\n⚡ NEXT STEPS:")
    print("1. Go to Facebook Ads Manager")
    print("2. Review the updated ads with unique images")
    print("3. Activate the FOMO campaigns")
    print("4. Monitor performance:")
    print("   - CTR target: >2.5%")
    print("   - CPA target: <€30")
    print("   - Frequency: <3.0")
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main()