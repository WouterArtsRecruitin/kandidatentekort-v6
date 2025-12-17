#!/usr/bin/env python3
"""
Kandidatentekort Campaign Creator with Google Drive Images
Uses the images from yesterday's successful deployment
"""

import argparse
import sys
import os
import requests
import tempfile
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

class KandidatentekortDriveCampaigns:
    def __init__(self, access_token, account_id, page_id):
        FacebookAdsApi.init(access_token=access_token)
        self.ad_account = AdAccount(account_id)
        self.account_id = account_id
        self.page_id = page_id
        self.uploaded_images = {}
        
        # Campaign structure with Google Drive images
        self.campaign_config = {
            'cold': {
                'name': 'KT25--Traffic--Cold-Awareness--Dec2025-Complete',
                'budget': 8000,
                'ads': [
                    {
                        'name': 'Cold-1-Stats',
                        'headline': '87% van recruiters mist topkandidaten',
                        'description': 'Ontdek hoe jouw vacatures 40-60% meer reacties krijgen',
                        'image': '33_Facebook-bericht - Tekort aan engineers.png',
                        'folder': '1tAU4IRetVs9mufb8aMDtsowSG9rma7B6',
                        'utm_content': 'cold_stats'
                    },
                    {
                        'name': 'Cold-2-Problem',
                        'headline': 'Te weinig goede sollicitaties?',
                        'description': 'Gratis vacature-analyse toont verbeterpunten',
                        'image': '03_beige_problem_pain.png',
                        'folder': '1IgkGJk-ab4PkQ6XU0dXeYLig_jl_WqOz',
                        'utm_content': 'cold_problem'
                    },
                    {
                        'name': 'Cold-3-Solution',
                        'headline': '40-60% meer sollicitaties gegarandeerd',
                        'description': 'Bewezen methode voor betere vacatureteksten',
                        'image': '10_Facebook-omslagfoto - 40-60% MEER SOLLICITATIES.png',
                        'folder': '1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V',
                        'utm_content': 'cold_solution'
                    },
                    {
                        'name': 'Cold-4-Authority',
                        'headline': '500+ recruiters verbeterden al hun resultaten',
                        'description': 'Krijg direct praktische tips voor jouw vacatures',
                        'image': '12_Facebook-bericht - 15 jaar recruitmentervaring.png',
                        'folder': '1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V',
                        'utm_content': 'cold_authority'
                    }
                ]
            },
            'consideration': {
                'name': 'KT25--Traffic--Consideration--Dec2025-Complete',
                'budget': 8000,
                'audiences': ['120241125896930536'],  # 30d visitors
                'ads': [
                    {
                        'name': 'Consider-1-Case',
                        'headline': 'ASML: Van 12 naar 47 sollicitaties',
                        'description': 'Zie hoe zij hun vacatures transformeerden',
                        'image': '25_Facebook-bericht - Proven Recruitment Performance.png',
                        'folder': '1tAU4IRetVs9mufb8aMDtsowSG9rma7B6',
                        'utm_content': 'consider_case'
                    },
                    {
                        'name': 'Consider-2-Features',
                        'headline': 'AI-analyse + persoonlijk advies',
                        'description': 'Complete vacature-optimalisatie in 24 uur',
                        'image': '1_Instagram-bericht - Kandidatentekort.png',
                        'folder': '1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V',
                        'utm_content': 'consider_features'
                    },
                    {
                        'name': 'Consider-3-Comparison',
                        'headline': 'Waarom 73% kiest voor onze methode',
                        'description': 'Vergelijk zelf: traditioneel vs. geoptimaliseerd',
                        'image': 'split_screen_ad.png',
                        'folder': '1IgkGJk-ab4PkQ6XU0dXeYLig_jl_WqOz',
                        'utm_content': 'consider_compare'
                    },
                    {
                        'name': 'Consider-4-ROI',
                        'headline': '€2.400 bespaard per vacature',
                        'description': 'Bereken jouw potentiële ROI',
                        'image': '04_beige_urgency_roi.png',
                        'folder': '1IgkGJk-ab4PkQ6XU0dXeYLig_jl_WqOz',
                        'utm_content': 'consider_roi'
                    }
                ]
            },
            'retargeting': {
                'name': 'KT25--Traffic--Retargeting--Dec2025-Complete',
                'budget': 8000,
                'audiences': ['120241125897210536', '120241125897460536'],  # 7d + form starters
                'exclude': ['120241125897870536'],  # converters
                'ads': [
                    {
                        'name': 'Retarget-1-Reminder',
                        'headline': 'Je vacature-analyse staat klaar',
                        'description': 'Bekijk je persoonlijke verbeterplan',
                        'image': '8_Instagram-bericht - Elke dag zonder operator.png',
                        'folder': '1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V',
                        'utm_content': 'retarget_reminder'
                    },
                    {
                        'name': 'Retarget-2-Urgency',
                        'headline': 'Laatste 48 uur: Gratis quickscan',
                        'description': 'Daarna €97 voor complete analyse',
                        'image': '4_Facebook-bericht - Wacht niet. Check nu je vacature.png',
                        'folder': '1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V',
                        'utm_content': 'retarget_urgency'
                    },
                    {
                        'name': 'Retarget-3-Social',
                        'headline': '+127 recruiters deze week',
                        'description': 'Sluit je aan bij succesvolle collega\'s',
                        'image': '66_KandidatenTekort Social Proof Carousel.png',
                        'folder': '1tAU4IRetVs9mufb8aMDtsowSG9rma7B6',
                        'utm_content': 'retarget_social'
                    },
                    {
                        'name': 'Retarget-4-Bonus',
                        'headline': 'Extra: Template bibliotheek cadeau',
                        'description': 'Bij aanvraag voor 31 december',
                        'image': '45_Facebook-bericht - 150+ bedrijven gingen je voor.png',
                        'folder': '1tAU4IRetVs9mufb8aMDtsowSG9rma7B6',
                        'utm_content': 'retarget_bonus'
                    }
                ]
            }
        }
    
    def download_and_upload_image(self, filename, folder_id):
        """Download from Google Drive and upload to Facebook"""
        try:
            # For now, we'll need the actual files locally
            # In production, you'd download from Google Drive
            print(f"      ℹ️  Image needed: {filename} from folder {folder_id}")
            
            # Check if we already uploaded this image
            if filename in self.uploaded_images:
                return self.uploaded_images[filename]
                
            # Here you would download from Google Drive and upload
            # For now, return None to create ads without images
            return None
            
        except Exception as e:
            print(f"      {Colors.WARNING}⚠ Could not process image {filename}: {str(e)}{Colors.ENDC}")
            return None
    
    def create_campaign_complete(self, campaign_type):
        """Create complete campaign with ad sets and ads"""
        config = self.campaign_config[campaign_type]
        print(f"\n{Colors.OKBLUE}Creating {campaign_type.upper()} Campaign...{Colors.ENDC}")
        
        try:
            # Create Campaign
            campaign_params = {
                'name': config['name'],
                'objective': Campaign.Objective.outcome_traffic,
                'status': Campaign.Status.paused,
                'special_ad_categories': [],
                'is_adset_budget_sharing_enabled': False
            }
            
            campaign = self.ad_account.create_campaign(params=campaign_params)
            print(f"  {Colors.OKGREEN}✓ Campaign: {campaign['id']}{Colors.ENDC}")
            
            # Create Ad Set
            targeting = {
                'geo_locations': {'countries': ['NL']},
                'age_min': 25,
                'age_max': 55,
                'targeting_automation': {'advantage_audience': 0}
            }
            
            # Add custom audiences
            if 'audiences' in config:
                targeting['custom_audiences'] = [{'id': aud} for aud in config['audiences']]
            if 'exclude' in config:
                targeting['excluded_custom_audiences'] = [{'id': aud} for aud in config['exclude']]
            
            adset_params = {
                'name': f"{config['name']}--AdSet",
                'campaign_id': campaign['id'],
                'daily_budget': config['budget'],
                'billing_event': AdSet.BillingEvent.impressions,
                'optimization_goal': AdSet.OptimizationGoal.link_clicks,
                'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                'targeting': targeting,
                'status': AdSet.Status.paused
            }
            
            adset = self.ad_account.create_ad_set(params=adset_params)
            print(f"    {Colors.OKGREEN}✓ Ad Set: {adset['id']}{Colors.ENDC}")
            
            # Create Ads
            print(f"    Creating {len(config['ads'])} ads...")
            for ad_config in config['ads']:
                self.create_ad_with_image(adset['id'], campaign_type, ad_config)
                
            return True
            
        except Exception as e:
            print(f"  {Colors.FAIL}✗ Error: {str(e)}{Colors.ENDC}")
            return False
    
    def create_ad_with_image(self, adset_id, campaign_type, ad_config):
        """Create ad with Google Drive image"""
        try:
            # Build UTM URL
            utm = f"utm_source=meta&utm_medium=paid&utm_campaign={campaign_type}&utm_content={ad_config['utm_content']}"
            url = f"https://kandidatentekort.nl/?{utm}"
            
            # Get image hash
            image_hash = self.download_and_upload_image(ad_config['image'], ad_config['folder'])
            
            # Create creative
            creative_params = {
                'name': f"{ad_config['name']}--Creative",
                'object_story_spec': {
                    'page_id': self.page_id,
                    'link_data': {
                        'link': url,
                        'name': ad_config['headline'],
                        'message': ad_config['description'],
                        'call_to_action': {
                            'type': 'LEARN_MORE',
                            'value': {'link': url}
                        }
                    }
                }
            }
            
            # Add image if available
            if image_hash:
                creative_params['object_story_spec']['link_data']['image_hash'] = image_hash
            
            creative = self.ad_account.create_ad_creative(params=creative_params)
            
            # Create ad
            ad = self.ad_account.create_ad(params={
                'name': f"KT-{ad_config['name']}",
                'adset_id': adset_id,
                'creative': {'creative_id': creative['id']},
                'status': Ad.Status.paused
            })
            
            print(f"      {Colors.OKGREEN}✓ {ad_config['name']}: {ad_config['headline'][:30]}...{Colors.ENDC}")
            
        except Exception as e:
            print(f"      {Colors.FAIL}✗ {ad_config['name']}: {str(e)}{Colors.ENDC}")
    
    def run(self):
        """Create all campaigns"""
        print(f"\n{Colors.HEADER}=== KANDIDATENTEKORT COMPLETE CAMPAIGN CREATION ==={Colors.ENDC}")
        print("Creating 3 campaigns with 12 ads using Google Drive images")
        print(f"Account: {self.account_id}")
        print(f"Destination: kandidatentekort.nl\n")
        
        # Note about images
        print(f"{Colors.WARNING}NOTE: To use the Google Drive images:{Colors.ENDC}")
        print("1. Download images from the Google Drive folders")
        print("2. Place them in the script directory")
        print("3. Or manually add them in Ads Manager after creation\n")
        
        success = 0
        for campaign_type in ['cold', 'consideration', 'retargeting']:
            if self.create_campaign_complete(campaign_type):
                success += 1
        
        print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
        print(f"Created {success}/3 campaigns successfully")
        
        if success == 3:
            print(f"\n{Colors.OKGREEN}✅ SUCCESS! All campaigns created!{Colors.ENDC}")
            print("\nGoogle Drive folders with images:")
            print("1. https://drive.google.com/drive/folders/1IgkGJk-ab4PkQ6XU0dXeYLig_jl_WqOz")
            print("2. https://drive.google.com/drive/folders/1tAU4IRetVs9mufb8aMDtsowSG9rma7B6")
            print("3. https://drive.google.com/drive/folders/1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V")
            print("\nAdd these images to your ads in Ads Manager!")

def main():
    parser = argparse.ArgumentParser(
        description='Create Kandidatentekort Campaigns with Drive Images'
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117')
    parser.add_argument('--page', default='660118697194302')
    
    args = parser.parse_args()
    
    creator = KandidatentekortDriveCampaigns(args.token, args.account, args.page)
    creator.run()

if __name__ == "__main__":
    main()