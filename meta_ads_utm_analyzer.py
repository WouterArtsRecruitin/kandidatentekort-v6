#!/usr/bin/env python3
"""
Meta Ads UTM Analyzer - Deep dive into campaign URLs and UTM setup
"""

import argparse
import json
from datetime import datetime
from urllib.parse import urlparse, parse_qs
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

class MetaAdsUTMAnalyzer:
    def __init__(self, access_token, account_id):
        FacebookAdsApi.init(access_token=access_token)
        self.account_id = account_id
        self.ad_account = AdAccount(account_id)
        self.report = {
            'total_campaigns': 0,
            'total_ads': 0,
            'ads_to_website': 0,
            'ads_to_facebook': 0,
            'ads_with_proper_utm': 0,
            'campaigns': []
        }

    def analyze_all_campaigns(self):
        print(f"\n{Colors.HEADER}=== META ADS UTM DEEP ANALYSIS ==={Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        # Focus on Kandidatentekort campaigns
        campaigns = self.ad_account.get_campaigns(fields=[
            Campaign.Field.id,
            Campaign.Field.name,
            Campaign.Field.status,
            Campaign.Field.objective
        ])

        for campaign in campaigns:
            if 'KT25' in campaign.get('name', '') or 'Kandidatentekort' in campaign.get('name', ''):
                self.report['total_campaigns'] += 1
                self.analyze_campaign_details(campaign)

        self.print_detailed_report()

    def analyze_campaign_details(self, campaign):
        campaign_data = {
            'name': campaign['name'],
            'objective': campaign.get('objective', 'Unknown'),
            'ads': []
        }

        print(f"\n{Colors.OKBLUE}Campaign: {campaign['name']}{Colors.ENDC}")
        print(f"  Objective: {campaign.get('objective', 'Unknown')}")

        try:
            adsets = campaign.get_ad_sets(fields=[
                AdSet.Field.id,
                AdSet.Field.name,
                AdSet.Field.status
            ])

            for adset in adsets:
                if adset['status'] in ['ACTIVE', 'PAUSED']:
                    ads = adset.get_ads(fields=[
                        Ad.Field.id,
                        Ad.Field.name,
                        Ad.Field.status,
                        Ad.Field.creative,
                        Ad.Field.tracking_specs,
                        Ad.Field.url_tags
                    ])

                    for ad in ads:
                        if ad['status'] in ['ACTIVE', 'PAUSED']:
                            self.report['total_ads'] += 1
                            ad_analysis = self.analyze_ad_utm(ad, campaign, adset)
                            campaign_data['ads'].append(ad_analysis)

        except Exception as e:
            print(f"  {Colors.FAIL}Error analyzing campaign: {str(e)}{Colors.ENDC}")

        self.report['campaigns'].append(campaign_data)

    def analyze_ad_utm(self, ad, campaign, adset):
        ad_data = {
            'name': ad['name'],
            'destination': 'Unknown',
            'url': None,
            'utm_params': {},
            'issues': []
        }

        print(f"\n  {Colors.OKCYAN}Ad: {ad['name']}{Colors.ENDC}")

        try:
            # Get creative details
            creative_id = ad.get('creative', {}).get('id')
            if creative_id:
                creative = AdCreative(creative_id)
                creative_data = creative.api_get(fields=[
                    AdCreative.Field.object_story_spec,
                    AdCreative.Field.link_url,
                    AdCreative.Field.url_tags,
                    AdCreative.Field.call_to_action
                ])

                # Extract all URLs
                urls = self.extract_all_urls(creative_data)
                
                # Check Meta URL tags
                url_tags = ad.get('url_tags', '') or creative_data.get('url_tags', '')
                if url_tags:
                    print(f"    URL Tags: {url_tags}")
                    ad_data['utm_params'] = self.parse_url_tags(url_tags)

                # Analyze destination
                primary_url = None
                for url_type, url in urls.items():
                    if url:
                        print(f"    {url_type}: {url[:80]}...")
                        if not primary_url:
                            primary_url = url
                            ad_data['url'] = url

                if primary_url:
                    if 'kandidatentekort.nl' in primary_url:
                        ad_data['destination'] = 'Website'
                        self.report['ads_to_website'] += 1
                        print(f"    {Colors.OKGREEN}✓ Goes to kandidatentekort.nl{Colors.ENDC}")
                    elif 'facebook.com' in primary_url:
                        ad_data['destination'] = 'Facebook'
                        self.report['ads_to_facebook'] += 1
                        print(f"    {Colors.WARNING}⚠ Stays on Facebook{Colors.ENDC}")
                        ad_data['issues'].append('Links to Facebook, not website')
                else:
                    print(f"    {Colors.FAIL}✗ No destination URL found{Colors.ENDC}")
                    ad_data['issues'].append('No destination URL')

                # Check UTM completeness
                self.check_utm_completeness(ad_data)

        except Exception as e:
            print(f"    {Colors.FAIL}Error: {str(e)}{Colors.ENDC}")
            ad_data['issues'].append(f'Error: {str(e)}')

        return ad_data

    def extract_all_urls(self, creative_data):
        urls = {}
        
        # Direct link URL
        if 'link_url' in creative_data:
            urls['link_url'] = creative_data['link_url']
        
        # Object story spec
        if 'object_story_spec' in creative_data:
            story_spec = creative_data['object_story_spec']
            
            # Video data
            if 'video_data' in story_spec:
                video_data = story_spec['video_data']
                if 'call_to_action' in video_data:
                    cta = video_data['call_to_action']
                    if 'value' in cta and 'link' in cta['value']:
                        urls['video_cta_link'] = cta['value']['link']
                if 'message' in video_data:
                    # Check if message contains a link
                    message = video_data['message']
                    if 'http' in message:
                        urls['message_link'] = 'Link in message text'
            
            # Link data
            if 'link_data' in story_spec:
                link_data = story_spec['link_data']
                if 'link' in link_data:
                    urls['story_link'] = link_data['link']
        
        return urls

    def parse_url_tags(self, url_tags):
        """Parse Meta's url_tags format"""
        params = {}
        if url_tags:
            # url_tags format: "utm_source=meta&utm_medium=paid"
            pairs = url_tags.split('&')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    params[key] = value
        return params

    def check_utm_completeness(self, ad_data):
        required_utms = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content']
        missing = []
        
        for utm in required_utms:
            if utm not in ad_data['utm_params'] or not ad_data['utm_params'][utm]:
                missing.append(utm)
        
        if missing:
            ad_data['issues'].append(f"Missing UTM: {', '.join(missing)}")
            print(f"    {Colors.FAIL}✗ Missing UTM parameters: {', '.join(missing)}{Colors.ENDC}")
        else:
            self.report['ads_with_proper_utm'] += 1
            print(f"    {Colors.OKGREEN}✓ All UTM parameters present{Colors.ENDC}")

    def print_detailed_report(self):
        print(f"\n{Colors.HEADER}=== DETAILED REPORT ==={Colors.ENDC}")
        print(f"\nTotal Campaigns Analyzed: {self.report['total_campaigns']}")
        print(f"Total Ads Analyzed: {self.report['total_ads']}")
        print(f"{Colors.OKGREEN}Ads to Website: {self.report['ads_to_website']}{Colors.ENDC}")
        print(f"{Colors.WARNING}Ads to Facebook: {self.report['ads_to_facebook']}{Colors.ENDC}")
        print(f"Ads with Proper UTM: {self.report['ads_with_proper_utm']}")

        print(f"\n{Colors.HEADER}=== ISSUES SUMMARY ==={Colors.ENDC}")
        
        # Collect all issues
        all_issues = []
        for campaign in self.report['campaigns']:
            for ad in campaign['ads']:
                if ad['issues']:
                    all_issues.append({
                        'campaign': campaign['name'],
                        'ad': ad['name'],
                        'issues': ad['issues']
                    })
        
        if all_issues:
            for issue in all_issues:
                print(f"\n{Colors.FAIL}Campaign: {issue['campaign'][:50]}...{Colors.ENDC}")
                print(f"Ad: {issue['ad']}")
                for i in issue['issues']:
                    print(f"  - {i}")
        else:
            print(f"{Colors.OKGREEN}No issues found!{Colors.ENDC}")

        # Save detailed report
        with open('utm_analysis_report.json', 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"\n💾 Detailed report saved to: utm_analysis_report.json")

def main():
    parser = argparse.ArgumentParser(description='Analyze Meta Ads UTM setup')
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', required=True, help='Ad account ID')
    
    args = parser.parse_args()
    
    analyzer = MetaAdsUTMAnalyzer(args.token, args.account)
    
    try:
        analyzer.analyze_all_campaigns()
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")

if __name__ == "__main__":
    main()