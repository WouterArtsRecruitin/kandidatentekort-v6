#!/usr/bin/env python3
"""
Complete the FOMO campaigns by adding ad sets and ads
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

# Campaign IDs from previous run
CAMPAIGN_IDS = {
    "cold": "120241127981990536",
    "warm": "120241127982370536",
    "hot": "120241127983150536"
}

# Base URL
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

def create_adset(campaign_id, name, daily_budget, targeting):
    """Create an ad set with fixed targeting"""
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
    print("\n🚀 COMPLETING FOMO CAMPAIGNS")
    print("=" * 60)
    print("Adding ad sets and ads to existing campaigns")
    print("=" * 60)
    
    # Campaign configurations
    configs = {
        "cold": {
            "adset_name": "Cold--DirectePijn--500PerDag",
            "daily_budget": 6000,
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
                },
                {
                    "name": "FOMO-Cold-Concurrent",
                    "headline": "Je concurrent vindt WEL die werkvoorbereider",
                    "primary_text": "Terwijl jij al 2 maanden zoekt. Verschil? Zij gebruiken een bewezen methode.\n\nResultaat: 8-12 goede reacties binnen 3 weken. Gegarandeerd.",
                    "description": "Zie hoe →",
                    "utm_content": "cold_concurrent"
                },
                {
                    "name": "FOMO-Cold-30000weg",
                    "headline": "2 maanden zoeken = €30.000 verdampt",
                    "primary_text": "€500 per dag x 60 dagen = €30.000 aan gemiste omzet.\n\nStop het bloeden. Andere productiebedrijven vinden binnen 3 weken.",
                    "description": "Start vandaag →",
                    "utm_content": "cold_30000"
                }
            ]
        },
        "warm": {
            "adset_name": "Warm--127Bedrijven--Urgency",
            "daily_budget": 6000,
            "targeting": {
                "geo_locations": {"countries": ["NL"]},
                "age_min": 25,
                "age_max": 55,
                "targeting_automation": {"advantage_audience": 0}
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
                },
                {
                    "name": "FOMO-Warm-Collega",
                    "headline": "Je collega's vullen hun vacatures WEL",
                    "primary_text": "Metaalbewerker Overijssel: 3 weken\nMachinebouwer Gelderland: 18 dagen\nProductiebedrijf Brabant: 21 dagen\n\nJij? Al 8 weken bezig...",
                    "description": "Wat doen zij anders? →",
                    "utm_content": "warm_collega"
                },
                {
                    "name": "FOMO-Warm-Q1weg",
                    "headline": "Q1 2025 al €45.000 aan recruitment",
                    "primary_text": "En nog steeds 3 vacatures open. Dit kan anders.\n\nOnze methode: €297 per vacature. Geen %. Geen verrassingen.\n\n93% vindt binnen 4 weken.",
                    "description": "Bereken je besparing →",
                    "utm_content": "warm_q1"
                }
            ]
        },
        "hot": {
            "adset_name": "Hot--24Uur--LastChance",
            "daily_budget": 6000,
            "targeting": {
                "geo_locations": {"countries": ["NL"]},
                "age_min": 25,
                "age_max": 55,
                "targeting_automation": {"advantage_audience": 0}
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
                },
                {
                    "name": "FOMO-Hot-Analyse",
                    "headline": "Je analyse is bijna verlopen",
                    "primary_text": "Gisteren gemaakt. Morgen weg.\n\n5 concrete tips voor jouw werkvoorbereider vacature. Normaal €297.\n\nNu nog gratis.",
                    "description": "Download nu →",
                    "utm_content": "hot_analyse"
                },
                {
                    "name": "FOMO-Hot-Maandag",
                    "headline": "Maandag weer beginnen met zoeken?",
                    "primary_text": "Of maandag 8 sollicitaties in je inbox?\n\n93% van onze klanten heeft binnen 72 uur eerste reacties.\n\nLaatste kans dit weekend. Gratis.",
                    "description": "Start het weekend goed →",
                    "utm_content": "hot_maandag"
                }
            ]
        }
    }
    
    # Create ad sets and ads for each campaign
    for key, campaign_id in CAMPAIGN_IDS.items():
        config = configs[key]
        print(f"\n📍 Completing {key.upper()} campaign (ID: {campaign_id})...")
        
        # Create ad set
        adset_id = create_adset(
            campaign_id,
            config["adset_name"],
            config["daily_budget"],
            config["targeting"]
        )
        
        if adset_id:
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
    
    print(f"\n{'='*60}")
    print(f"✅ FOMO campaigns completed!")
    print(f"\n💡 NEXT STEPS:")
    print(f"1. Go to Facebook Ads Manager")
    print(f"2. Add images to the ads")
    print(f"3. Review all settings")
    print(f"4. Activate campaigns when ready!")
    print(f"\nTotal budget: €180/day (€60 per campaign)")
    print(f"Focus: €500/day loss messaging with urgency")

if __name__ == "__main__":
    main()