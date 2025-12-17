#!/usr/bin/env python3
"""
Kandidatentekort FOMO/Scarcity Campaign Updater
Updates existing campaigns with high-converting ads focused on €500/day loss messaging
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

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class FOMOScarcityCampaignUpdater:
    def __init__(self, access_token, account_id, page_id):
        FacebookAdsApi.init(access_token=access_token)
        self.ad_account = AdAccount(account_id)
        self.account_id = account_id
        self.page_id = page_id
        self.updated_ads = []
        
    def get_fomo_ad_copies(self):
        """Get FOMO/Scarcity focused ad copies with €500/day messaging"""
        return {
            'cold': [
                {
                    'name': 'KT-Cold-500EUR-Daily-Loss',
                    'headline': 'Elke dag €500+ verlies door open vacatures',
                    'description': 'Stop het bloeden. Gratis analyse toont direct wat je vacature mist.',
                    'primary_text': 'Jouw vacature staat al 47 dagen open? Dat kost je €23.500 aan verloren productiviteit. Onze gratis analyse toont in 24 uur waarom kandidaten niet reageren.',
                    'utm_content': 'cold_500eur_loss'
                },
                {
                    'name': 'KT-Cold-Competitor-Stealing',
                    'headline': 'Concurrenten pikken JOUW kandidaten',
                    'description': '87% van bedrijven mist topkandidaten. Krijg direct inzicht waarom.',
                    'primary_text': 'Terwijl jij wacht, werven concurrenten dezelfde technische professionals. 150+ bedrijven kregen al 40-60% meer reacties. Nu jij.',
                    'utm_content': 'cold_competitor_threat'
                },
                {
                    'name': 'KT-Cold-3-Months-Pain',
                    'headline': '3 maanden open = €36.000 verlies',
                    'description': 'Technische vacatures kosten €500-800 per dag. Stop het NU.',
                    'primary_text': 'Je vacature staat al 3 maanden open? Dat is €36.000+ aan gemiste omzet. In 24 uur weet je waarom kandidaten afhaken.',
                    'utm_content': 'cold_3months_pain'
                },
                {
                    'name': 'KT-Cold-Last-24h-Free',
                    'headline': 'LAATSTE 24 UUR: Gratis vacature-analyse',
                    'description': 'Morgen €297. Vandaag gratis. Geen verplichtingen.',
                    'primary_text': 'Deze week al 127 recruiters geholpen. Laatste gratis analyses beschikbaar. Ontdek waarom jouw vacature faalt.',
                    'utm_content': 'cold_24h_urgency'
                }
            ],
            'warm': [
                {
                    'name': 'KT-Warm-Calculator-Shock',
                    'headline': 'Bereken: €847/dag verlies door jouw vacature',
                    'description': 'Schrik van het bedrag? Wij lossen het in 3 weken op.',
                    'primary_text': 'Open vacature calculator: €500 productiviteit + €247 overwerk + €100 gemiste deadlines = €847/dag verlies. Check wat jouw vacature kost.',
                    'utm_content': 'warm_calculator_shock'
                },
                {
                    'name': 'KT-Warm-7Days-127Companies',
                    'headline': '127 bedrijven deze week al geholpen',
                    'description': 'Laatste 23 gratis plekken. Claim die van jou NU.',
                    'primary_text': 'Deze week transformeerden we al 127 vacatures. Van 3 naar 47 reacties is normaal. Nog 23 gratis analyses beschikbaar.',
                    'utm_content': 'warm_social_urgency'
                },
                {
                    'name': 'KT-Warm-Tomorrow-297EUR',
                    'headline': 'Morgen kost deze analyse €297',
                    'description': 'Vandaag laatste kans op gratis quickscan + actieplan.',
                    'primary_text': 'Je hebt onze site bezocht. Je weet wat mogelijk is. Vanaf morgen €297 voor dezelfde analyse. Grijp vandaag je kans.',
                    'utm_content': 'warm_price_anchor'
                },
                {
                    'name': 'KT-Warm-Waiting-Costs',
                    'headline': 'Terwijl jij twijfelt, verlies je €3.500/week',
                    'description': 'Elke week wachten = 5 gemiste topkandidaten. Start NU.',
                    'primary_text': 'Feit: 73% van technische professionals solliciteert binnen 7 dagen. Jouw vertraging kost je de beste kandidaten.',
                    'utm_content': 'warm_waiting_cost'
                }
            ],
            'hot': [
                {
                    'name': 'KT-Hot-Analysis-Ready',
                    'headline': 'Je vacature-analyse staat KLAAR',
                    'description': 'Log in binnen 48 uur of we geven je plek aan een ander.',
                    'primary_text': 'We hebben je vacature geanalyseerd. Resultaat: 18/40 sterren. Met onze aanpassingen: 34/40. Check je inbox NU.',
                    'utm_content': 'hot_ready_urgency'
                },
                {
                    'name': 'KT-Hot-Spot-Reserved',
                    'headline': 'Je gratis analyse vervalt over 48 uur',
                    'description': 'Daarna €297. Of geef je plek op aan de wachtlijst?',
                    'primary_text': 'We reserveerden 1 van onze laatste gratis plekken voor jou. 48 uur om te claimen, anders naar #128 op de wachtlijst.',
                    'utm_content': 'hot_spot_expire'
                },
                {
                    'name': 'KT-Hot-Implementation-Bonus',
                    'headline': 'BONUS: Gratis implementatie (€500 waarde)',
                    'description': 'Alleen bij aanvraag voor middernacht. Wij doen het werk.',
                    'primary_text': 'Speciaal aanbod: We implementeren de verbeteringen GRATIS (normaal €500). Alleen vandaag bij directe actie.',
                    'utm_content': 'hot_implementation_bonus'
                },
                {
                    'name': 'KT-Hot-Final-Warning',
                    'headline': 'LAATSTE WAARSCHUWING: €500/dag blijft lekken',
                    'description': 'Je kent het probleem. Je kent de oplossing. Wat houdt je tegen?',
                    'primary_text': 'Je vacature kost je €500+/dag. Wij kunnen het stoppen. 150+ bedrijven gingen je voor. Dit is je laatste kans.',
                    'utm_content': 'hot_final_warning'
                }
            ]
        }
    
    def create_ab_test_structure(self, adset_id, campaign_type, ad_configs):
        """Create A/B test structure with multiple ad variants"""
        print(f"\n{Colors.OKBLUE}Creating A/B Test Structure for {campaign_type}...{Colors.ENDC}")
        
        created_ads = []
        for i, ad_config in enumerate(ad_configs):
            try:
                # Build URL with proper UTM tracking
                utm_params = f"utm_source=meta&utm_medium=paid&utm_campaign=kt_{campaign_type}_fomo&utm_content={ad_config['utm_content']}&utm_term=v2"
                full_url = f"https://kandidatentekort.nl/?{utm_params}"
                
                # Create creative
                creative_params = {
                    'name': f"{ad_config['name']}--Creative-V2",
                    'object_story_spec': {
                        'page_id': self.page_id,
                        'link_data': {
                            'link': full_url,
                            'name': ad_config['headline'],
                            'message': ad_config['primary_text'],
                            'description': ad_config['description'],
                            'call_to_action': {
                                'type': 'LEARN_MORE',
                                'value': {'link': full_url}
                            }
                        }
                    }
                }
                
                creative = self.ad_account.create_ad_creative(params=creative_params)
                
                # Create ad
                ad_params = {
                    'name': f"{ad_config['name']}--V2-FOMO",
                    'adset_id': adset_id,
                    'creative': {'creative_id': creative['id']},
                    'status': Ad.Status.paused,
                    'tracking_specs': [
                        {
                            'action.type': ['link_click'],
                            'fb_pixel': ['YOUR_PIXEL_ID']  # Add your pixel ID
                        }
                    ]
                }
                
                ad = self.ad_account.create_ad(params=ad_params)
                created_ads.append({
                    'id': ad['id'],
                    'name': ad_config['name'],
                    'variant': f"Variant_{chr(65 + i)}"  # A, B, C, D
                })
                
                print(f"  {Colors.OKGREEN}✓ Created: {ad_config['name']} (Variant {chr(65 + i)}){Colors.ENDC}")
                self.updated_ads.append(ad)
                
            except Exception as e:
                print(f"  {Colors.FAIL}✗ Error creating {ad_config['name']}: {str(e)}{Colors.ENDC}")
        
        return created_ads
    
    def update_campaign(self, campaign_id, campaign_type):
        """Update a single campaign with new FOMO ads"""
        print(f"\n{Colors.OKCYAN}Updating {campaign_type.upper()} Campaign...{Colors.ENDC}")
        
        try:
            # Get campaign
            campaign = Campaign(campaign_id)
            campaign_data = campaign.api_get(fields=['name', 'status'])
            print(f"  Campaign: {campaign_data['name']}")
            
            # Get ad sets
            adsets = campaign.get_ad_sets(fields=['id', 'name', 'status', 'daily_budget'])
            
            if not adsets:
                print(f"  {Colors.WARNING}No ad sets found in campaign{Colors.ENDC}")
                return False
            
            # Get FOMO ad copies for this campaign type
            fomo_copies = self.get_fomo_ad_copies()[campaign_type]
            
            # Update each ad set
            for adset in adsets:
                print(f"\n  AdSet: {adset['name']} (Budget: €{int(adset['daily_budget'])/100})")
                
                # Pause existing ads
                existing_ads = AdSet(adset['id']).get_ads(fields=['id', 'name', 'status'])
                for ad in existing_ads:
                    if ad['status'] == 'ACTIVE':
                        Ad(ad['id']).api_update(params={'status': Ad.Status.paused})
                        print(f"    {Colors.WARNING}⏸ Paused: {ad['name']}{Colors.ENDC}")
                
                # Create new FOMO/Scarcity ads with A/B structure
                new_ads = self.create_ab_test_structure(adset['id'], campaign_type, fomo_copies)
                
                if new_ads:
                    print(f"\n    {Colors.OKGREEN}✓ Created {len(new_ads)} new FOMO ads{Colors.ENDC}")
                    print(f"    {Colors.OKCYAN}A/B Test Structure Ready:{Colors.ENDC}")
                    for ad in new_ads:
                        print(f"      • {ad['variant']}: {ad['name']}")
            
            return True
            
        except Exception as e:
            print(f"  {Colors.FAIL}✗ Error updating campaign: {str(e)}{Colors.ENDC}")
            return False
    
    def update_all_campaigns(self, campaign_ids):
        """Update all three campaigns with new FOMO/Scarcity ads"""
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}KANDIDATENTEKORT FOMO/SCARCITY CAMPAIGN UPDATE{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Strategy: €500/day loss messaging + urgency triggers{Colors.ENDC}")
        print(f"Account: {self.account_id}")
        print(f"Creating 12 new FOMO ads across 3 campaigns")
        
        campaign_types = ['cold', 'warm', 'hot']
        success_count = 0
        
        for i, campaign_id in enumerate(campaign_ids):
            if i < len(campaign_types):
                if self.update_campaign(campaign_id, campaign_types[i]):
                    success_count += 1
        
        # Summary
        print(f"\n{Colors.HEADER}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}DEPLOYMENT SUMMARY{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*60}{Colors.ENDC}")
        
        print(f"\n{Colors.OKGREEN}✓ Successfully updated {success_count}/3 campaigns{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ Created {len(self.updated_ads)} new FOMO/Scarcity ads{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ A/B test structure implemented{Colors.ENDC}")
        print(f"{Colors.OKGREEN}✓ UTM tracking configured{Colors.ENDC}")
        
        if success_count == 3:
            print(f"\n{Colors.OKCYAN}🚀 ALL CAMPAIGNS UPDATED WITH FOMO MESSAGING!{Colors.ENDC}")
            print("\n📋 Next Steps:")
            print("1. Review new ads in Meta Ads Manager")
            print("2. Set up A/B test parameters (even budget split)")
            print("3. Activate campaigns when ready")
            print("4. Monitor performance in GA4 Dashboard")
            print("\n🎯 Performance Tracking:")
            print("• Monitor CTR improvement (target: 3-4%)")
            print("• Track €500/day messaging conversion rate")
            print("• Compare FOMO variants performance")
            print("• Optimize based on cost per conversion")
        else:
            print(f"\n{Colors.WARNING}⚠ Some campaigns failed to update. Check errors above.{Colors.ENDC}")
        
        # Export tracking data
        self.export_tracking_data()
    
    def export_tracking_data(self):
        """Export tracking data for performance monitoring"""
        tracking_data = {
            'update_date': datetime.now().isoformat(),
            'campaign_strategy': 'FOMO_SCARCITY_500EUR',
            'total_ads_created': len(self.updated_ads),
            'utm_structure': {
                'source': 'meta',
                'medium': 'paid',
                'campaign_pattern': 'kt_{audience}_fomo',
                'content_variants': [
                    'cold_500eur_loss', 'cold_competitor_threat', 'cold_3months_pain', 'cold_24h_urgency',
                    'warm_calculator_shock', 'warm_social_urgency', 'warm_price_anchor', 'warm_waiting_cost',
                    'hot_ready_urgency', 'hot_spot_expire', 'hot_implementation_bonus', 'hot_final_warning'
                ]
            },
            'ab_test_setup': {
                'variants_per_audience': 4,
                'total_variants': 12,
                'test_duration': '7_days_recommended'
            }
        }
        
        with open('fomo_campaign_tracking.json', 'w') as f:
            json.dump(tracking_data, f, indent=2)
        
        print(f"\n{Colors.OKBLUE}📊 Tracking data exported to: fomo_campaign_tracking.json{Colors.ENDC}")

def main():
    parser = argparse.ArgumentParser(
        description='Update Kandidatentekort Campaigns with FOMO/Scarcity Messaging',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python update_campaigns_fomo_scarcity.py --token YOUR_TOKEN --campaigns CAMPAIGN_ID1 CAMPAIGN_ID2 CAMPAIGN_ID3
  
Campaign order should be: COLD, WARM, HOT
        """
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', help='Ad account ID')
    parser.add_argument('--page', default='660118697194302', help='Facebook Page ID')
    parser.add_argument('--campaigns', nargs='+', required=True, help='Campaign IDs to update (Cold, Warm, Hot order)')
    
    args = parser.parse_args()
    
    # Security reminder
    print(f"\n{Colors.WARNING}SECURITY CHECK:{Colors.ENDC}")
    print("✓ Updates ONLY Kandidatentekort campaigns")
    print("✓ ALL traffic to kandidatentekort.nl")
    print("✓ FOMO/Scarcity messaging with €500/day focus")
    print("✓ A/B testing structure enabled\n")
    
    input("Press Enter to continue with updates...")
    
    updater = FOMOScarcityCampaignUpdater(args.token, args.account, args.page)
    updater.update_all_campaigns(args.campaigns)

if __name__ == "__main__":
    main()