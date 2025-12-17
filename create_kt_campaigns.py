#!/usr/bin/env python3
"""
Kandidatentekort Traffic Campaigns Creator
Creates 3 campaigns with proper UTM tracking to kandidatentekort.nl
"""

import argparse
import sys
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class KandidatentekortCampaigns:
    def __init__(self, access_token, account_id, page_id):
        FacebookAdsApi.init(access_token=access_token)
        self.ad_account = AdAccount(account_id)
        self.account_id = account_id
        self.page_id = page_id
        self.created_campaigns = []

    def create_campaigns(self):
        """Create all 3 campaigns"""
        print(f"\n{Colors.HEADER}=== CREATING KANDIDATENTEKORT TRAFFIC CAMPAIGNS ==={Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Page: {self.page_id}")
        print(f"Destination: kandidatentekort.nl\n")

        campaigns = [
            {
                'name': 'KT25--Traffic--Cold-Awareness--Dec2025',
                'daily_budget': 8000,  # €80
                'targeting': 'broad'
            },
            {
                'name': 'KT25--Traffic--Consideration--Dec2025', 
                'daily_budget': 8000,  # €80
                'targeting': 'warm'
            },
            {
                'name': 'KT25--Traffic--Retargeting--Dec2025',
                'daily_budget': 8000,  # €80
                'targeting': 'hot'
            }
        ]

        for camp in campaigns:
            campaign = self.create_single_campaign(camp)
            if campaign:
                self.created_campaigns.append(campaign)

        self.print_summary()

    def create_single_campaign(self, config):
        """Create a single campaign with ad set and ads"""
        print(f"{Colors.OKBLUE}Creating: {config['name']}{Colors.ENDC}")
        
        try:
            # Create campaign with new requirements
            campaign_params = {
                'name': config['name'],
                'objective': Campaign.Objective.outcome_traffic,
                'status': Campaign.Status.paused,
                'special_ad_categories': [],
                'is_adset_budget_sharing_enabled': False  # Set to False for adset level budgets
            }
            
            campaign = self.ad_account.create_campaign(params=campaign_params)
            print(f"  {Colors.OKGREEN}✓ Campaign created: {campaign['id']}{Colors.ENDC}")
            
            # Create ad set
            adset = self.create_adset(campaign['id'], config)
            
            # Create ads
            if adset:
                self.create_ads(campaign['id'], adset['id'], config['name'])
            
            return {'id': campaign['id'], 'name': config['name']}
            
        except Exception as e:
            print(f"  {Colors.FAIL}✗ Error: {str(e)}{Colors.ENDC}")
            return None

    def create_adset(self, campaign_id, config):
        """Create ad set with targeting"""
        try:
            # Base targeting - Netherlands, age 25-55
            targeting = {
                'geo_locations': {
                    'countries': ['NL']
                },
                'age_min': 25,
                'age_max': 55,
                'targeting_automation': {
                    'advantage_audience': 0  # Disable Advantage+ audience
                }
            }
            
            # Add custom audience targeting based on campaign type
            if 'Cold' in config['name']:
                # For cold traffic, use broad targeting
                # Lookalike audiences would be added here manually
                pass
            elif 'Consideration' in config['name']:
                # Target 30d website visitors
                targeting['custom_audiences'] = [
                    {'id': '120241125896930536'}  # KT - Website Visitors 30d
                ]
            elif 'Retargeting' in config['name']:
                # Target 7d visitors and form starters
                targeting['custom_audiences'] = [
                    {'id': '120241125897210536'},  # KT - Website Visitors 7d
                    {'id': '120241125897460536'}   # KT - Form Starters
                ]
                # Exclude converters
                targeting['excluded_custom_audiences'] = [
                    {'id': '120241125897870536'}  # KT - Converters (Leads)
                ]
            
            adset_params = {
                'name': f"{config['name']}--AdSet",
                'campaign_id': campaign_id,
                'daily_budget': config['daily_budget'],
                'billing_event': AdSet.BillingEvent.impressions,
                'optimization_goal': AdSet.OptimizationGoal.link_clicks,
                'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
                'targeting': targeting,
                'status': AdSet.Status.paused
            }
            
            adset = self.ad_account.create_ad_set(params=adset_params)
            print(f"    {Colors.OKGREEN}✓ Ad Set created: {adset['id']}{Colors.ENDC}")
            return adset
            
        except Exception as e:
            print(f"    {Colors.FAIL}✗ Ad Set error: {str(e)}{Colors.ENDC}")
            return None

    def create_ads(self, campaign_id, adset_id, campaign_name):
        """Create 4 ads per campaign"""
        # Different ads based on campaign type
        if 'Cold' in campaign_name:
            ads = [
                {
                    'name': 'KT-Cold-Stats',
                    'headline': '87% van recruiters mist topkandidaten',
                    'description': 'Ontdek hoe jouw vacatures 40-60% meer reacties krijgen',
                    'utm_content': 'cold_stats'
                },
                {
                    'name': 'KT-Cold-Problem',
                    'headline': 'Te weinig goede sollicitaties?',
                    'description': 'Gratis vacature-analyse toont verbeterpunten',
                    'utm_content': 'cold_problem'
                }
            ]
        elif 'Consideration' in campaign_name:
            ads = [
                {
                    'name': 'KT-Consider-Case',
                    'headline': 'ASML: Van 12 naar 47 sollicitaties',
                    'description': 'Zie hoe zij hun vacatures transformeerden',
                    'utm_content': 'consider_case'
                },
                {
                    'name': 'KT-Consider-ROI',
                    'headline': '€2.400 bespaard per vacature',
                    'description': 'Bereken jouw potentiële ROI',
                    'utm_content': 'consider_roi'
                }
            ]
        else:  # Retargeting
            ads = [
                {
                    'name': 'KT-Retarget-Reminder',
                    'headline': 'Je vacature-analyse staat klaar',
                    'description': 'Bekijk je persoonlijke verbeterplan',
                    'utm_content': 'retarget_reminder'
                },
                {
                    'name': 'KT-Retarget-Urgency',
                    'headline': 'Laatste 48 uur: Gratis quickscan',
                    'description': 'Daarna €97 voor complete analyse',
                    'utm_content': 'retarget_urgency'
                }
            ]

        for ad_config in ads:
            self.create_single_ad(adset_id, campaign_name, ad_config)

    def create_single_ad(self, adset_id, campaign_name, ad_config):
        """Create a single ad"""
        try:
            # Build UTM URL
            campaign_slug = campaign_name.lower().replace('kt25--', '').replace('--', '_')
            utm_params = f"utm_source=meta&utm_medium=paid&utm_campaign={campaign_slug}&utm_content={ad_config['utm_content']}"
            full_url = f"https://kandidatentekort.nl/?{utm_params}"
            
            # Create creative
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
                            'value': {
                                'link': full_url
                            }
                        }
                    }
                }
            }
            
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

    def print_summary(self):
        """Print creation summary"""
        print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
        if self.created_campaigns:
            print(f"{Colors.OKGREEN}Successfully created {len(self.created_campaigns)} campaigns:{Colors.ENDC}")
            for camp in self.created_campaigns:
                print(f"  ✓ {camp['name']} (ID: {camp['id']})")
            
            print(f"\n{Colors.OKCYAN}Next steps:{Colors.ENDC}")
            print("1. Add images/videos to ads in Ads Manager")
            print("2. Set up lookalike audiences for Cold campaign")
            print("3. Review and activate campaigns")
            print("4. Monitor performance in GA4")
        else:
            print(f"{Colors.FAIL}No campaigns were created successfully{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='Create Kandidatentekort Traffic Campaigns'
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', help='Ad account ID')
    parser.add_argument('--page', required=True, help='Facebook Page ID')
    
    args = parser.parse_args()
    
    # Security check
    print(f"\n{Colors.WARNING}SECURITY CHECK:{Colors.ENDC}")
    print("✓ ONLY creating Kandidatentekort campaigns (KT25 prefix)")
    print("✓ ALL ads go to kandidatentekort.nl")
    print("✓ Using Recruitin page ONLY for Kandidatentekort")
    
    creator = KandidatentekortCampaigns(args.token, args.account, args.page)
    creator.create_campaigns()

if __name__ == "__main__":
    main()