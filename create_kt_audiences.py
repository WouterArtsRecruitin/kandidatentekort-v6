#!/usr/bin/env python3
"""
Simplified Kandidatentekort Custom Audiences Creator
Creates only the essential audiences for the funnel
"""

import argparse
import sys
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.customaudience import CustomAudience

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def create_website_audiences(account, pixel_id):
    """Create website visitor audiences"""
    audiences = []
    
    website_configs = [
        {
            'name': 'KT - All Website Visitors 180d',
            'retention_days': 180,
            'description': 'All visitors - Seed for lookalikes'
        },
        {
            'name': 'KT - Website Visitors 30d',
            'retention_days': 30,
            'description': 'Recent visitors - Consideration'
        },
        {
            'name': 'KT - Website Visitors 14d',
            'retention_days': 14,
            'description': 'Recent visitors - Warm retargeting'
        },
        {
            'name': 'KT - Website Visitors 7d',
            'retention_days': 7,
            'description': 'Hot leads - Immediate retargeting'
        }
    ]
    
    for config in website_configs:
        try:
            print(f"\n{Colors.OKCYAN}Creating: {config['name']}{Colors.ENDC}")
            
            params = {
                'name': config['name'],
                'description': config['description'],
                'subtype': 'WEBSITE',
                'retention_days': config['retention_days'],
                'rule': {
                    'inclusions': {
                        'operator': 'or',
                        'rules': [{
                            'event_sources': [{'id': pixel_id, 'type': 'pixel'}],
                            'retention_seconds': config['retention_days'] * 86400,
                            'filter': {
                                'operator': 'and',
                                'filters': [{
                                    'field': 'event',
                                    'operator': 'eq',
                                    'value': 'PageView'
                                }]
                            }
                        }]
                    }
                },
                'prefill': True
            }
            
            audience = account.create_custom_audience(params=params)
            print(f"{Colors.OKGREEN}✓ Created: {audience['id']}{Colors.ENDC}")
            audiences.append(audience)
            
        except Exception as e:
            print(f"{Colors.FAIL}✗ Error creating {config['name']}: {str(e)}{Colors.ENDC}")
    
    return audiences

def create_event_audiences(account, pixel_id):
    """Create event-based audiences"""
    audiences = []
    
    event_configs = [
        {
            'name': 'KT - Form Starters',
            'event': 'InitiateCheckout',
            'retention_days': 30,
            'description': 'Started form but didn\'t complete'
        },
        {
            'name': 'KT - Converters (Leads)',
            'event': 'Lead',
            'retention_days': 180,
            'description': 'Completed form - Use for exclusion'
        }
    ]
    
    for config in event_configs:
        try:
            print(f"\n{Colors.OKCYAN}Creating: {config['name']}{Colors.ENDC}")
            
            params = {
                'name': config['name'],
                'description': config['description'],
                'subtype': 'WEBSITE',
                'retention_days': config['retention_days'],
                'rule': {
                    'inclusions': {
                        'operator': 'or',
                        'rules': [{
                            'event_sources': [{'id': pixel_id, 'type': 'pixel'}],
                            'retention_seconds': config['retention_days'] * 86400,
                            'filter': {
                                'operator': 'and',
                                'filters': [{
                                    'field': 'event',
                                    'operator': 'eq',
                                    'value': config['event']
                                }]
                            }
                        }]
                    }
                },
                'prefill': True
            }
            
            audience = account.create_custom_audience(params=params)
            print(f"{Colors.OKGREEN}✓ Created: {audience['id']}{Colors.ENDC}")
            audiences.append(audience)
            
        except Exception as e:
            print(f"{Colors.FAIL}✗ Error creating {config['name']}: {str(e)}{Colors.ENDC}")
    
    return audiences

def create_page_audiences(account, page_id):
    """Create page engagement audiences"""
    audiences = []
    
    page_configs = [
        {
            'name': 'KT - Page Engaged 30d',
            'retention_days': 30,
            'description': 'Recent page engagement'
        },
        {
            'name': 'KT - Page Engaged 90d', 
            'retention_days': 90,
            'description': 'Broader page engagement'
        }
    ]
    
    for config in page_configs:
        try:
            print(f"\n{Colors.OKCYAN}Creating: {config['name']}{Colors.ENDC}")
            
            params = {
                'name': config['name'],
                'description': config['description'],
                'subtype': 'ENGAGEMENT',
                'retention_days': config['retention_days'],
                'rule': {
                    'inclusions': {
                        'operator': 'or',
                        'rules': [{
                            'event_sources': [{'id': page_id, 'type': 'page'}],
                            'retention_seconds': config['retention_days'] * 86400,
                            'filter': {
                                'operator': 'and',
                                'filters': [{
                                    'field': 'event',
                                    'operator': 'eq',
                                    'value': 'page_engaged'
                                }]
                            }
                        }]
                    }
                },
                'prefill': True
            }
            
            audience = account.create_custom_audience(params=params)
            print(f"{Colors.OKGREEN}✓ Created: {audience['id']}{Colors.ENDC}")
            audiences.append(audience)
            
        except Exception as e:
            print(f"{Colors.FAIL}✗ Error creating {config['name']}: {str(e)}{Colors.ENDC}")
    
    return audiences

def main():
    parser = argparse.ArgumentParser(
        description='Create Kandidatentekort Custom Audiences',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', help='Ad account ID')
    parser.add_argument('--pixel', required=True, help='Facebook Pixel ID')
    parser.add_argument('--page', required=True, help='Facebook Page ID')
    parser.add_argument('--test', action='store_true', help='Test mode - create 1 audience')
    
    args = parser.parse_args()
    
    print(f"\n{Colors.HEADER}=== KANDIDATENTEKORT CUSTOM AUDIENCES ==={Colors.ENDC}")
    print(f"Account: {args.account}")
    print(f"Pixel: {args.pixel}")
    print(f"Page: {args.page}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize API
    try:
        FacebookAdsApi.init(access_token=args.token)
        account = AdAccount(args.account)
        print(f"{Colors.OKGREEN}✓ API initialized{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ API initialization failed: {str(e)}{Colors.ENDC}")
        sys.exit(1)
    
    # Create audiences
    all_audiences = []
    
    if args.test:
        # Test mode - create only one audience
        print(f"\n{Colors.WARNING}TEST MODE - Creating only 1 audience{Colors.ENDC}")
        try:
            params = {
                'name': 'KT - Test Audience Delete Me',
                'description': 'Test audience - can be deleted',
                'subtype': 'WEBSITE',
                'retention_days': 7,
                'rule': {
                    'inclusions': {
                        'operator': 'or',
                        'rules': [{
                            'event_sources': [{'id': args.pixel, 'type': 'pixel'}],
                            'retention_seconds': 7 * 86400,
                            'filter': {
                                'operator': 'and',
                                'filters': [{
                                    'field': 'event',
                                    'operator': 'eq',
                                    'value': 'PageView'
                                }]
                            }
                        }]
                    }
                },
                'prefill': True
            }
            
            audience = account.create_custom_audience(params=params)
            print(f"{Colors.OKGREEN}✓ Test audience created: {audience['id']}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}✗ Test failed: {str(e)}{Colors.ENDC}")
    else:
        # Create all audiences
        print(f"\n{Colors.OKBLUE}Creating Website Audiences...{Colors.ENDC}")
        website_audiences = create_website_audiences(account, args.pixel)
        all_audiences.extend(website_audiences)
        
        print(f"\n{Colors.OKBLUE}Creating Event Audiences...{Colors.ENDC}")
        event_audiences = create_event_audiences(account, args.pixel)
        all_audiences.extend(event_audiences)
        
        print(f"\n{Colors.OKBLUE}Creating Page Audiences...{Colors.ENDC}")
        page_audiences = create_page_audiences(account, args.page)
        all_audiences.extend(page_audiences)
        
        # Summary
        print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
        print(f"Total audiences created: {len(all_audiences)}")
        print(f"\n{Colors.OKCYAN}Created audiences:{Colors.ENDC}")
        for aud in all_audiences:
            print(f"  - {aud.get('name', 'Unknown')}")
        
        print(f"\n{Colors.WARNING}Note: Lookalike audiences must be created manually in Ads Manager{Colors.ENDC}")
        print(f"Base them on:")
        print(f"  - KT - All Website Visitors 180d")
        print(f"  - KT - Converters (Leads)")

if __name__ == "__main__":
    main()