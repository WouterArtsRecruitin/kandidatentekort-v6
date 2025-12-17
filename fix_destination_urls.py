#!/usr/bin/env python3
"""
Fix Destination URLs for Existing Kandidatentekort Ads
Converts Reels/Engagement ads to Traffic ads with proper UTM tracking
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

class DestinationURLFixer:
    def __init__(self, access_token, account_id):
        FacebookAdsApi.init(access_token=access_token)
        self.account_id = account_id
        self.ad_account = AdAccount(account_id)
        self.stats = {
            'total_ads': 0,
            'reels_ads': 0,
            'fixed_ads': 0,
            'errors': 0
        }

    def fix_all_campaigns(self, dry_run=True):
        """Fix destination URLs for all Kandidatentekort campaigns"""
        mode = "DRY RUN" if dry_run else "LIVE UPDATE"
        print(f"\n{Colors.HEADER}=== FIX DESTINATION URLS - {mode} ==={Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        campaigns = self.ad_account.get_campaigns(fields=[
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status,
            Campaign.Field.objective
        ])

        for campaign in campaigns:
            if ('KT25' in campaign.get('name', '') or 
                'Kandidatentekort' in campaign.get('name', '')) and \
               campaign['status'] in ['ACTIVE', 'PAUSED']:
                self.process_campaign(campaign, dry_run)

        self.print_summary()

    def process_campaign(self, campaign, dry_run):
        """Process a single campaign"""
        print(f"\n{Colors.OKBLUE}Campaign: {campaign['name']}{Colors.ENDC}")
        print(f"  Objective: {campaign.get('objective', 'Unknown')}")

        if campaign.get('objective') != 'OUTCOME_TRAFFIC':
            print(f"  {Colors.WARNING}⚠ Campaign objective is {campaign.get('objective')}, not TRAFFIC{Colors.ENDC}")

        try:
            adsets = campaign.get_ad_sets(fields=[
                AdSet.Field.id,
                AdSet.Field.name,
                AdSet.Field.status
            ])

            for adset in adsets:
                if adset['status'] in ['ACTIVE', 'PAUSED']:
                    self.process_adset(adset, campaign, dry_run)

        except Exception as e:
            print(f"  {Colors.FAIL}Error: {str(e)}{Colors.ENDC}")
            self.stats['errors'] += 1

    def process_adset(self, adset, campaign, dry_run):
        """Process a single ad set"""
        print(f"\n  {Colors.OKCYAN}Ad Set: {adset['name']}{Colors.ENDC}")

        try:
            ads = adset.get_ads(fields=[
                Ad.Field.id,
                Ad.Field.name,
                Ad.Field.status,
                Ad.Field.creative
            ])

            for ad in ads:
                if ad['status'] in ['ACTIVE', 'PAUSED']:
                    self.fix_ad_destination(ad, campaign, adset, dry_run)

        except Exception as e:
            print(f"    {Colors.FAIL}Error: {str(e)}{Colors.ENDC}")
            self.stats['errors'] += 1

    def fix_ad_destination(self, ad, campaign, adset, dry_run):
        """Fix destination URL for a single ad"""
        self.stats['total_ads'] += 1
        print(f"\n    {Colors.WARNING}Ad: {ad['name']}{Colors.ENDC}")

        try:
            # Get creative
            creative_id = ad.get('creative', {}).get('id')
            if not creative_id:
                print(f"      {Colors.FAIL}✗ No creative found{Colors.ENDC}")
                return

            creative = AdCreative(creative_id)
            creative_data = creative.api_get(fields=[
                AdCreative.Field.object_story_spec,
                AdCreative.Field.link_url,
                AdCreative.Field.name
            ])

            # Check current destination
            current_url = None
            needs_fix = False
            
            if 'object_story_spec' in creative_data:
                story_spec = creative_data['object_story_spec']
                
                # Check video data (Reels)
                if 'video_data' in story_spec:
                    video_data = story_spec['video_data']
                    print(f"      📹 Currently a Reels/Video ad")
                    self.stats['reels_ads'] += 1
                    needs_fix = True
                    
                    # Check if there's already a CTA
                    if 'call_to_action' in video_data:
                        cta = video_data['call_to_action']
                        if 'value' in cta and 'link' in cta['value']:
                            current_url = cta['value']['link']
                            print(f"      Current CTA URL: {current_url[:50]}...")
                
                # Check link data
                elif 'link_data' in story_spec:
                    link_data = story_spec['link_data']
                    if 'link' in link_data:
                        current_url = link_data['link']
                        print(f"      Current URL: {current_url[:50]}...")
                        
                        if 'kandidatentekort.nl' not in current_url:
                            needs_fix = True

            if not needs_fix and current_url and 'kandidatentekort.nl' in current_url:
                print(f"      {Colors.OKGREEN}✓ Already goes to kandidatentekort.nl{Colors.ENDC}")
                return

            # Generate proper URL with UTM
            campaign_slug = self.generate_campaign_slug(campaign['name'])
            ad_slug = self.generate_ad_slug(ad['name'])
            
            new_url = f"https://kandidatentekort.nl/?utm_source=meta&utm_medium=paid&utm_campaign={campaign_slug}&utm_content={ad_slug}"

            print(f"      {Colors.FAIL}✗ Needs fix - currently goes to Facebook/Reels{Colors.ENDC}")
            print(f"      New URL: {new_url}")

            if dry_run:
                print(f"      {Colors.OKCYAN}[DRY RUN] Would update to traffic ad{Colors.ENDC}")
                self.stats['fixed_ads'] += 1
            else:
                # Create new creative with website link
                new_creative_data = self.create_traffic_creative(
                    creative_data, 
                    new_url,
                    ad['name']
                )
                
                # Create new creative
                new_creative = self.ad_account.create_ad_creative(
                    params=new_creative_data
                )
                
                # Update ad with new creative
                ad.api_update(params={
                    'creative': {'creative_id': new_creative['id']}
                })
                
                print(f"      {Colors.OKGREEN}✓ Updated to traffic ad with UTM tracking{Colors.ENDC}")
                self.stats['fixed_ads'] += 1

        except Exception as e:
            print(f"      {Colors.FAIL}✗ Error: {str(e)}{Colors.ENDC}")
            self.stats['errors'] += 1

    def create_traffic_creative(self, original_creative, new_url, ad_name):
        """Create a new creative that drives traffic to website"""
        new_data = {
            'name': f"{original_creative.get('name', 'Creative')}_Traffic_Fixed",
            'object_story_spec': {}
        }

        # Get page ID from original
        if 'object_story_spec' in original_creative:
            orig_spec = original_creative['object_story_spec']
            if 'page_id' in orig_spec:
                new_data['object_story_spec']['page_id'] = orig_spec['page_id']
            elif 'instagram_actor_id' in orig_spec:
                new_data['object_story_spec']['instagram_actor_id'] = orig_spec['instagram_actor_id']

        # Create link data structure
        link_data = {
            'link': new_url,
            'call_to_action': {
                'type': 'LEARN_MORE',
                'value': {
                    'link': new_url
                }
            }
        }

        # Add content from original creative
        if 'object_story_spec' in original_creative:
            orig_spec = original_creative['object_story_spec']
            
            # If it was a video ad
            if 'video_data' in orig_spec:
                video_data = orig_spec['video_data']
                if 'message' in video_data:
                    link_data['message'] = video_data['message']
                if 'title' in video_data:
                    link_data['name'] = video_data['title']
                # You might want to reuse the video as an image
                # This would require additional processing
            
            # If it already had link data
            elif 'link_data' in orig_spec:
                orig_link = orig_spec['link_data']
                if 'message' in orig_link:
                    link_data['message'] = orig_link['message']
                if 'name' in orig_link:
                    link_data['name'] = orig_link['name']
                if 'description' in orig_link:
                    link_data['description'] = orig_link['description']

        # Default content if none found
        if 'name' not in link_data:
            link_data['name'] = '40-60% meer sollicitaties gegarandeerd'
        if 'message' not in link_data:
            link_data['message'] = 'Ontdek hoe jouw vacatures meer gekwalificeerde kandidaten aantrekken. Gratis analyse!'

        new_data['object_story_spec']['link_data'] = link_data
        
        return new_data

    def generate_campaign_slug(self, campaign_name):
        """Generate URL-safe campaign slug"""
        # Remove KT25 prefix and clean up
        slug = campaign_name.lower()
        slug = slug.replace('kt25--', '').replace('kt25_', '')
        slug = slug.replace('--', '_').replace(' ', '_')
        slug = slug.replace('kandidatentekort_', 'kt_')
        # Keep only alphanumeric and underscore
        slug = ''.join(c for c in slug if c.isalnum() or c == '_')
        return slug[:30]  # Limit length

    def generate_ad_slug(self, ad_name):
        """Generate URL-safe ad slug"""
        slug = ad_name.lower()
        slug = slug.replace('kt-', '').replace('kt_', '')
        slug = slug.replace('-', '_').replace(' ', '_')
        # Keep only alphanumeric and underscore
        slug = ''.join(c for c in slug if c.isalnum() or c == '_')
        return slug[:20]  # Limit length

    def print_summary(self):
        """Print fix summary"""
        print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
        print(f"Total ads analyzed: {self.stats['total_ads']}")
        print(f"{Colors.WARNING}Reels/Facebook ads found: {self.stats['reels_ads']}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}Ads fixed: {self.stats['fixed_ads']}{Colors.ENDC}")
        if self.stats['errors'] > 0:
            print(f"{Colors.FAIL}Errors: {self.stats['errors']}{Colors.ENDC}")

        if self.stats['reels_ads'] > 0:
            print(f"\n{Colors.WARNING}⚠ {self.stats['reels_ads']} ads are currently Reels/Engagement ads{Colors.ENDC}")
            print(f"These need to be converted to Traffic ads to track conversions")

def main():
    parser = argparse.ArgumentParser(
        description='Fix destination URLs for Kandidatentekort ads',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', required=True, help='Ad account ID')
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help='Preview changes without updating (default)')
    parser.add_argument('--live', action='store_true',
                       help='Actually update the ads')
    
    args = parser.parse_args()
    
    # If --live is specified, turn off dry-run
    if args.live:
        args.dry_run = False
    
    fixer = DestinationURLFixer(args.token, args.account)
    
    try:
        fixer.fix_all_campaigns(dry_run=args.dry_run)
        
        if args.dry_run:
            print(f"\n{Colors.WARNING}This was a DRY RUN. Add --live to apply changes.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()