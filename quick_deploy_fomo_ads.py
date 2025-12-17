#!/usr/bin/env python3
"""
Quick Deploy FOMO Ads - Kandidatentekort
Rapid deployment of €500/day loss messaging across campaigns
"""

import requests
import json
from datetime import datetime

# Configuration
ACCESS_TOKEN = "EAAYqzG39fnoBQI36ltDvwpuGHU9TJpa6DSe4ZCr5Twrv6nHGwdOQnOVEtXez6Md7lYFTdsPq3ZA9IWjAU49eXcGmtDrA6GdiicwT5faw4vHQqWcg5q2Eof5AN3naiBXBueSE7RBbMIrdxvYjpu7t0TOahFDDkruV1DTUkTrsv5H6oZCkqn1F2UPAsZB0yQ83sVpe2Y2unEFoapJRSJssZCfpKuGb0NK5bT27VdS22rYmnMZAGgbCIKqer8keYj4t9stUqDh1tpObdOZBoIWFc2eZCCvVzrZC3"
AD_ACCOUNT_ID = "act_1236576254450117"
PAGE_ID = "660118697194302"
API_VERSION = "v18.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

def create_fomo_ad(adset_id, ad_name, headline, primary_text, description, utm_content):
    """Create a single FOMO ad"""
    
    # Build UTM URL
    utm_params = f"utm_source=meta&utm_medium=paid&utm_campaign=kt_fomo_dec2024&utm_content={utm_content}"
    landing_url = f"https://kandidatentekort.nl/?{utm_params}"
    
    # Create Ad Creative
    creative_data = {
        "name": f"{ad_name}_Creative",
        "object_story_spec": json.dumps({
            "page_id": PAGE_ID,
            "link_data": {
                "link": landing_url,
                "name": headline,
                "message": primary_text,
                "description": description,
                "call_to_action": {
                    "type": "LEARN_MORE"
                }
            }
        }),
        "access_token": ACCESS_TOKEN
    }
    
    creative_response = requests.post(
        f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives",
        data=creative_data
    )
    
    if creative_response.status_code != 200:
        print(f"❌ Failed to create creative: {creative_response.text}")
        return None
    
    creative_id = creative_response.json()['id']
    
    # Create Ad
    ad_data = {
        "name": ad_name,
        "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",
        "access_token": ACCESS_TOKEN
    }
    
    ad_response = requests.post(
        f"{BASE_URL}/{AD_ACCOUNT_ID}/ads",
        data=ad_data
    )
    
    if ad_response.status_code == 200:
        print(f"✅ Created: {ad_name}")
        return ad_response.json()['id']
    else:
        print(f"❌ Failed to create ad: {ad_response.text}")
        return None

def deploy_fomo_campaign():
    """Deploy all FOMO ads quickly"""
    
    print("\n🚀 KANDIDATENTEKORT FOMO ADS - QUICK DEPLOY")
    print("="*50)
    print("Strategy: €500/day loss messaging")
    print("Focus: Direct pain points + urgency\n")
    
    # Define your ad sets here (get these from Ads Manager)
    adsets = {
        "cold": "YOUR_COLD_ADSET_ID",  # Replace with actual ID
        "warm": "YOUR_WARM_ADSET_ID",  # Replace with actual ID
        "hot": "YOUR_HOT_ADSET_ID"     # Replace with actual ID
    }
    
    # FOMO Ad Copies - Direct and Hard-Hitting
    fomo_ads = {
        "cold": [
            {
                "name": "FOMO_Cold_500EUR_Daily",
                "headline": "Jouw vacature kost je €500 per dag",
                "primary_text": "Elke dag zonder de juiste kandidaat kost je €500+. Productieverlies, overwerk, gemiste deadlines. Stop het bloeden. Gratis analyse toont in 24 uur wat er mis is.",
                "description": "Ontdek waarom kandidaten niet reageren. 100% gratis.",
                "utm_content": "fomo_500eur"
            },
            {
                "name": "FOMO_Cold_Competitors",
                "headline": "Concurrenten stelen JOUW kandidaten",
                "primary_text": "Terwijl jij wacht, werven zij. 150+ bedrijven verbeterden hun vacatures en kregen 40-60% meer reacties. Jij blijft achter.",
                "description": "Krijg direct inzicht. Gratis quickscan beschikbaar.",
                "utm_content": "fomo_competitors"
            }
        ],
        "warm": [
            {
                "name": "FOMO_Warm_LastChance",
                "headline": "Laatste 48 uur: Gratis analyse",
                "primary_text": "Je hebt onze site bezocht. Je kent het probleem. Vanaf vrijdag kost deze analyse €297. Grijp nu je kans.",
                "description": "127 bedrijven gingen je voor deze week. Nu jij.",
                "utm_content": "fomo_lastchance"
            },
            {
                "name": "FOMO_Warm_Calculator",
                "headline": "€847/dag kwijt aan open vacature",
                "primary_text": "Reken maar uit: €500 productiviteit + €247 overwerk + €100 deadlines = €847 per dag. Check wat jouw vacature je kost.",
                "description": "Schrikken? Wij lossen het op. Start vandaag.",
                "utm_content": "fomo_calculator"
            }
        ],
        "hot": [
            {
                "name": "FOMO_Hot_Expires",
                "headline": "Je analyse vervalt over 24 uur",
                "primary_text": "We reserveerden een gratis plek voor je. Over 24 uur gaat deze naar #128 op de wachtlijst. Jouw keuze.",
                "description": "Log in en claim je analyse + actieplan. NU.",
                "utm_content": "fomo_expires"
            },
            {
                "name": "FOMO_Hot_Final",
                "headline": "Dit is je laatste kans",
                "primary_text": "Je vacature blijft €500/dag kosten. Wij kunnen het stoppen. 150+ bedrijven gingen je voor. Wat houdt je tegen?",
                "description": "Gratis analyse + implementatieplan. Laatste kans.",
                "utm_content": "fomo_final"
            }
        ]
    }
    
    # Deploy ads
    created_count = 0
    for audience, adset_id in adsets.items():
        print(f"\n📍 Deploying {audience.upper()} ads...")
        
        if adset_id == f"YOUR_{audience.upper()}_ADSET_ID":
            print(f"⚠️  Please update the adset ID for {audience} audience")
            continue
            
        for ad in fomo_ads[audience]:
            ad_id = create_fomo_ad(
                adset_id,
                ad["name"],
                ad["headline"],
                ad["primary_text"],
                ad["description"],
                ad["utm_content"]
            )
            if ad_id:
                created_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"✅ DEPLOYMENT COMPLETE")
    print(f"{'='*50}")
    print(f"Created: {created_count} FOMO ads")
    print(f"Status: PAUSED (ready for review)")
    print(f"\n📋 Next Steps:")
    print("1. Go to Meta Ads Manager")
    print("2. Review ad creatives")
    print("3. Set budget distribution (even split for A/B test)")
    print("4. Activate when ready")
    print("\n💡 Pro tip: Start with €80/day total, €20 per ad variant")

if __name__ == "__main__":
    # First, get your ad set IDs
    print("\n🔍 First, let's find your ad set IDs...")
    print(f"\nGetting campaigns from account {AD_ACCOUNT_ID}...")
    
    # Get campaigns
    campaigns_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        "fields": "id,name,status",
        "filtering": json.dumps([{"field": "name", "operator": "CONTAIN", "value": "KT"}]),
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.get(campaigns_url, params=params)
    
    if response.status_code == 200:
        campaigns = response.json().get('data', [])
        print(f"\nFound {len(campaigns)} Kandidatentekort campaigns:")
        
        for campaign in campaigns:
            print(f"\nCampaign: {campaign['name']} (ID: {campaign['id']})")
            
            # Get ad sets for this campaign
            adsets_url = f"{BASE_URL}/{campaign['id']}/adsets"
            adsets_params = {
                "fields": "id,name,daily_budget",
                "access_token": ACCESS_TOKEN
            }
            
            adsets_response = requests.get(adsets_url, params=adsets_params)
            
            if adsets_response.status_code == 200:
                adsets = adsets_response.json().get('data', [])
                for adset in adsets:
                    budget = int(adset.get('daily_budget', 0)) / 100
                    print(f"  └─ AdSet: {adset['name']} (ID: {adset['id']}) - €{budget}/day")
            
        print("\n⚠️  Update the adset IDs in the script with the IDs above, then run again.")
    else:
        print(f"❌ Error getting campaigns: {response.text}")
        
    # Uncomment this line after updating the adset IDs:
    # deploy_fomo_campaign()