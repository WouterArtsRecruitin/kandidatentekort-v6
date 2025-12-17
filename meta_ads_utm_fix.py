#!/usr/bin/env python3
"""
Meta Ads UTM Parameter Fix Tool
Ensures all ads have proper UTM tracking parameters
"""

import argparse
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MetaAdsUTMFixer:
    def __init__(self, access_token, account_id):
        """Initialize the Meta Ads API"""
        FacebookAdsApi.init(access_token=access_token)
        self.account_id = account_id
        self.ad_account = AdAccount(account_id)
        self.stats = {
            'total_ads': 0,
            'ads_with_utm': 0,
            'ads_missing_utm': 0,
            'ads_fixed': 0,
            'errors': 0
        }

    def get_utm_params(self, campaign_name, adset_name, ad_name):
        """Generate proper UTM parameters"""
        # Clean names for URL safety
        campaign_clean = campaign_name.lower().replace(' ', '_').replace('-', '_')
        adset_clean = adset_name.lower().replace(' ', '_').replace('-', '_')
        ad_clean = ad_name.lower().replace(' ', '_').replace('-', '_')
        
        return {
            'utm_source': 'facebook',
            'utm_medium': 'paid_social',
            'utm_campaign': f'kandidatentekort_{campaign_clean}',
            'utm_content': f'{adset_clean}_{ad_clean}',
            'utm_term': 'recruitment_nl'
        }

    def add_utm_to_url(self, url, utm_params):
        """Add UTM parameters to a URL"""
        if not url:
            return url
            
        # Parse the URL
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        
        # Add UTM parameters (don't override existing ones)
        for key, value in utm_params.items():
            if key not in query_params:
                query_params[key] = [value]
        
        # Reconstruct the URL
        new_query = urlencode(query_params, doseq=True)
        new_parsed = parsed._replace(query=new_query)
        return urlunparse(new_parsed)

    def check_url_utm(self, url):
        """Check if URL has UTM parameters"""
        if not url:
            return False
        
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        utm_keys = ['utm_source', 'utm_medium', 'utm_campaign']
        
        return all(key in query_params for key in utm_keys)

    def analyze_campaigns(self):
        """Analyze all campaigns for UTM parameters"""
        print(f"\n{Colors.HEADER}=== META ADS UTM ANALYSIS ==={Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        campaigns = self.ad_account.get_campaigns(fields=[
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status
        ])

        for campaign in campaigns:
            if campaign['status'] in ['ACTIVE', 'PAUSED']:
                self.analyze_campaign(campaign)

        self.print_summary()

    def analyze_campaign(self, campaign):
        """Analyze a single campaign"""
        print(f"\n{Colors.OKBLUE}Campaign: {campaign['name']}{Colors.ENDC}")
        
        adsets = campaign.get_ad_sets(fields=[
            AdSet.Field.id,
            AdSet.Field.name,
            AdSet.Field.status
        ])

        for adset in adsets:
            if adset['status'] in ['ACTIVE', 'PAUSED']:
                self.analyze_adset(adset, campaign)

    def analyze_adset(self, adset, campaign):
        """Analyze a single ad set"""
        print(f"  {Colors.OKCYAN}Ad Set: {adset['name']}{Colors.ENDC}")
        
        ads = adset.get_ads(fields=[
            Ad.Field.id,
            Ad.Field.name,
            Ad.Field.status,
            Ad.Field.creative
        ])

        for ad in ads:
            if ad['status'] in ['ACTIVE', 'PAUSED']:
                self.analyze_ad(ad, campaign, adset)

    def analyze_ad(self, ad, campaign, adset):
        """Analyze a single ad"""
        self.stats['total_ads'] += 1
        
        try:
            # Get creative
            creative_id = ad.get('creative', {}).get('id')
            if not creative_id:
                print(f"    {Colors.WARNING}⚠ Ad {ad['name']}: No creative found{Colors.ENDC}")
                return

            creative = AdCreative(creative_id)
            creative_data = creative.api_get(fields=[
                AdCreative.Field.object_story_spec,
                AdCreative.Field.link_url,
                AdCreative.Field.call_to_action
            ])

            # Extract URLs
            urls = self.extract_urls_from_creative(creative_data)
            
            has_utm = False
            missing_utm_urls = []
            
            for url_type, url in urls.items():
                if url:
                    if self.check_url_utm(url):
                        has_utm = True
                    else:
                        missing_utm_urls.append((url_type, url))
            
            if has_utm:
                self.stats['ads_with_utm'] += 1
                print(f"    {Colors.OKGREEN}✓ Ad {ad['name']}: UTM parameters present{Colors.ENDC}")
            elif missing_utm_urls:
                self.stats['ads_missing_utm'] += 1
                print(f"    {Colors.FAIL}✗ Ad {ad['name']}: Missing UTM parameters{Colors.ENDC}")
                for url_type, url in missing_utm_urls:
                    print(f"      - {url_type}: {url[:50]}...")
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"    {Colors.FAIL}✗ Ad {ad['name']}: Error - {str(e)}{Colors.ENDC}")

    def extract_urls_from_creative(self, creative_data):
        """Extract all URLs from creative"""
        urls = {}
        
        # Direct link URL
        if 'link_url' in creative_data:
            urls['link_url'] = creative_data['link_url']
        
        # Call to action
        if 'call_to_action' in creative_data:
            cta = creative_data['call_to_action']
            if isinstance(cta, dict) and 'value' in cta and 'link' in cta['value']:
                urls['cta_link'] = cta['value']['link']
        
        # Object story spec
        if 'object_story_spec' in creative_data:
            story_spec = creative_data['object_story_spec']
            if 'link_data' in story_spec:
                link_data = story_spec['link_data']
                if 'link' in link_data:
                    urls['story_link'] = link_data['link']
                if 'call_to_action' in link_data and 'value' in link_data['call_to_action']:
                    if 'link' in link_data['call_to_action']['value']:
                        urls['story_cta_link'] = link_data['call_to_action']['value']['link']
        
        return urls

    def fix_campaigns(self, dry_run=True):
        """Fix missing UTM parameters in campaigns"""
        mode = "DRY RUN" if dry_run else "LIVE UPDATE"
        print(f"\n{Colors.HEADER}=== META ADS UTM FIX - {mode} ==={Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        campaigns = self.ad_account.get_campaigns(fields=[
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status
        ])

        for campaign in campaigns:
            if campaign['status'] in ['ACTIVE', 'PAUSED']:
                self.fix_campaign(campaign, dry_run)

        self.print_summary()

    def fix_campaign(self, campaign, dry_run):
        """Fix UTM parameters in a single campaign"""
        print(f"\n{Colors.OKBLUE}Campaign: {campaign['name']}{Colors.ENDC}")
        
        adsets = campaign.get_ad_sets(fields=[
            AdSet.Field.id,
            AdSet.Field.name,
            AdSet.Field.status
        ])

        for adset in adsets:
            if adset['status'] in ['ACTIVE', 'PAUSED']:
                self.fix_adset(adset, campaign, dry_run)

    def fix_adset(self, adset, campaign, dry_run):
        """Fix UTM parameters in a single ad set"""
        print(f"  {Colors.OKCYAN}Ad Set: {adset['name']}{Colors.ENDC}")
        
        ads = adset.get_ads(fields=[
            Ad.Field.id,
            Ad.Field.name,
            Ad.Field.status,
            Ad.Field.creative
        ])

        for ad in ads:
            if ad['status'] in ['ACTIVE', 'PAUSED']:
                self.fix_ad(ad, campaign, adset, dry_run)

    def fix_ad(self, ad, campaign, adset, dry_run):
        """Fix UTM parameters in a single ad"""
        self.stats['total_ads'] += 1
        
        try:
            # Get creative
            creative_id = ad.get('creative', {}).get('id')
            if not creative_id:
                print(f"    {Colors.WARNING}⚠ Ad {ad['name']}: No creative found{Colors.ENDC}")
                return

            creative = AdCreative(creative_id)
            creative_data = creative.api_get(fields=[
                AdCreative.Field.object_story_spec,
                AdCreative.Field.link_url,
                AdCreative.Field.call_to_action,
                AdCreative.Field.name
            ])

            # Check if update needed
            urls = self.extract_urls_from_creative(creative_data)
            needs_update = False
            
            for url in urls.values():
                if url and not self.check_url_utm(url):
                    needs_update = True
                    break
            
            if not needs_update:
                self.stats['ads_with_utm'] += 1
                print(f"    {Colors.OKGREEN}✓ Ad {ad['name']}: Already has UTM{Colors.ENDC}")
                return
            
            # Generate UTM parameters
            utm_params = self.get_utm_params(
                campaign['name'],
                adset['name'],
                ad['name']
            )
            
            print(f"    {Colors.WARNING}⚡ Ad {ad['name']}: Adding UTM parameters{Colors.ENDC}")
            
            if dry_run:
                print(f"      {Colors.OKCYAN}[DRY RUN] Would add:{Colors.ENDC}")
                for key, value in utm_params.items():
                    print(f"        - {key}={value}")
            else:
                # Create new creative with UTM
                new_creative_data = self.create_updated_creative(
                    creative_data, 
                    utm_params,
                    f"{creative_data.get('name', 'Creative')}_UTM"
                )
                
                # Create new creative
                new_creative = self.ad_account.create_ad_creative(
                    params=new_creative_data
                )
                
                # Update ad with new creative
                ad.api_update(params={
                    'creative': {'creative_id': new_creative['id']}
                })
                
                self.stats['ads_fixed'] += 1
                print(f"      {Colors.OKGREEN}✓ Updated successfully{Colors.ENDC}")
            
            self.stats['ads_missing_utm'] += 1
            
        except Exception as e:
            self.stats['errors'] += 1
            print(f"    {Colors.FAIL}✗ Ad {ad['name']}: Error - {str(e)}{Colors.ENDC}")

    def create_updated_creative(self, original_creative, utm_params, new_name):
        """Create a new creative with UTM parameters"""
        new_data = {
            'name': new_name
        }
        
        # Copy and update link_url
        if 'link_url' in original_creative:
            new_data['link_url'] = self.add_utm_to_url(
                original_creative['link_url'], 
                utm_params
            )
        
        # Copy and update object_story_spec
        if 'object_story_spec' in original_creative:
            story_spec = original_creative['object_story_spec'].copy()
            
            if 'link_data' in story_spec:
                link_data = story_spec['link_data']
                if 'link' in link_data:
                    link_data['link'] = self.add_utm_to_url(
                        link_data['link'], 
                        utm_params
                    )
            
            new_data['object_story_spec'] = story_spec
        
        return new_data

    def print_summary(self):
        """Print analysis summary"""
        print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
        print(f"Total ads analyzed: {self.stats['total_ads']}")
        print(f"{Colors.OKGREEN}Ads with UTM: {self.stats['ads_with_utm']}{Colors.ENDC}")
        print(f"{Colors.FAIL}Ads missing UTM: {self.stats['ads_missing_utm']}{Colors.ENDC}")
        if self.stats['ads_fixed'] > 0:
            print(f"{Colors.OKGREEN}Ads fixed: {self.stats['ads_fixed']}{Colors.ENDC}")
        if self.stats['errors'] > 0:
            print(f"{Colors.WARNING}Errors: {self.stats['errors']}{Colors.ENDC}")
        
        if self.stats['ads_missing_utm'] > 0:
            percentage = (self.stats['ads_missing_utm'] / self.stats['total_ads']) * 100
            print(f"\n{Colors.WARNING}⚠ {percentage:.1f}% of ads need UTM parameters{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='Fix missing UTM parameters in Meta ads',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze ads
  python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_123456

  # Fix ads (dry run)
  python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_123456 --fix

  # Fix ads (live)
  python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_123456 --fix --live
        """
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', required=True, help='Ad account ID (e.g., act_123456)')
    parser.add_argument('--fix', action='store_true', help='Fix missing UTM parameters')
    parser.add_argument('--live', action='store_true', help='Actually update ads (requires --fix)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.live and not args.fix:
        parser.error("--live requires --fix")
    
    # Initialize fixer
    fixer = MetaAdsUTMFixer(args.token, args.account)
    
    try:
        if args.fix:
            fixer.fix_campaigns(dry_run=not args.live)
        else:
            fixer.analyze_campaigns()
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()