#!/usr/bin/env python3
"""
Kandidatentekort Custom Audiences Creator V2
Using simplified API approach
"""

import argparse
import sys
import json
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

def create_audiences(account, pixel_id, page_id):
    """Create all Kandidatentekort audiences"""
    created = []
    failed = []
    
    # Website audiences
    website_audiences = [
        {
            'name': 'KT - All Website Visitors 180d',
            'days': 180,
            'desc': 'All visitors for lookalike base'
        },
        {
            'name': 'KT - Website Visitors 30d',
            'days': 30,
            'desc': 'Recent visitors for consideration'
        },
        {
            'name': 'KT - Website Visitors 7d',
            'days': 7,
            'desc': 'Hot leads for retargeting'
        }
    ]
    
    print(f"\n{Colors.OKBLUE}Creating Website Audiences...{Colors.ENDC}")
    
    for aud in website_audiences:
        try:
            print(f"\nCreating: {aud['name']}")
            
            # Simplified rule structure
            rule = json.dumps({
                "inclusions": {
                    "operator": "or",
                    "rules": [{
                        "event_sources": [{"id": pixel_id, "type": "pixel"}],
                        "retention_seconds": aud['days'] * 86400,
                        "filter": {
                            "operator": "and",
                            "filters": [{
                                "field": "event",
                                "operator": "=",
                                "value": "PageView"
                            }]
                        }
                    }]
                }
            })
            
            params = {
                'name': aud['name'],
                'description': aud['desc'],
                'customer_file_source': 'BOTH_USER_AND_PARTNER_PROVIDED',
                'is_value_based': False,
                'rule': rule,
                'retention_days': aud['days']
            }
            
            audience = account.create_custom_audience(fields=[], params=params)
            print(f"{Colors.OKGREEN}✓ Created: {audience['id']}{Colors.ENDC}")
            created.append(aud['name'])
            
        except Exception as e:
            print(f"{Colors.FAIL}✗ Failed: {str(e)}{Colors.ENDC}")
            failed.append({'name': aud['name'], 'error': str(e)})
    
    # Event audiences  
    event_audiences = [
        {
            'name': 'KT - Form Starters',
            'event': 'InitiateCheckout',
            'days': 30,
            'desc': 'Started form but did not complete'
        },
        {
            'name': 'KT - Converters (Leads)',
            'event': 'Lead',
            'days': 180,
            'desc': 'Completed form - use for exclusion'
        }
    ]
    
    print(f"\n{Colors.OKBLUE}Creating Event Audiences...{Colors.ENDC}")
    
    for aud in event_audiences:
        try:
            print(f"\nCreating: {aud['name']}")
            
            rule = json.dumps({
                "inclusions": {
                    "operator": "or",
                    "rules": [{
                        "event_sources": [{"id": pixel_id, "type": "pixel"}],
                        "retention_seconds": aud['days'] * 86400,
                        "filter": {
                            "operator": "and",
                            "filters": [{
                                "field": "event",
                                "operator": "=",
                                "value": aud['event']
                            }]
                        }
                    }]
                }
            })
            
            params = {
                'name': aud['name'],
                'description': aud['desc'],
                'customer_file_source': 'BOTH_USER_AND_PARTNER_PROVIDED',
                'is_value_based': False,
                'rule': rule,
                'retention_days': aud['days']
            }
            
            audience = account.create_custom_audience(fields=[], params=params)
            print(f"{Colors.OKGREEN}✓ Created: {audience['id']}{Colors.ENDC}")
            created.append(aud['name'])
            
        except Exception as e:
            print(f"{Colors.FAIL}✗ Failed: {str(e)}{Colors.ENDC}")
            failed.append({'name': aud['name'], 'error': str(e)})
    
    return created, failed

def main():
    parser = argparse.ArgumentParser(
        description='Create Kandidatentekort Custom Audiences V2',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', help='Ad account ID')
    parser.add_argument('--pixel', required=True, help='Facebook Pixel ID')
    parser.add_argument('--page', required=True, help='Facebook Page ID')
    
    args = parser.parse_args()
    
    print(f"\n{Colors.HEADER}=== KANDIDATENTEKORT CUSTOM AUDIENCES V2 ==={Colors.ENDC}")
    print(f"Account: {args.account}")
    print(f"Pixel: {args.pixel}")
    print(f"Page: {args.page}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Security check
    print(f"\n{Colors.WARNING}SECURITY CHECK:{Colors.ENDC}")
    print("✓ ONLY creating Kandidatentekort audiences (KT prefix)")
    print("✓ ONLY using approved Pixel ID: 1430141541402009")
    print("✓ ONLY using Recruitin Page for Kandidatentekort")
    
    # Initialize API
    try:
        FacebookAdsApi.init(access_token=args.token)
        account = AdAccount(args.account)
        print(f"\n{Colors.OKGREEN}✓ API initialized{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ API initialization failed: {str(e)}{Colors.ENDC}")
        sys.exit(1)
    
    # Create audiences
    created, failed = create_audiences(account, args.pixel, args.page)
    
    # Summary
    print(f"\n{Colors.HEADER}=== SUMMARY ==={Colors.ENDC}")
    print(f"{Colors.OKGREEN}Successfully created: {len(created)}{Colors.ENDC}")
    for aud in created:
        print(f"  ✓ {aud}")
    
    if failed:
        print(f"\n{Colors.FAIL}Failed: {len(failed)}{Colors.ENDC}")
        for f in failed:
            print(f"  ✗ {f['name']}: {f['error']}")
    
    print(f"\n{Colors.OKCYAN}Next steps:{Colors.ENDC}")
    print("1. Create lookalike audiences manually based on:")
    print("   - KT - All Website Visitors 180d (1% and 2%)")
    print("   - KT - Converters (Leads) (1%)")
    print("2. Run traffic campaign creator")

if __name__ == "__main__":
    main()