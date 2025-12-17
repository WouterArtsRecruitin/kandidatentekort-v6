#!/usr/bin/env python3
"""
Kandidatentekort FOMO Campaign Creator
Creates 3 NEW campaigns with €500/day messaging
"""

import json
import requests
from datetime import datetime

# Configuration
ACCESS_TOKEN = "EAAYqzG39fnoBQI36ltDvwpuGHU9TJpa6DSe4ZCr5Twrv6nHGwdOQnOVEtXez6Md7lYFTdsPq3ZA9IWjAU49eXcGmtDrA6GdiicwT5faw4vHQqWcg5q2Eof5AN3naiBXBueSE7RBbMIrdxvYjpu7t0TOahFDDkruV1DTUkTrsv5H6oZCkqn1F2UPAsZB0yQ83sVpe2Y2unEFoapJRSJssZCfpKuGb0NK5bT27VdS22rYmnMZAGgbCIKqer8keYj4t9stUqDh1tpObdOZBoIWFc2eZCCvVzrZC3"
AD_ACCOUNT_ID = "act_1236576254450117"
PAGE_ID = "660118697194302"
PIXEL_ID = "1430141541402009"
API_VERSION = "v18.0"

# Base URL
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_campaign(name, objective="OUTCOME_LEADS"):
    """Create a campaign"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    
    data = {
        "name": name,
        "objective": objective,
        "status": "PAUSED",
        "special_ad_categories": []
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        campaign_id = response.json()["id"]
        print(f"✅ Campaign created: {name} (ID: {campaign_id})")
        return campaign_id
    else:
        print(f"❌ Error creating campaign: {response.text}")
        return None

def create_adset(campaign_id, name, daily_budget, targeting):
    """Create an ad set"""
    url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adsets"
    
    data = {
        "name": name,
        "campaign_id": campaign_id,
        "daily_budget": daily_budget,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "OFFSITE_CONVERSIONS",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "targeting": targeting,
        "promoted_object": {
            "pixel_id": PIXEL_ID,
            "custom_event_type": "COMPLETE_REGISTRATION"
        },
        "status": "PAUSED"
    }
    
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        adset_id = response.json()["id"]
        print(f"  ✅ Ad Set created: {name} (ID: {adset_id})")
        return adset_id
    else:
        print(f"  ❌ Error creating ad set: {response.text}")
        return None

def create_ad(adset_id, name, headline, primary_text, description, utm_content):
    """Create an ad"""
    # First create the creative
    creative_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    
    link = f"https://kandidatentekort.nl/gratis-analyse?utm_source=facebook&utm_medium=paid&utm_campaign=fomo_{utm_content}&utm_content={utm_content}"
    
    creative_data = {
        "name": f"{name}_creative",
        "object_story_spec": {
            "page_id": PAGE_ID,
            "link_data": {
                "link": link,
                "name": headline,
                "message": primary_text,
                "description": description,
                "call_to_action": {
                    "type": "LEARN_MORE",
                    "value": {"link": link}
                }
            }
        }
    }
    
    response = requests.post(creative_url, json=creative_data, headers=headers)
    if response.status_code == 200:
        creative_id = response.json()["id"]
        
        # Now create the ad
        ad_url = f"{BASE_URL}/{AD_ACCOUNT_ID}/ads"
        ad_data = {
            "name": name,
            "adset_id": adset_id,
            "creative": {"creative_id": creative_id},
            "status": "PAUSED"
        }
        
        response = requests.post(ad_url, json=ad_data, headers=headers)
        if response.status_code == 200:
            ad_id = response.json()["id"]
            print(f"    ✅ Ad created: {name}")
            return ad_id
        else:
            print(f"    ❌ Error creating ad: {response.text}")
    else:
        print(f"    ❌ Error creating creative: {response.text}")
    
    return None

def main():
    print("\n🚀 KANDIDATENTEKORT FOMO CAMPAIGN CREATOR")
    print("=" * 60)
    print(f"Creating 3 NEW campaigns with €500/day messaging")
    print(f"Total budget: €180/day (€60 per campaign)")
    print("=" * 60)
    
    # Campaign configurations
    campaigns = {
        "cold": {
            "campaign_name": "KT25--FOMO--Cold--500PerDag",
            "adset_name": "Cold--DirectePijn--500PerDag",
            "daily_budget": 6000,  # €60 in cents
            "targeting": {
                "geo_locations": {"countries": ["NL"]},
                "age_min": 25,
                "age_max": 55,
                "targeting_automation": {"advantage_audience": 0}
            },
            "ads": [
                {
                    "name": "FOMO-Cold-47dagen",
                    "headline": "Werkvoorbereider gezocht? Al 8 weken?",
                    "primary_text": "Elke week kost je €3.500 aan gemiste productie. Dat is al €28.000.\n\nMachinebouwer Arnhem had hetzelfde probleem. Nu opgelost. In 3 weken.",
                    "description": "Bekijk hun aanpak →",
                    "utm_content": "cold_47dagen"
                },
                {
                    "name": "FOMO-Cold-87procent",
                    "headline": "We vinden gewoon niemand",
                    "primary_text": "Klopt. 87% krijgt 0 goede reacties. Kost gemiddeld €45.000 per vacature.\n\nDe andere 13% doet iets anders. Simpel. Effectief. Zonder bureau.",
                    "description": "Ontdek wat →",
                    "utm_content": "cold_87procent"
                }
            ]
        },
        "warm": {
            "campaign_name": "KT25--FOMO--Warm--Urgency",
            "adset_name": "Warm--127Bedrijven--Urgency",
            "daily_budget": 6000,
            "targeting": {
                "geo_locations": {"countries": ["NL"]},
                "age_min": 25,
                "age_max": 55,
                "targeting_automation": {"advantage_audience": 0},
                "custom_audiences": [
                    {"id": "120241125896930536"},  # 30d visitors
                    {"id": "120241125897210536"}   # 7d visitors
                ]
            },
            "ads": [
                {
                    "name": "FOMO-Warm-47dagen",
                    "headline": "Die lastige vacature... 47 dagen al?",
                    "primary_text": "€500 per dag verlies = €23.500 weg. En het wordt alleen maar meer.\n\nDeze week: 12 bedrijven geholpen. Gemiddeld 9 reacties. Binnen 3 weken.",
                    "description": "Check of wij jou kunnen helpen →",
                    "utm_content": "warm_47dagen"
                },
                {
                    "name": "FOMO-Warm-127bedrijven",
                    "headline": "Nog steeds aan het zoeken?",
                    "primary_text": "Deze week al 127 bedrijven geholpen:\n✓ Maintenance Engineer - 11 reacties\n✓ Projectleider - binnen 18 dagen\n✓ Calculator - 8 goede CV's\n\nZonder bureau. Voor €297.",
                    "description": "Nog 3 plekken deze week →",
                    "utm_content": "warm_127bedrijven"
                }
            ]
        },
        "hot": {
            "campaign_name": "KT25--FOMO--Hot--LastChance",
            "adset_name": "Hot--24Uur--LastChance",
            "daily_budget": 6000,
            "targeting": {
                "geo_locations": {"countries": ["NL"]},
                "age_min": 25,
                "age_max": 55,
                "targeting_automation": {"advantage_audience": 0},
                "custom_audiences": [
                    {"id": "120241125897210536"},  # 7d visitors
                    {"id": "120241125897460536"}   # Form starters
                ],
                "excluded_custom_audiences": [
                    {"id": "120241125897870536"}   # Converters
                ]
            },
            "ads": [
                {
                    "name": "FOMO-Hot-24uur",
                    "headline": "⚠️ Je gratis vacature-analyse",
                    "primary_text": "Die staat nog 24 uur klaar. Daarna betaal je €297.\n\nOf... blijf nog 60 dagen zoeken. Kost je €30.000 (€500/dag).\n\nJouw keuze. Tiktak.",
                    "description": "Claim nu (€0) →",
                    "utm_content": "hot_24uur"
                },
                {
                    "name": "FOMO-Hot-Weekend",
                    "headline": "Weekend = €1.000 weg",
                    "primary_text": "2 dagen x €500 = €1.000 aan die openstaande functie.\n\nOf: Gebruik onze gratis analyse. Begin maandag met 5-10 reacties.\n\n⏰ Nog 3 uur gratis. 127 bedrijven gingen je voor.",
                    "description": "Wees #128 →",
                    "utm_content": "hot_weekend"
                }
            ]
        }
    }
    
    # Create campaigns
    created_count = 0
    for key, config in campaigns.items():
        print(f"\n📍 Creating {key.upper()} campaign...")
        
        # Create campaign
        campaign_id = create_campaign(config["campaign_name"])
        if not campaign_id:
            continue
            
        # Create ad set
        adset_id = create_adset(
            campaign_id,
            config["adset_name"],
            config["daily_budget"],
            config["targeting"]
        )
        if not adset_id:
            continue
            
        # Create ads
        for ad in config["ads"]:
            create_ad(
                adset_id,
                ad["name"],
                ad["headline"],
                ad["primary_text"],
                ad["description"],
                ad["utm_content"]
            )
        
        created_count += 1
    
    print(f"\n{'='*60}")
    print(f"✅ SUMMARY: Created {created_count}/3 FOMO campaigns")
    print(f"\n💡 NEXT STEPS:")
    print(f"1. Go to Facebook Ads Manager")
    print(f"2. Review the 3 new FOMO campaigns")
    print(f"3. Add images to ads")
    print(f"4. Activate when ready!")
    print(f"\n🎯 These campaigns focus on €500/day loss messaging")
    print(f"and run alongside your existing campaigns.")

if __name__ == "__main__":
    main()