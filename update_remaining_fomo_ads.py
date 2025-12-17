#!/usr/bin/env python3
"""
Update remaining FOMO ads with available images
"""

import os
import json
import requests
import time

# Configuration
ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
AD_ACCOUNT_ID = 'act_1236576254450117'
API_VERSION = 'v24.0'
BASE_URL = f'https://graph.facebook.com/{API_VERSION}'

# Image folder paths
FEED_PATH = '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628'
STORY_PATH = '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/story_1080x1920'
CAROUSEL_PATH = '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/carousel_940x788'

# Updated mapping for remaining ads
REMAINING_AD_MAPPING = {
    # Ads that still need images
    'FOMO-Hot-Analyse': f'{FEED_PATH}/FEED_01_Overijssel_Problem_0reacties.png',  # Reuse this
    'FOMO-Warm-Q1weg': f'{FEED_PATH}/FEED_02_Gelderland_ROI_500perdag.png',  # Reuse this
    'FOMO-Warm-127bedrijven': f'{CAROUSEL_PATH}/CAROUSEL_01_Dark_Blue_Transform.png',  # Already uploaded
    'FOMO-Warm-Collega': f'{STORY_PATH}/STORY_01_Jouw_Verhaal_Premium.png',
    'FOMO-Cold-30000weg': f'{STORY_PATH}/STORY_04_Problem_Pain.png'
}

def get_ads_without_unique_images():
    """Get ads that still have the default image"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,creative{object_story_spec,id}',
        'effective_status': '["PAUSED","ACTIVE"]',
        'limit': 100
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    ads_to_update = []
    
    if 'data' in data:
        for ad in data['data']:
            if 'FOMO' in ad.get('name', ''):
                # Check if this ad still has the default image
                creative = ad.get('creative', {})
                story_spec = creative.get('object_story_spec', {})
                
                if 'link_data' in story_spec:
                    image_hash = story_spec['link_data'].get('image_hash', '')
                    # Check if it's the default image (all ads had same hash)
                    if image_hash == '98bc10e6f31d97f1f5c5b3d9b79cd758' or ad['name'] in REMAINING_AD_MAPPING:
                        ads_to_update.append(ad)
    
    return ads_to_update

def upload_image(image_path):
    """Upload an image to Facebook"""
    filename = os.path.basename(image_path)
    print(f"\n📸 Uploading: {filename}")
    
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
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
                        print(f"✅ Uploaded: {img_data['hash']}")
                        return img_data['hash']
                    
            print(f"❌ Upload error: {result.get('error', {}).get('message', 'Unknown')}")
            return None
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None

def update_ad_with_image(ad_id, ad_name, image_hash, creative_id):
    """Update ad creative with new image"""
    print(f"\n🔄 Updating: {ad_name}")
    
    # Get current creative
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
    
    # Create new creative
    new_creative_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    object_story_spec = creative_data['object_story_spec']
    
    # Update image hash
    if 'link_data' in object_story_spec:
        object_story_spec['link_data']['image_hash'] = image_hash
    
    new_creative_data = {
        'access_token': ACCESS_TOKEN,
        'name': f"{ad_name}_final_image_{int(time.time())}",
        'object_story_spec': json.dumps(object_story_spec)
    }
    
    create_response = requests.post(new_creative_url, data=new_creative_data)
    create_result = create_response.json()
    
    if 'id' in create_result:
        new_creative_id = create_result['id']
        
        # Update ad
        update_url = f"{BASE_URL}/{ad_id}"
        update_data = {
            'access_token': ACCESS_TOKEN,
            'creative': json.dumps({'creative_id': new_creative_id})
        }
        
        update_response = requests.post(update_url, data=update_data)
        update_result = update_response.json()
        
        if update_result.get('success'):
            print(f"✅ Successfully updated")
            return True
    
    return False

def main():
    print("🚀 UPDATING REMAINING FOMO ADS")
    print("=" * 60)
    
    if not ACCESS_TOKEN:
        print("❌ No token found!")
        return
    
    # Get ads that need updating
    print("\n🔍 Finding ads that need unique images...")
    ads_to_update = get_ads_without_unique_images()
    print(f"Found {len(ads_to_update)} ads to update")
    
    # Track uploaded images
    uploaded_images = {}
    success_count = 0
    
    # Update each ad
    for ad in ads_to_update:
        ad_name = ad['name']
        ad_id = ad['id']
        creative_id = ad.get('creative', {}).get('id')
        
        if ad_name in REMAINING_AD_MAPPING:
            image_path = REMAINING_AD_MAPPING[ad_name]
            
            # Check if already uploaded
            if image_path in uploaded_images:
                image_hash = uploaded_images[image_path]
                print(f"\n♻️  Reusing image for {ad_name}")
            else:
                image_hash = upload_image(image_path)
                if image_hash:
                    uploaded_images[image_path] = image_hash
                time.sleep(1)
            
            if image_hash and creative_id:
                if update_ad_with_image(ad_id, ad_name, image_hash, creative_id):
                    success_count += 1
                time.sleep(1)
    
    # List available story images for reference
    print("\n\n📁 Available Story Images:")
    if os.path.exists(STORY_PATH):
        for file in os.listdir(STORY_PATH):
            if file.endswith(('.png', '.jpg')):
                print(f"   - {file}")
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    print(f"\n✅ Successfully updated: {success_count} ads")
    print(f"✅ Total FOMO ads should now have unique images")
    
    print("\n\n🎯 CAMPAIGN STATUS:")
    print("- COLD Campaign: Focus on €500/day pain")
    print("- WARM Campaign: Social proof (127 companies)")
    print("- HOT Campaign: Urgency & countdown")
    
    print("\n\n⚡ READY TO ACTIVATE!")
    print("1. Go to Ads Manager")
    print("2. Review all 12 ads have different images")
    print("3. Activate the 3 FOMO campaigns")
    print("4. Set to €180/day total budget")

if __name__ == "__main__":
    main()