#!/usr/bin/env python3
"""
Create FOMO images and upload to Facebook
Using simple PIL for image generation
"""

from PIL import Image, ImageDraw, ImageFont
import requests
import json
import io
import os
from datetime import datetime

# Facebook Configuration
ACCESS_TOKEN = "EAAYqzG39fnoBQI36ltDvwpuGHU9TJpa6DSe4ZCr5Twrv6nHGwdOQnOVEtXez6Md7lYFTdsPq3ZA9IWjAU49eXcGmtDrA6GdiicwT5faw4vHQqWcg5q2Eof5AN3naiBXBueSE7RBbMIrdxvYjpu7t0TOahFDDkruV1DTUkTrsv5H6oZCkqn1F2UPAsZB0yQ83sVpe2Y2unEFoapJRSJssZCfpKuGb0NK5bT27VdS22rYmnMZAGgbCIKqer8keYj4t9stUqDh1tpObdOZBoIWFc2eZCCvVzrZC3"
AD_ACCOUNT_ID = "act_1236576254450117"

def create_fomo_cold_image():
    """Create COLD campaign image - €500 per day"""
    # Create image
    img = Image.new('RGB', (1200, 628), color='black')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a bold font, fallback to default
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Main text: €500 PER DAG
    draw.text((600, 150), "€500 PER DAG", font=title_font, fill='red', anchor="mm")
    
    # Subtitle: KOST JE DIE LEGE VACATURE
    draw.text((600, 250), "KOST JE DIE LEGE VACATURE", font=subtitle_font, fill='white', anchor="mm")
    
    # Calculation box
    draw.rectangle([(200, 320), (1000, 420)], outline='red', width=3)
    draw.text((600, 370), "47 DAGEN = €23.500 WEG", font=subtitle_font, fill='white', anchor="mm")
    
    # Bottom text
    draw.text((600, 500), "Stop het bloeden. Start vandaag.", font=small_font, fill='#FF6B35', anchor="mm")
    
    # Save
    img.save('kandidatentekort_cold_500perdag.png', quality=95)
    print("✅ Created: kandidatentekort_cold_500perdag.png")
    return 'kandidatentekort_cold_500perdag.png'

def create_fomo_warm_image():
    """Create WARM campaign image - 127 bedrijven"""
    img = Image.new('RGB', (1200, 628), color='#1a1a1a')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 100)
        number_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 140)
        list_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
    except:
        title_font = ImageFont.load_default()
        number_font = ImageFont.load_default()
        list_font = ImageFont.load_default()
    
    # Header
    draw.text((600, 80), "DEZE WEEK GEHOLPEN:", font=title_font, fill='#FF6B35', anchor="mm")
    
    # Big number
    draw.text((600, 180), "127", font=number_font, fill='white', anchor="mm")
    draw.text((600, 250), "BEDRIJVEN", font=title_font, fill='white', anchor="mm")
    
    # Success list
    y = 350
    successes = [
        "✓ Werkvoorbereider - 11 reacties",
        "✓ Maintenance Engineer - 3 weken",
        "✓ Projectleider - 8 CV's"
    ]
    
    for success in successes:
        draw.text((300, y), success, font=list_font, fill='#10B981')
        y += 60
    
    # Bottom urgency
    draw.rectangle([(200, 530), (1000, 590)], fill='#FF6B35')
    draw.text((600, 560), "NOG 3 PLEKKEN DEZE WEEK", font=list_font, fill='black', anchor="mm")
    
    img.save('kandidatentekort_warm_127bedrijven.png', quality=95)
    print("✅ Created: kandidatentekort_warm_127bedrijven.png")
    return 'kandidatentekort_warm_127bedrijven.png'

def create_fomo_hot_image():
    """Create HOT campaign image - 24 hour countdown"""
    img = Image.new('RGB', (1200, 628), color='black')
    draw = ImageDraw.Draw(img)
    
    # Red border
    draw.rectangle([(10, 10), (1190, 618)], outline='red', width=10)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
        timer_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 160)
        price_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
    except:
        title_font = ImageFont.load_default()
        timer_font = ImageFont.load_default()
        price_font = ImageFont.load_default()
    
    # Timer
    draw.text((600, 120), "NOG", font=title_font, fill='white', anchor="mm")
    draw.text((600, 240), "24 UUR", font=timer_font, fill='red', anchor="mm")
    
    # Price slash
    draw.text((400, 380), "€297", font=price_font, fill='gray', anchor="mm")
    draw.line([(300, 380), (500, 380)], fill='red', width=5)
    draw.text((700, 380), "€0", font=price_font, fill='#10B981', anchor="mm")
    
    # CTA
    draw.rectangle([(300, 480), (900, 560)], fill='#FF6B35')
    draw.text((600, 520), "CLAIM GRATIS ANALYSE", font=title_font, fill='white', anchor="mm")
    
    img.save('kandidatentekort_hot_24uur.png', quality=95)
    print("✅ Created: kandidatentekort_hot_24uur.png")
    return 'kandidatentekort_hot_24uur.png'

def upload_image_to_facebook(image_path):
    """Upload image to Facebook"""
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/adimages"
    
    with open(image_path, 'rb') as image_file:
        files = {'file': image_file}
        data = {'access_token': ACCESS_TOKEN}
        
        response = requests.post(url, files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            image_hash = result['images'][os.path.basename(image_path)]['hash']
            print(f"✅ Uploaded to Facebook: {image_path} (hash: {image_hash})")
            return image_hash
        else:
            print(f"❌ Error uploading {image_path}: {response.text}")
            return None

def assign_images_to_ads(image_hashes):
    """Assign uploaded images to the FOMO ads"""
    # Ad to image mapping
    ad_mappings = {
        'cold': {
            'ads': [
                'FOMO-Cold-47dagen',
                'FOMO-Cold-87procent', 
                'FOMO-Cold-Concurrent',
                'FOMO-Cold-30000weg'
            ],
            'image_hash': image_hashes['cold']
        },
        'warm': {
            'ads': [
                'FOMO-Warm-47dagen',
                'FOMO-Warm-127bedrijven',
                'FOMO-Warm-Collega',
                'FOMO-Warm-Q1weg'
            ],
            'image_hash': image_hashes['warm']
        },
        'hot': {
            'ads': [
                'FOMO-Hot-24uur',
                'FOMO-Hot-Weekend',
                'FOMO-Hot-Analyse',
                'FOMO-Hot-Maandag'
            ],
            'image_hash': image_hashes['hot']
        }
    }
    
    print("\n📎 Image hash mapping for ads:")
    for campaign_type, mapping in ad_mappings.items():
        print(f"\n{campaign_type.upper()} ads use image hash: {mapping['image_hash']}")
        for ad_name in mapping['ads']:
            print(f"  - {ad_name}")

def main():
    print("🎨 CREATING AND UPLOADING FOMO IMAGES")
    print("=" * 60)
    
    # Create images
    print("\n📸 Creating images...")
    cold_image = create_fomo_cold_image()
    warm_image = create_fomo_warm_image()
    hot_image = create_fomo_hot_image()
    
    # Upload to Facebook
    print("\n📤 Uploading to Facebook...")
    image_hashes = {
        'cold': upload_image_to_facebook(cold_image),
        'warm': upload_image_to_facebook(warm_image),
        'hot': upload_image_to_facebook(hot_image)
    }
    
    # Show mapping
    if all(image_hashes.values()):
        assign_images_to_ads(image_hashes)
        
        print("\n✅ SUCCESS! All images uploaded to Facebook")
        print("\n💡 NEXT STEPS:")
        print("1. Go to Ads Manager")
        print("2. Find your FOMO ads")
        print("3. Images should be automatically available")
        print("4. If not, use these image hashes to assign manually")
        
        # Save hashes for reference
        with open('fomo_image_hashes.json', 'w') as f:
            json.dump(image_hashes, f, indent=2)
        print(f"\n📁 Image hashes saved to: fomo_image_hashes.json")
    else:
        print("\n⚠️  Some images failed to upload")
        print("Please check the errors above")

if __name__ == "__main__":
    main()