#!/usr/bin/env python3
"""
FOMO Campaign Performance Tracker - Kandidatentekort
Real-time monitoring of €500/day campaign performance
"""

import argparse
import requests
import json
from datetime import datetime, timedelta
from tabulate import tabulate

# Configuration
API_VERSION = "v18.0"
BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class FOMOPerformanceTracker:
    def __init__(self, access_token, account_id):
        self.access_token = access_token
        self.account_id = account_id
        self.performance_data = {}
        
    def get_campaign_insights(self, hours=24):
        """Get performance data for FOMO campaigns"""
        
        # Calculate date range
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        # Get all campaigns with KT prefix
        campaigns_url = f"{BASE_URL}/{self.account_id}/campaigns"
        params = {
            "fields": "id,name,status",
            "filtering": json.dumps([{"field": "name", "operator": "CONTAIN", "value": "KT"}]),
            "access_token": self.access_token
        }
        
        response = requests.get(campaigns_url, params=params)
        
        if response.status_code != 200:
            print(f"{Colors.FAIL}Error getting campaigns: {response.text}{Colors.ENDC}")
            return
        
        campaigns = response.json().get('data', [])
        
        for campaign in campaigns:
            self.get_campaign_performance(campaign, start_time, end_time)
    
    def get_campaign_performance(self, campaign, start_time, end_time):
        """Get detailed performance for a single campaign"""
        
        # Determine campaign type from name
        campaign_name = campaign['name'].lower()
        if 'cold' in campaign_name:
            campaign_type = 'COLD'
        elif 'warm' in campaign_name or 'consideration' in campaign_name:
            campaign_type = 'WARM'
        elif 'hot' in campaign_name or 'retarget' in campaign_name:
            campaign_type = 'HOT'
        else:
            campaign_type = 'UNKNOWN'
        
        # Get campaign insights
        insights_url = f"{BASE_URL}/{campaign['id']}/insights"
        params = {
            "fields": "impressions,clicks,ctr,cpc,spend,conversions,cost_per_conversion",
            "time_range": json.dumps({
                "since": start_time.strftime("%Y-%m-%d"),
                "until": end_time.strftime("%Y-%m-%d")
            }),
            "access_token": self.access_token
        }
        
        response = requests.get(insights_url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                insights = data[0]
                self.performance_data[campaign['id']] = {
                    'name': campaign['name'],
                    'type': campaign_type,
                    'status': campaign['status'],
                    'insights': insights
                }
                
                # Get ad-level performance
                self.get_ad_performance(campaign['id'], start_time, end_time)
    
    def get_ad_performance(self, campaign_id, start_time, end_time):
        """Get performance data for individual ads"""
        
        # Get all ads in campaign
        ads_url = f"{BASE_URL}/{campaign_id}/ads"
        params = {
            "fields": "id,name,status",
            "access_token": self.access_token
        }
        
        response = requests.get(ads_url, params=params)
        
        if response.status_code == 200:
            ads = response.json().get('data', [])
            
            ad_performances = []
            for ad in ads:
                # Get ad insights
                ad_insights_url = f"{BASE_URL}/{ad['id']}/insights"
                insights_params = {
                    "fields": "impressions,clicks,ctr,cpc,spend,conversions,cost_per_conversion",
                    "time_range": json.dumps({
                        "since": start_time.strftime("%Y-%m-%d"),
                        "until": end_time.strftime("%Y-%m-%d")
                    }),
                    "access_token": self.access_token
                }
                
                insights_response = requests.get(ad_insights_url, params=insights_params)
                
                if insights_response.status_code == 200:
                    insights_data = insights_response.json().get('data', [])
                    if insights_data:
                        ad_performances.append({
                            'name': ad['name'],
                            'status': ad['status'],
                            'insights': insights_data[0]
                        })
            
            if campaign_id in self.performance_data:
                self.performance_data[campaign_id]['ads'] = ad_performances
    
    def analyze_fomo_performance(self):
        """Analyze FOMO messaging performance"""
        
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}KANDIDATENTEKORT FOMO CAMPAIGN PERFORMANCE ANALYSIS{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"\n{Colors.BOLD}Strategy: €500/day loss messaging{Colors.ENDC}")
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Campaign Level Summary
        print(f"\n{Colors.OKBLUE}📊 CAMPAIGN LEVEL PERFORMANCE{Colors.ENDC}")
        print(f"{'-'*80}")
        
        campaign_summary = []
        total_spend = 0
        total_clicks = 0
        total_conversions = 0
        
        for campaign_id, data in self.performance_data.items():
            insights = data['insights']
            
            impressions = int(insights.get('impressions', 0))
            clicks = int(insights.get('clicks', 0))
            spend = float(insights.get('spend', 0))
            ctr = float(insights.get('ctr', 0))
            cpc = float(insights.get('cpc', 0))
            conversions = int(insights.get('conversions', {}).get('value', 0))
            cpa = float(insights.get('cost_per_conversion', {}).get('value', 0))
            
            total_spend += spend
            total_clicks += clicks
            total_conversions += conversions
            
            # Performance indicators
            ctr_indicator = "🟢" if ctr >= 3 else "🟡" if ctr >= 2 else "🔴"
            cpc_indicator = "🟢" if cpc <= 2 else "🟡" if cpc <= 3 else "🔴"
            cpa_indicator = "🟢" if cpa <= 10 else "🟡" if cpa <= 15 else "🔴"
            
            campaign_summary.append([
                data['type'],
                f"{impressions:,}",
                f"{clicks:,}",
                f"{ctr_indicator} {ctr:.2f}%",
                f"{cpc_indicator} €{cpc:.2f}",
                f"€{spend:.2f}",
                conversions,
                f"{cpa_indicator} €{cpa:.2f}" if cpa > 0 else "-"
            ])
        
        headers = ["Type", "Impr", "Clicks", "CTR", "CPC", "Spend", "Conv", "CPA"]
        print(tabulate(campaign_summary, headers=headers, tablefmt="grid"))
        
        # Ad Level Performance (Top Performers)
        print(f"\n{Colors.OKGREEN}🏆 TOP PERFORMING FOMO ADS{Colors.ENDC}")
        print(f"{'-'*80}")
        
        all_ads = []
        for campaign_id, data in self.performance_data.items():
            if 'ads' in data:
                for ad in data['ads']:
                    if ad['status'] == 'ACTIVE':
                        insights = ad['insights']
                        ctr = float(insights.get('ctr', 0))
                        if ctr > 0:
                            all_ads.append({
                                'campaign_type': data['type'],
                                'name': ad['name'],
                                'ctr': ctr,
                                'cpc': float(insights.get('cpc', 0)),
                                'spend': float(insights.get('spend', 0)),
                                'conversions': int(insights.get('conversions', {}).get('value', 0))
                            })
        
        # Sort by CTR and show top 5
        top_ads = sorted(all_ads, key=lambda x: x['ctr'], reverse=True)[:5]
        
        top_ads_table = []
        for ad in top_ads:
            # Extract FOMO type from ad name
            fomo_type = "Unknown"
            if "500EUR" in ad['name']:
                fomo_type = "€500/day Loss"
            elif "Competitor" in ad['name']:
                fomo_type = "Competitor Threat"
            elif "LastChance" in ad['name'] or "24h" in ad['name']:
                fomo_type = "Urgency/Scarcity"
            elif "Calculator" in ad['name']:
                fomo_type = "Cost Calculator"
            
            top_ads_table.append([
                ad['campaign_type'],
                fomo_type,
                f"{ad['ctr']:.2f}%",
                f"€{ad['cpc']:.2f}",
                ad['conversions']
            ])
        
        headers = ["Audience", "FOMO Type", "CTR", "CPC", "Conv"]
        print(tabulate(top_ads_table, headers=headers, tablefmt="grid"))
        
        # FOMO Message Analysis
        print(f"\n{Colors.OKCYAN}💡 FOMO MESSAGE EFFECTIVENESS{Colors.ENDC}")
        print(f"{'-'*80}")
        
        fomo_analysis = {
            "€500/day Loss": {"clicks": 0, "conversions": 0, "spend": 0},
            "Competitor Threat": {"clicks": 0, "conversions": 0, "spend": 0},
            "Urgency/Scarcity": {"clicks": 0, "conversions": 0, "spend": 0},
            "Cost Calculator": {"clicks": 0, "conversions": 0, "spend": 0}
        }
        
        # Aggregate by FOMO type
        for campaign_id, data in self.performance_data.items():
            if 'ads' in data:
                for ad in data['ads']:
                    insights = ad['insights']
                    
                    # Categorize by ad name
                    if "500EUR" in ad['name'] or "500+/dag" in ad['name']:
                        fomo_type = "€500/day Loss"
                    elif "Competitor" in ad['name'] or "concurrenten" in ad['name']:
                        fomo_type = "Competitor Threat"
                    elif "LastChance" in ad['name'] or "24h" in ad['name'] or "48h" in ad['name']:
                        fomo_type = "Urgency/Scarcity"
                    elif "Calculator" in ad['name'] or "€847" in ad['name']:
                        fomo_type = "Cost Calculator"
                    else:
                        continue
                    
                    fomo_analysis[fomo_type]["clicks"] += int(insights.get('clicks', 0))
                    fomo_analysis[fomo_type]["conversions"] += int(insights.get('conversions', {}).get('value', 0))
                    fomo_analysis[fomo_type]["spend"] += float(insights.get('spend', 0))
        
        fomo_table = []
        for fomo_type, metrics in fomo_analysis.items():
            if metrics['clicks'] > 0:
                cvr = (metrics['conversions'] / metrics['clicks']) * 100
                cpa = metrics['spend'] / metrics['conversions'] if metrics['conversions'] > 0 else 0
                
                effectiveness = "🟢 High" if cvr >= 5 else "🟡 Medium" if cvr >= 2 else "🔴 Low"
                
                fomo_table.append([
                    fomo_type,
                    metrics['clicks'],
                    metrics['conversions'],
                    f"{cvr:.1f}%",
                    f"€{cpa:.2f}" if cpa > 0 else "-",
                    effectiveness
                ])
        
        headers = ["FOMO Type", "Clicks", "Conv", "CVR", "CPA", "Effectiveness"]
        print(tabulate(fomo_table, headers=headers, tablefmt="grid"))
        
        # Recommendations
        print(f"\n{Colors.WARNING}📈 OPTIMIZATION RECOMMENDATIONS{Colors.ENDC}")
        print(f"{'-'*80}")
        
        if total_spend > 0:
            overall_ctr = (total_clicks / total_spend) * 100
            overall_cpa = total_spend / total_conversions if total_conversions > 0 else 0
            
            print(f"\n✅ Overall Performance:")
            print(f"   • Total Spend: €{total_spend:.2f}")
            print(f"   • Total Conversions: {total_conversions}")
            print(f"   • Average CPA: €{overall_cpa:.2f}")
            
            print(f"\n🎯 Action Items:")
            
            # Find best performing FOMO type
            best_fomo = max(fomo_analysis.items(), 
                          key=lambda x: x[1]['conversions'] / x[1]['spend'] if x[1]['spend'] > 0 else 0)
            
            print(f"   1. Scale '{best_fomo[0]}' messaging - best ROI")
            print(f"   2. A/B test new variations of €500/day loss angle")
            print(f"   3. Increase urgency in retargeting (HOT) ads")
            
            if overall_ctr < 3:
                print(f"   4. {Colors.WARNING}CTR below target - test new headlines{Colors.ENDC}")
            
            if overall_cpa > 15:
                print(f"   5. {Colors.WARNING}CPA above target - review landing page{Colors.ENDC}")
        
        print(f"\n{Colors.OKBLUE}💰 Projected Monthly Impact:{Colors.ENDC}")
        if total_conversions > 0 and total_spend > 0:
            daily_conversions = total_conversions / (total_spend / 100)  # Assuming €100/day budget
            monthly_conversions = daily_conversions * 30
            monthly_value = monthly_conversions * 500  # €500 saved per conversion
            
            print(f"   • Projected conversions: {int(monthly_conversions)}")
            print(f"   • Value delivered: €{int(monthly_value):,}")
            print(f"   • ROI: {int((monthly_value / 3000) * 100)}%")  # Assuming €3000 monthly ad spend

def main():
    parser = argparse.ArgumentParser(
        description='Track FOMO Campaign Performance'
    )
    
    parser.add_argument('--token', required=True, help='Facebook access token')
    parser.add_argument('--account', default='act_1236576254450117', help='Ad account ID')
    parser.add_argument('--hours', type=int, default=24, help='Hours of data to analyze (default: 24)')
    
    args = parser.parse_args()
    
    tracker = FOMOPerformanceTracker(args.token, args.account)
    tracker.get_campaign_insights(args.hours)
    tracker.analyze_fomo_performance()

if __name__ == "__main__":
    main()