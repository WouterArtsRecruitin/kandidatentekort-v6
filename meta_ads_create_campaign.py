#!/usr/bin/env python3
"""
Create Meta Ads Traffic Campaigns with Proper UTM Tracking
Voor Kandidatentekort.nl - 40-60% meer sollicitaties
"""

import argparse
import sys
import json
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.targetinggeolocationcustomlocation import TargetingGeoLocationCustomLocation
from facebook_business.adobjects.targetinggeolocation import TargetingGeoLocation

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class KandidatentekortCampaignCreator:
    def __init__(self, access_token=None, account_id=None, page_id=None):
        if access_token:
            FacebookAdsApi.init(access_token=access_token)
            self.ad_account = AdAccount(account_id)
        self.account_id = account_id
        self.page_id = page_id
        
        # Campaign configurations
        self.campaigns = [
            {
                'name': 'KT25--Traffic--Cold-Awareness--Dec2025',
                'daily_budget': 8000,  # €80 in cents
                'ads': [
                    {
                        'name': 'KT-Traffic-Cold-1-Stats',
                        'headline': '87% van recruiters mist topkandidaten',
                        'description': 'Ontdek hoe jouw vacatures 40-60% meer reacties krijgen',
                        'cta': 'LEARN_MORE',
                        'utm_content': 'cold_stats'
                    },
                    {
                        'name': 'KT-Traffic-Cold-2-Problem',
                        'headline': 'Te weinig goede sollicitaties?',
                        'description': 'Gratis vacature-analyse toont verbeterpunten',
                        'cta': 'LEARN_MORE',
                        'utm_content': 'cold_problem'
                    },
                    {
                        'name': 'KT-Traffic-Cold-3-Solution',
                        'headline': '40-60% meer sollicitaties gegarandeerd',
                        'description': 'Bewezen methode voor betere vacatureteksten',
                        'cta': 'GET_OFFER',
                        'utm_content': 'cold_solution'
                    },
                    {
                        'name': 'KT-Traffic-Cold-4-Authority',
                        'headline': '500+ recruiters verbeterden al hun resultaten',
                        'description': 'Krijg direct praktische tips voor jouw vacatures',
                        'cta': 'LEARN_MORE',
                        'utm_content': 'cold_authority'
                    }
                ]
            },
            {
                'name': 'KT25--Traffic--Consideration--Dec2025',
                'daily_budget': 8000,  # €80 in cents
                'ads': [
                    {
                        'name': 'KT-Traffic-Consider-1-CaseStudy',
                        'headline': 'ASML: Van 12 naar 47 sollicitaties',
                        'description': 'Zie hoe zij hun vacatures transformeerden',
                        'cta': 'DOWNLOAD',
                        'utm_content': 'consider_case'
                    },
                    {
                        'name': 'KT-Traffic-Consider-2-Features',
                        'headline': 'AI-analyse + persoonlijk advies',
                        'description': 'Complete vacature-optimalisatie in 24 uur',
                        'cta': 'LEARN_MORE',
                        'utm_content': 'consider_features'
                    },
                    {
                        'name': 'KT-Traffic-Consider-3-Comparison',
                        'headline': 'Waarom 73% kiest voor onze methode',
                        'description': 'Vergelijk zelf: traditioneel vs. geoptimaliseerd',
                        'cta': 'SEE_MORE',
                        'utm_content': 'consider_compare'
                    },
                    {
                        'name': 'KT-Traffic-Consider-4-ROI',
                        'headline': '€2.400 bespaard per vacature',
                        'description': 'Bereken jouw potentiële ROI',
                        'cta': 'GET_QUOTE',
                        'utm_content': 'consider_roi'
                    }
                ]
            },
            {
                'name': 'KT25--Traffic--Retargeting--Dec2025',
                'daily_budget': 8000,  # €80 in cents
                'ads': [
                    {
                        'name': 'KT-Traffic-Retarget-1-Reminder',
                        'headline': 'Je vacature-analyse staat klaar',
                        'description': 'Bekijk je persoonlijke verbeterplan',
                        'cta': 'GET_STARTED',
                        'utm_content': 'retarget_reminder'
                    },
                    {
                        'name': 'KT-Traffic-Retarget-2-Urgency',
                        'headline': 'Laatste 48 uur: Gratis quickscan',
                        'description': 'Daarna €97 voor complete analyse',
                        'cta': 'APPLY_NOW',
                        'utm_content': 'retarget_urgency'
                    },
                    {
                        'name': 'KT-Traffic-Retarget-3-Social',
                        'headline': '+127 recruiters deze week',
                        'description': 'Sluit je aan bij succesvolle collega\'s',
                        'cta': 'SIGN_UP',
                        'utm_content': 'retarget_social'
                    },
                    {
                        'name': 'KT-Traffic-Retarget-4-Bonus',
                        'headline': 'Extra: Template bibliotheek cadeau',
                        'description': 'Bij aanvraag voor 31 december',
                        'cta': 'LEARN_MORE',
                        'utm_content': 'retarget_bonus'
                    }
                ]
            }
        ]

    def preview_campaigns(self):
        """Show campaign structure without API calls"""
        print(f"\n{Colors.HEADER}=== KANDIDATENTEKORT CAMPAIGN PREVIEW ==={Colors.ENDC}")
        print(f"Total daily budget: €240 (€80 per campaign)")
        print(f"Target: Netherlands, Age 25-55")
        print(f"Objective: OUTCOME_TRAFFIC → kandidatentekort.nl\n")

        for campaign in self.campaigns:
            print(f"{Colors.OKBLUE}Campaign: {campaign['name']}{Colors.ENDC}")
            print(f"  Daily Budget: €{campaign['daily_budget']/100}")
            print(f"  Number of Ads: {len(campaign['ads'])}")
            
            for ad in campaign['ads']:
                print(f"\n  {Colors.OKCYAN}Ad: {ad['name']}{Colors.ENDC}")
                print(f"    Headline: {ad['headline']}")
                print(f"    Description: {ad['description']}")
                print(f"    CTA: {ad['cta']}")
                print(f"    UTM: kandidatentekort.nl/?utm_source=meta&utm_medium=paid&utm_campaign={campaign['name'].lower().replace('--', '_')}&utm_content={ad['utm_content']}")
            print()

    def create_campaigns(self, dry_run=True):
        """Create campaigns with proper structure"""
        created_campaigns = []
        
        print(f"\n{Colors.HEADER}=== CREATING KANDIDATENTEKORT TRAFFIC CAMPAIGNS ==={Colors.ENDC}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print(f"Account: {self.account_id}\n")

        for campaign_config in self.campaigns:
            try:
                campaign = self.create_campaign(campaign_config, dry_run)
                if campaign:
                    created_campaigns.append(campaign)
            except Exception as e:
                print(f"{Colors.FAIL}Error creating campaign: {str(e)}{Colors.ENDC}")

        return created_campaigns

    def create_campaign(self, config, dry_run):
        """Create a single campaign"""
        print(f"{Colors.OKBLUE}Creating Campaign: {config['name']}{Colors.ENDC}")
        
        campaign_params = {
            'name': config['name'],
            'objective': Campaign.Objective.outcome_traffic,
            'status': Campaign.Status.paused,
            'special_ad_categories': []
        }

        if dry_run:
            print(f"  [DRY RUN] Would create campaign with:")
            print(f"    - Objective: TRAFFIC")
            print(f"    - Status: PAUSED")
            print(f"    - Budget: €{config['daily_budget']/100}/day")
            campaign_id = f"dry_run_campaign_{config['name']}"
        else:
            campaign = self.ad_account.create_campaign(params=campaign_params)
            campaign_id = campaign['id']
            print(f"  {Colors.OKGREEN}✓ Campaign created: {campaign_id}{Colors.ENDC}")

        # Create ad set
        adset = self.create_adset(campaign_id, config, dry_run)
        
        # Create ads
        for ad_config in config['ads']:
            self.create_ad(campaign_id, adset['id'] if adset else 'dry_run_adset', 
                          config['name'], ad_config, dry_run)

        return {'id': campaign_id, 'name': config['name']}

    def create_adset(self, campaign_id, campaign_config, dry_run):
        """Create ad set with targeting"""
        print(f"\n  {Colors.OKCYAN}Creating Ad Set{Colors.ENDC}")
        
        # Dutch targeting
        targeting = {
            'geo_locations': {
                'countries': ['NL']
            },
            'age_min': 25,
            'age_max': 55,
            'publisher_platforms': ['facebook', 'instagram'],
            'facebook_positions': ['feed', 'instant_article', 'marketplace'],
            'instagram_positions': ['stream', 'story', 'explore']
        }

        adset_params = {
            'name': f"{campaign_config['name']}--AdSet",
            'campaign_id': campaign_id,
            'daily_budget': campaign_config['daily_budget'],
            'billing_event': AdSet.BillingEvent.impressions,
            'optimization_goal': AdSet.OptimizationGoal.link_clicks,
            'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
            'targeting': targeting,
            'status': AdSet.Status.paused
        }

        if dry_run:
            print(f"    [DRY RUN] Would create ad set with:")
            print(f"      - Targeting: Netherlands, Age 25-55")
            print(f"      - Daily Budget: €{campaign_config['daily_budget']/100}")
            print(f"      - Optimization: Link Clicks")
            return {'id': 'dry_run_adset'}
        else:
            adset = AdSet(parent_id=self.account_id)
            adset.update(adset_params)
            adset.remote_create()
            print(f"    {Colors.OKGREEN}✓ Ad Set created: {adset['id']}{Colors.ENDC}")
            return adset

    def create_ad(self, campaign_id, adset_id, campaign_name, ad_config, dry_run):
        """Create individual ad with UTM tracking"""
        print(f"\n    {Colors.WARNING}Creating Ad: {ad_config['name']}{Colors.ENDC}")
        
        # Build URL with UTM
        base_url = "https://kandidatentekort.nl/"
        utm_params = {
            'utm_source': 'meta',
            'utm_medium': 'paid',
            'utm_campaign': campaign_name.lower().replace('--', '_').replace('kt25_', ''),
            'utm_content': ad_config['utm_content']
        }
        
        utm_string = '&'.join([f"{k}={v}" for k, v in utm_params.items()])
        full_url = f"{base_url}?{utm_string}"

        # Creative data
        creative_params = {
            'name': f"{ad_config['name']}--Creative",
            'object_story_spec': {
                'page_id': self.page_id,
                'link_data': {
                    'link': full_url,
                    'message': ad_config['description'],
                    'name': ad_config['headline'],
                    'call_to_action': {
                        'type': ad_config['cta'],
                        'value': {
                            'link': full_url
                        }
                    }
                }
            }
        }

        if dry_run:
            print(f"      [DRY RUN] Would create ad with:")
            print(f"        - Headline: {ad_config['headline']}")
            print(f"        - URL: {full_url}")
            print(f"        - CTA: {ad_config['cta']}")
        else:
            # Create creative
            creative = self.ad_account.create_ad_creative(params=creative_params)
            
            # Create ad
            ad_params = {
                'name': ad_config['name'],
                'adset_id': adset_id,
                'creative': {'creative_id': creative['id']},
                'status': Ad.Status.paused
            }
            
            ad = self.ad_account.create_ad(params=ad_params)
            print(f"      {Colors.OKGREEN}✓ Ad created: {ad['id']}{Colors.ENDC}")
            print(f"        - URL: {full_url}")

def main():
    parser = argparse.ArgumentParser(
        description='Create Kandidatentekort Traffic Campaigns',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--preview', action='store_true', 
                       help='Preview campaign structure without API calls')
    parser.add_argument('--token', help='Facebook access token')
    parser.add_argument('--account', help='Ad account ID (e.g., act_123456)')
    parser.add_argument('--page', help='Facebook Page ID')
    parser.add_argument('--live', action='store_true', 
                       help='Actually create campaigns (default is dry run)')
    
    args = parser.parse_args()
    
    if args.preview:
        creator = KandidatentekortCampaignCreator()
        creator.preview_campaigns()
    else:
        if not all([args.token, args.account, args.page]):
            parser.error("--token, --account, and --page are required for campaign creation")
        
        creator = KandidatentekortCampaignCreator(
            args.token, 
            args.account, 
            args.page
        )
        
        creator.create_campaigns(dry_run=not args.live)
        
        if not args.live:
            print(f"\n{Colors.WARNING}This was a DRY RUN. Add --live to create campaigns.{Colors.ENDC}")

if __name__ == "__main__":
    main()