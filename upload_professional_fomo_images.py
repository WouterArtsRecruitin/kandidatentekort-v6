#!/usr/bin/env python3
"""
Upload professional FOMO images to Facebook and update ads
"""

import os
import json
import time
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Facebook API configuration
ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
AD_ACCOUNT_ID = 'act_757606233848402'

# Initialize the Facebook API
FacebookAdsApi.init(access_token=ACCESS_TOKEN)

# Professional image mappings
IMAGE_MAPPINGS = {
    'cold': {
        'path': '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628/FEED_02_Gelderland_ROI_500perdag.png',
        'ads': ['FOMO-COLD-Werkvoorbereider-8weken', 'FOMO-COLD-CNC-Programmeur-12weken', 
                'FOMO-COLD-Lasser-10weken', 'FOMO-COLD-Maintenance-Engineer-6weken']
    },
    'warm': {
        'path': '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628/FEED_03_Gelderland_SocialProof.png',
        'ads': ['FOMO-WARM-127-Bedrijven-Week', 'FOMO-WARM-47-Vacatures-3dagen',
                'FOMO-WARM-93%-Sneller-Gevuld', 'FOMO-WARM-Elke-24uur-Update']
    },
    'hot': {
        'path': '/Users/wouterarts/Kandidatentekortfull/f24 imagesiles/META_ADS_COMPLETE_24_DESIGNS/feed_1200x628/FEED_07_Urgency_CTA.png',
        'ads': ['FOMO-HOT-24uur-Gratis', 'FOMO-HOT-Laatste-3-Plekken',
                'FOMO-HOT-Morgen-297-Euro', 'FOMO-HOT-Weekend-Beslissen']
    }
}

def upload_image(image_path):
    """Upload an image to Facebook"""
    print(f"\nUploading image: {os.path.basename(image_path)}")
    
    image = AdImage(parent_id=AD_ACCOUNT_ID)
    image[AdImage.Field.filename] = image_path
    
    try:
        image.remote_create()
        print(f"✅ Image uploaded successfully: {image[AdImage.Field.hash]}")
        return image[AdImage.Field.hash]
    except Exception as e:
        print(f"❌ Error uploading image: {str(e)}")
        return None

def get_fomo_campaigns():
    """Get all FOMO campaigns"""
    account = AdAccount(AD_ACCOUNT_ID)
    campaigns = account.get_campaigns(
        fields=[Campaign.Field.name, Campaign.Field.id],
        params={'effective_status': ['PAUSED', 'ACTIVE']}
    )
    
    fomo_campaigns = []
    for campaign in campaigns:
        if 'FOMO' in campaign['name']:
            print(f"\n📊 Found FOMO Campaign: {campaign['name']} (ID: {campaign['id']})")
            fomo_campaigns.append(campaign)
    
    return fomo_campaigns

def update_ads_with_images(campaign_type, image_hash):
    """Update ads with new images"""
    account = AdAccount(AD_ACCOUNT_ID)
    
    # Get all ads
    ads = account.get_ads(
        fields=[Ad.Field.name, Ad.Field.id, Ad.Field.creative],
        params={'effective_status': ['PAUSED', 'ACTIVE']}
    )
    
    updated_count = 0
    target_ad_names = IMAGE_MAPPINGS[campaign_type]['ads']
    
    for ad in ads:
        if any(target_name in ad['name'] for target_name in target_ad_names):
            print(f"\n🔄 Updating ad: {ad['name']}")
            
            try:
                # Get the creative
                creative_id = ad['creative']['id']
                creative = AdCreative(creative_id)
                creative_data = creative.remote_read(fields=['object_story_spec'])
                
                # Create new creative with updated image
                new_creative = AdCreative(parent_id=AD_ACCOUNT_ID)
                
                # Copy existing creative data
                object_story_spec = creative_data['object_story_spec']
                
                # Update image hash
                if 'link_data' in object_story_spec:
                    object_story_spec['link_data']['image_hash'] = image_hash
                elif 'video_data' in object_story_spec:
                    object_story_spec['video_data']['image_hash'] = image_hash
                
                new_creative.update({
                    'name': f"{ad['name']}_updated_{int(time.time())}",
                    'object_story_spec': object_story_spec
                })
                
                new_creative.remote_create()
                
                # Update the ad with new creative
                ad_obj = Ad(ad['id'])
                ad_obj.update({
                    'creative': {'creative_id': new_creative['id']}
                })
                ad_obj.remote_update()
                
                print(f"✅ Ad updated successfully")
                updated_count += 1
                
            except Exception as e:
                print(f"❌ Error updating ad: {str(e)}")
    
    return updated_count

def main():
    print("🚀 Starting Professional FOMO Image Upload and Ad Update")
    print("=" * 60)
    
    # Track results
    results = {
        'images_uploaded': {},
        'ads_updated': {}
    }
    
    # Upload images and update ads for each campaign type
    for campaign_type, config in IMAGE_MAPPINGS.items():
        print(f"\n\n{'='*60}")
        print(f"📁 Processing {campaign_type.upper()} campaign images")
        print(f"{'='*60}")
        
        # Upload image
        image_hash = upload_image(config['path'])
        if image_hash:
            results['images_uploaded'][campaign_type] = image_hash
            
            # Update ads
            updated = update_ads_with_images(campaign_type, image_hash)
            results['ads_updated'][campaign_type] = updated
            print(f"\n✅ Updated {updated} ads for {campaign_type} campaign")
        else:
            print(f"\n❌ Failed to upload image for {campaign_type} campaign")
    
    # Summary
    print("\n\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    print("\n✅ Images Uploaded:")
    for campaign_type, hash_val in results['images_uploaded'].items():
        print(f"   - {campaign_type}: {hash_val}")
    
    print(f"\n✅ Total Ads Updated:")
    total_updated = sum(results['ads_updated'].values())
    print(f"   - {total_updated} ads across {len(results['ads_updated'])} campaigns")
    
    print("\n\n⚡ NEXT STEPS:")
    print("1. Go to Facebook Ads Manager")
    print("2. Review the updated ads")
    print("3. Activate the FOMO campaigns")
    print("4. Monitor performance")
    
    # Get campaign list for reference
    print("\n\n📋 FOMO Campaigns Found:")
    fomo_campaigns = get_fomo_campaigns()
    
    print("\n\n✅ Professional images uploaded and ads updated!")

if __name__ == "__main__":
    main()