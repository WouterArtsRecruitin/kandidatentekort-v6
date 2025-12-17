# 🔧 Meta Ads UTM Fix Tool

## Overview
This tool automatically adds proper UTM tracking parameters to all your Meta (Facebook) ads for the Kandidatentekort campaigns.

## 🎯 What It Does

### Analysis Mode:
- Scans all active/paused campaigns
- Checks each ad for UTM parameters
- Reports which ads are missing tracking
- Shows percentage of ads needing fixes

### Fix Mode:
- Adds proper UTM parameters to all ads
- Preserves existing campaign structure
- Creates new creatives with UTM tracking
- Updates ads to use new tracked creatives

## 📋 UTM Structure

The tool adds these parameters:
```
utm_source=facebook
utm_medium=paid_social
utm_campaign=kandidatentekort_[campaign_name]
utm_content=[adset_name]_[ad_name]
utm_term=recruitment_nl
```

## 🚀 Quick Start

### 1. Setup (One Time)
```bash
# Make setup script executable
chmod +x setup_utm_fix.sh

# Run setup
./setup_utm_fix.sh
```

### 2. Get Access Token
1. Go to: https://developers.facebook.com/tools/explorer
2. Select your app or create a test app
3. Add permissions: `ads_read`, `ads_management`
4. Generate token
5. Copy the token

### 3. Run Analysis
```bash
python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117
```

### 4. Fix Missing UTMs (Dry Run)
```bash
python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117 --fix
```

### 5. Fix Missing UTMs (Live)
```bash
python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117 --fix --live
```

## 📊 Example Output

### Analysis Mode:
```
=== META ADS UTM ANALYSIS ===
Account: act_1236576254450117
Time: 2024-12-16 14:30:00

Campaign: Cold Awareness Campaign
  Ad Set: Broad Targeting 25-55
    ✓ Ad 1: UTM parameters present
    ✗ Ad 2: Missing UTM parameters
      - link_url: https://kandidatentekort.nl/...

=== SUMMARY ===
Total ads analyzed: 12
Ads with UTM: 8
Ads missing UTM: 4
⚠ 33.3% of ads need UTM parameters
```

### Fix Mode (Dry Run):
```
=== META ADS UTM FIX - DRY RUN ===
Campaign: Cold Awareness Campaign
  Ad Set: Broad Targeting 25-55
    ⚡ Ad 2: Adding UTM parameters
      [DRY RUN] Would add:
        - utm_source=facebook
        - utm_medium=paid_social
        - utm_campaign=kandidatentekort_cold_awareness_campaign
        - utm_content=broad_targeting_25_55_ad_2
        - utm_term=recruitment_nl
```

## 🔒 Safety Features

1. **Dry Run Mode**: Test changes without modifying ads
2. **Status Check**: Only processes active/paused campaigns
3. **Error Handling**: Continues if individual ads fail
4. **Preserve Structure**: Creates new creatives, doesn't delete
5. **Detailed Logging**: See exactly what's being changed

## ⚠️ Important Notes

1. **Token Expiration**: Access tokens expire. Get a new one if you see authentication errors.

2. **API Limits**: Facebook has rate limits. The tool handles this gracefully.

3. **Creative Duplication**: The tool creates new creatives with UTM parameters. Old creatives remain unchanged.

4. **Campaign Performance**: Adding UTM parameters requires creating new creatives, which may reset learning phase.

## 🆘 Troubleshooting

### "Invalid OAuth 2.0 Access Token"
- Your token has expired
- Get a new token from the Graph API Explorer

### "Unsupported post type"
- Some ad types can't be modified via API
- These will be skipped automatically

### "Rate limit reached"
- Wait a few minutes and try again
- The tool will show which ads were processed

## 📈 After Implementation

Once UTM parameters are added:

1. **Google Analytics**: Track traffic source properly
2. **Attribution**: See which campaigns drive applications
3. **ROI Calculation**: Accurate cost per acquisition
4. **A/B Testing**: Compare campaign performance

## 🔄 Regular Maintenance

Run the analysis weekly to ensure new ads have proper tracking:
```bash
# Weekly check
python meta_ads_utm_fix.py --token YOUR_TOKEN --account act_1236576254450117
```

## 📞 Support

If you encounter issues:
1. Check token permissions
2. Verify account ID is correct
3. Run analysis mode first
4. Use dry run before live updates

---

Remember: Always test with dry run first! 🚀