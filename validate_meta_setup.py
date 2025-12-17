#!/usr/bin/env python3
"""
Validate Meta Ads Setup - Check Token, Page ID, and Pixel ID
"""

import argparse
import sys
from datetime import datetime
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.page import Page
from facebook_business.adobjects.adspixel import AdsPixel
from facebook_business.adobjects.adaccount import AdAccount

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def validate_setup(token, account_id, page_id=None, pixel_id=None):
    """Validate all components needed for Meta Ads"""
    print(f"\n{Colors.HEADER}=== META ADS SETUP VALIDATION ==={Colors.ENDC}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize API
    try:
        FacebookAdsApi.init(access_token=token)
        print(f"{Colors.OKGREEN}✓ Token is valid{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ Token validation failed: {str(e)}{Colors.ENDC}")
        return False

    # Check user permissions
    try:
        me = User(fbid='me')
        permissions = me.remote_read(fields=['permissions'])
        perms = {p['permission']: p['status'] for p in permissions['permissions']['data']}
        
        print(f"\n{Colors.OKBLUE}Permissions:{Colors.ENDC}")
        required_perms = ['ads_management', 'ads_read', 'pages_read_engagement']
        for perm in required_perms:
            if perm in perms and perms[perm] == 'granted':
                print(f"  {Colors.OKGREEN}✓ {perm}: granted{Colors.ENDC}")
            else:
                print(f"  {Colors.FAIL}✗ {perm}: not granted{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.WARNING}⚠ Could not check permissions: {str(e)}{Colors.ENDC}")

    # Check ad account
    try:
        ad_account = AdAccount(account_id)
        account_info = ad_account.api_get(fields=['name', 'account_status', 'currency'])
        print(f"\n{Colors.OKBLUE}Ad Account:{Colors.ENDC}")
        print(f"  ID: {account_id}")
        print(f"  Name: {account_info.get('name', 'Unknown')}")
        print(f"  Status: {account_info.get('account_status', 'Unknown')}")
        print(f"  Currency: {account_info.get('currency', 'Unknown')}")
        print(f"  {Colors.OKGREEN}✓ Ad account accessible{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}✗ Ad account error: {str(e)}{Colors.ENDC}")
        return False

    # Find available pages
    try:
        pages = me.get_accounts(fields=['name', 'id', 'access_token'])
        print(f"\n{Colors.OKBLUE}Available Pages:{Colors.ENDC}")
        page_found = False
        for page in pages:
            print(f"  ID: {page['id']} - Name: {page['name']}")
            if page_id and page['id'] == page_id:
                page_found = True
                print(f"  {Colors.OKGREEN}✓ This is your specified page{Colors.ENDC}")
        
        if page_id and not page_found:
            print(f"  {Colors.WARNING}⚠ Specified page {page_id} not found in available pages{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.WARNING}⚠ Could not list pages: {str(e)}{Colors.ENDC}")

    # Check page details if provided
    if page_id:
        try:
            page = Page(page_id)
            page_info = page.api_get(fields=['name', 'id'])
            print(f"\n{Colors.OKBLUE}Page Validation:{Colors.ENDC}")
            print(f"  ID: {page_info['id']}")
            print(f"  Name: {page_info['name']}")
            print(f"  {Colors.OKGREEN}✓ Page accessible{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}✗ Page validation failed: {str(e)}{Colors.ENDC}")

    # Find available pixels
    try:
        pixels = ad_account.get_ads_pixels(fields=['name', 'id', 'code'])
        print(f"\n{Colors.OKBLUE}Available Pixels:{Colors.ENDC}")
        pixel_found = False
        for pixel in pixels:
            print(f"  ID: {pixel['id']} - Name: {pixel['name']}")
            if pixel_id and pixel['id'] == pixel_id:
                pixel_found = True
                print(f"  {Colors.OKGREEN}✓ This is your specified pixel{Colors.ENDC}")
        
        if pixel_id and not pixel_found:
            print(f"  {Colors.WARNING}⚠ Specified pixel {pixel_id} not found{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.WARNING}⚠ Could not list pixels: {str(e)}{Colors.ENDC}")

    # Check pixel details if provided
    if pixel_id:
        try:
            pixel = AdsPixel(pixel_id)
            pixel_info = pixel.api_get(fields=['name', 'id', 'last_fired_time'])
            print(f"\n{Colors.OKBLUE}Pixel Validation:{Colors.ENDC}")
            print(f"  ID: {pixel_info['id']}")
            print(f"  Name: {pixel_info['name']}")
            if 'last_fired_time' in pixel_info:
                print(f"  Last fired: {pixel_info['last_fired_time']}")
                print(f"  {Colors.OKGREEN}✓ Pixel is active{Colors.ENDC}")
            else:
                print(f"  {Colors.WARNING}⚠ Pixel may not be installed{Colors.ENDC}")
        except Exception as e:
            print(f"\n{Colors.FAIL}✗ Pixel validation failed: {str(e)}{Colors.ENDC}")

    # Summary
    print(f"\n{Colors.HEADER}=== READY TO PROCEED? ==={Colors.ENDC}")
    print(f"\n{Colors.OKGREEN}✓ Token is valid")
    print(f"✓ Ad account {account_id} is accessible")
    
    if not page_id:
        print(f"\n{Colors.WARNING}⚠ No Page ID provided")
        print(f"  Choose one from the list above{Colors.ENDC}")
    
    if not pixel_id:
        print(f"\n{Colors.WARNING}⚠ No Pixel ID provided")
        print(f"  Choose one from the list above{Colors.ENDC}")
    
    print(f"\n{Colors.OKCYAN}Next steps:")
    print(f"1. Note your Page ID and Pixel ID from above")
    print(f"2. Run: python meta_ads_create_audiences.py --token YOUR_TOKEN --account {account_id} --pixel PIXEL_ID --page PAGE_ID")
    print(f"3. Then: python meta_ads_create_campaign.py --token YOUR_TOKEN --account {account_id} --page PAGE_ID{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='Validate Meta Ads setup components',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', 
                       help='Ad account ID (default: act_1236576254450117)')
    parser.add_argument('--page', help='Facebook Page ID (optional)')
    parser.add_argument('--pixel', help='Facebook Pixel ID (optional)')
    
    args = parser.parse_args()
    
    try:
        validate_setup(args.token, args.account, args.page, args.pixel)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {str(e)}{Colors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main()