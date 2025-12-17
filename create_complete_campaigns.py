#!/usr/bin/env python3
"""
Kandidatentekort Complete Campaign Creator with Images
Creates campaigns, ad sets, ads AND uploads images
"""

import argparse
import sys
import os
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class KandidatentekortCompleteCampaigns:
    def __init__(self, access_token, account_id, page_id):
        FacebookAdsApi.init(access_token=access_token)
        self.ad_account = AdAccount(account_id)
        self.account_id = account_id
        self.page_id = page_id
        self.image_hashes = {}
        
    def upload_images(self):
        """Upload campaign images"""
        print(f"\n{Colors.OKBLUE}Uploading Images...{Colors.ENDC}")
        
        # Define image paths - you'll need to provide these
        images = {
            'cold': 'kandidatentekort_cold.jpg',
            'consideration': 'kandidatentekort_consideration.jpg',
            'retargeting': 'kandidatentekort_retargeting.jpg'
        }
        
        # For demo, we'll use a placeholder approach
        # In production, you'd have actual image files
        for key, filename in images.items():
            try:
                # Check if file exists locally
                if os.path.exists(filename):
                    image = AdImage(parent_id=self.account_id)
                    image[AdImage.Field.filename] = filename
                    image.remote_create()
                    self.image_hashes[key] = image[AdImage.Field.hash]
                    print(f"  {Colors.OKGREEN}✓ Uploaded {filename}{Colors.ENDC}")
                else:
                    print(f"  {Colors.WARNING}⚠ Image {filename} not found - ads will be created without images{Colors.ENDC}")
                    self.image_hashes[key] = None
            except Exception as e:
                print(f"  {Colors.FAIL}✗ Error uploading {filename}: {str(e)}{Colors.ENDC}")
                self.image_hashes[key] = None

    def create_complete_campaign(self, campaign_type):
        """Create a complete campaign with ad sets and ads"""
        print(f"\n{Colors.OKBLUE}Creating {campaign_type} Campaign...{Colors.ENDC}")
        
        # Campaign configurations
        configs = {
            'cold': {
                'campaign_name': 'KT25--Traffic--Cold-Awareness--Dec2025',
                'adset_name': 'Cold-Awareness-NL-25-55',
                'daily_budget': 8000,
                'ads': [
                    {
                        'name': 'KT-Cold-Stats-IMG',
                        'headline': '87% van recruiters mist topkandidaten',
                        'description': 'Ontdek hoe jouw vacatures 40-60% meer reacties krijgen. Gratis analyse!',
                        'utm_content': 'cold_stats'
                    },
                    {
                        'name': 'KT-Cold-Problem-IMG',
                        'headline': 'Te weinig goede sollicitaties?',
                        'description': 'Gratis vacature-analyse toont direct verbeterpunten. Start vandaag!',
                        'utm_content': 'cold_problem'
                    },
                    {
                        'name': 'KT-Cold-Solution-IMG',
                        'headline': '40-60% meer sollicitaties gegarandeerd',
                        'description': 'Bewezen methode voor betere vacatureteksten. Vraag je analyse aan!',
                        'utm_content': 'cold_solution'
                    },
                    {
                        'name': 'KT-Cold-Authority-IMG',
                        'headline': '500+ recruiters verbeterden al hun resultaten',
                        'description': 'Krijg direct praktische tips voor jouw vacatures. Gratis quickscan!',
                        'utm_content': 'cold_authority'
                    }
                ]
            },
            'consideration': {
                'campaign_name': 'KT25--Traffic--Consideration--Dec2025',
                'adset_name': 'Consideration-Engaged-NL',
                'daily_budget': 8000,
                'custom_audiences': ['120241125896930536'],  # 30d visitors
                'ads': [
                    {
                        'name': 'KT-Consider-Case-IMG',
                        'headline': 'ASML: Van 12 naar 47 sollicitaties',
                        'description': 'Download de case study en zie hoe zij hun vacatures transformeerden',
                        'utm_content': 'consider_case'
                    },
                    {
                        'name': 'KT-Consider-Features-IMG',
                        'headline': 'AI-analyse + persoonlijk advies',
                        'description': 'Complete vacature-optimalisatie in 24 uur. Bekijk de mogelijkheden!',
                        'utm_content': 'consider_features'
                    },
                    {
                        'name': 'KT-Consider-Compare-IMG',
                        'headline': 'Waarom 73% kiest voor onze methode',
                        'description': 'Vergelijk zelf: traditioneel vs. geoptimaliseerd werven',
                        'utm_content': 'consider_compare'
                    },
                    {
                        'name': 'KT-Consider-ROI-IMG',
                        'headline': '€2.400 bespaard per vacature',
                        'description': 'Bereken jouw potentiële ROI met onze gratis calculator',
                        'utm_content': 'consider_roi'
                    }
                ]
            },
            'retargeting': {
                'campaign_name': 'KT25--Traffic--Retargeting--Dec2025',
                'adset_name': 'Retargeting-Hot-Leads',
                'daily_budget': 8000,
                'custom_audiences': ['120241125897210536', '120241125897460536'],  # 7d + form starters
                'excluded_audiences': ['120241125897870536'],  # converters
                'ads': [
                    {
                        'name': 'KT-Retarget-Ready-IMG',
                        'headline': 'Je vacature-analyse staat klaar',
                        'description': 'Log in en bekijk je persoonlijke verbeterplan + bonus templates',
                        'utm_content': 'retarget_ready'
                    },
                    {
                        'name': 'KT-Retarget-Urgency-IMG',
                        'headline': 'Laatste 48 uur: Gratis quickscan',
                        'description': 'Daarna €97. Claim nu je gratis analyse + implementatieplan',
                        'utm_content': 'retarget_urgency'
                    },
                    {
                        'name': 'KT-Retarget-Social-IMG',
                        'headline': '+127 recruiters deze week',
                        'description': 'Sluit je aan en verbeter je vacatures. Laatste gratis plekken!',
                        'utm_content': 'retarget_social'
                    },
                    {
                        'name': 'KT-Retarget-Bonus-IMG',
                        'headline': 'Extra: Template bibliotheek cadeau',
                        'description': '47 bewezen templates bij aanvraag voor 31 december',
                        'utm_content': 'retarget_bonus'
                    }
                ]
            }
        }
        
        config = configs[campaign_type]
        
        try:
            # Step 1: Create Campaign
            campaign_params = {
                'name': config['campaign_name'],
                'objective': Campaign.Objective.outcome_traffic,
                'status': Campaign.Status.paused,
                'special_ad_categories': [],
                'is_adset_budget_sharing_enabled': False
            }
            
            campaign = self.ad_account.create_campaign(params=campaign_params)
            print(f"  {Colors.OKGREEN}✓ Campaign created: {campaign['id']}{Colors.ENDC}")
            
            # Step 2: Create Ad Set
            targeting = {
                'geo_locations': {'countries': ['NL']},
                'age_min': 25,
                'age_max': 55,
                'targeting_automation': {'advantage_audience': 0}
            }
            
            # Add custom audiences if specified
            if 'custom_audiences' in config:
                targeting['custom_audiences'] = [{'id': aud_id} for aud_id in config['custom_audiences']]
            if 'excluded_audiences' in config:
                targeting['excluded_custom_audiences'] = [{'id': aud_id} for aud_id in config['excluded_audiences']]
            
            adset_params = {
                'name': config['adset_name'],
                'campaign_id': campaign['id'],
                'daily_budget': config['daily_budget'],
                'billing_event': AdSet.BillingEvent.impressions,
                'optimization_goal': AdSet.OptimizationGoal.link_clicks,
                'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                'targeting': targeting,
                'status': AdSet.Status.paused
            }
            
            adset = self.ad_account.create_ad_set(params=adset_params)
            print(f"    {Colors.OKGREEN}✓ Ad Set created: {adset['id']}{Colors.ENDC}")
            
            # Step 3: Create Ads
            for ad_config in config['ads']:
                self.create_complete_ad(adset['id'], campaign_type, ad_config)
                
            return True
            
        except Exception as e:
            print(f"  {Colors.FAIL}✗ Error: {str(e)}{Colors.ENDC}")
            return False

    def create_complete_ad(self, adset_id, campaign_type, ad_config):
        """Create a single ad with image"""
        try:
            # Build URL with UTM
            utm_params = f"utm_source=meta&utm_medium=paid&utm_campaign={campaign_type}&utm_content={ad_config['utm_content']}"
            full_url = f"https://kandidatentekort.nl/?{utm_params}"
            
            # Create creative with image
            creative_params = {
                'name': f"{ad_config['name']}--Creative",
                'object_story_spec': {
                    'page_id': self.page_id,
                    'link_data': {
                        'link': full_url,
                        'name': ad_config['headline'],
                        'message': ad_config['description'],
                        'call_to_action': {
                            'type': 'LEARN_MORE',
                            'value': {'link': full_url}
                        }
                    }
                }
            }
            
            # Add image if available
            if self.image_hashes.get(campaign_type):
                creative_params['object_story_spec']['link_data']['picture'] = \
                    f"https://fb.me/{self.image_hashes[campaign_type]}"
            
            creative = self.ad_account.create_ad_creative(params=creative_params)
            
            # Create ad
            ad_params = {
                'name': ad_config['name'],
                'adset_id': adset_id,
                'creative': {'creative_id': creative['id']},
                'status': Ad.Status.paused
            }
            
            ad = self.ad_account.create_ad(params=ad_params)
            print(f"      {Colors.OKGREEN}✓ Ad created: {ad_config['name']}{Colors.ENDC}")
            
        except Exception as e:
            print(f"      {Colors.FAIL}✗ Ad error ({ad_config['name']}): {str(e)}{Colors.ENDC}")

    def create_all_campaigns(self):
        """Create all three campaigns"""
        print(f"\n{Colors.HEADER}=== KANDIDATENTEKORT COMPLETE CAMPAIGNS ==={Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Creating 3 campaigns, 12 ads total")
        
        # Upload images first
        self.upload_images()
        
        # Create campaigns
        success_count = 0
        for campaign_type in ['cold', 'consideration', 'retargeting']:
            if self.create_complete_campaign(campaign_type):
                success_count += 1
        
        # Summary
        print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
        print(f"{Colors.OKGREEN}Successfully created {success_count}/3 campaigns{Colors.ENDC}")
        
        if success_count == 3:
            print(f"\n{Colors.OKCYAN}✅ ALL DONE! Your campaigns are ready to activate!{Colors.ENDC}")
            print("\nNext steps:")
            print("1. Review ads in Ads Manager")
            print("2. Add/update images if needed")
            print("3. Activate campaigns when ready")
            print("4. Monitor performance in GA4")
        else:
            print(f"\n{Colors.WARNING}⚠ Some campaigns failed. Check errors above.{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='Create Complete Kandidatentekort Campaigns'
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', help='Ad account ID')
    parser.add_argument('--page', default='660118697194302', help='Facebook Page ID')
    
    args = parser.parse_args()
    
    # Security reminder
    print(f"\n{Colors.WARNING}REMINDER:{Colors.ENDC}")
    print("✓ ONLY Kandidatentekort campaigns")
    print("✓ ALL traffic to kandidatentekort.nl")
    print("✓ Using approved audiences only\n")
    
    creator = KandidatentekortCompleteCampaigns(args.token, args.account, args.page)
    creator.create_all_campaigns()

if __name__ == "__main__":
    main()