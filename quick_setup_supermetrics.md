# 🚀 Quick Setup: Supermetrics + Google Sheets

## Your Credentials:
- **Google Sheet**: [Kandidatentekort Campaign Dashboard](https://docs.google.com/spreadsheets/d/1gbo-7RJSCakhqaoicxwMops9yK0BHUsQWbWl5adxB3Q/edit)
- **API Key**: `api_9BLJx4w6XC5b8ZmfHKLTT6PtMlg4zkay2A9Uf_zIG4NJX7FHWNthRsiz0zw6BAOcb7lP6s7iLwAIEHrhXDLzRiu_DHnOzriba65e`

## ⚡ 5-Minute Setup

### 1️⃣ Install Supermetrics (1 min)
1. Open your Google Sheet
2. Extensions → Add-ons → Get add-ons
3. Search "**Supermetrics**" → Install

### 2️⃣ Connect Facebook Ads (2 min)
1. Extensions → Supermetrics → Launch sidebar
2. Select **Facebook Ads** → Connect
3. Choose your ad account

### 3️⃣ Create First Report (2 min)
Quick query for your recruitment campaigns:
```
📊 METRICS:
✓ Spend
✓ Impressions  
✓ Clicks
✓ Link clicks
✓ Conversions
✓ Cost per conversion

📅 DATE: Last 30 days
🎯 SPLIT BY: Campaign name, Date
```

### 4️⃣ Add the Google Apps Script
1. In your Sheet: Extensions → Apps Script
2. Delete any existing code
3. Copy & paste the `google_sheets_script.js` file
4. Click 💾 Save
5. Run → `onOpen` (authorize when prompted)

## 📊 What You'll Get:

### Automated Dashboard with:
- **Real-time campaign performance**
- **Cost per application tracking**
- **40-60% improvement metrics**
- **Daily budget monitoring (€240)**
- **Alert system for overspending**

### Campaign Tracking:
- Cold Awareness Campaign
- Consideration Campaign  
- Retargeting Campaign

### Key Metrics:
- Applications per day
- Cost per qualified candidate
- Regional performance (Netherlands)
- Age group analysis (25-55)

## 🔔 Alerts Configuration

The system will alert you when:
- ❌ Cost per application > €15
- ❌ Daily spend > €240
- ❌ CTR < 1%
- ❌ Application rate < 5%

## 📱 Next Steps:

1. **Set refresh schedule**: 
   - Supermetrics sidebar → Schedule → Daily at 6 AM

2. **Configure alerts**:
   - Kandidatentekort menu → Setup Triggers

3. **Connect more platforms**:
   - Google Ads
   - LinkedIn Ads
   - Google Analytics

## 💡 Pro Tips:

1. **Use the API for custom integrations**:
```javascript
fetch('https://api.supermetrics.com/enterprise/v2/query/data', {
  headers: {
    'Authorization': 'Bearer api_9BLJx4w6XC5b8ZmfHKLTT6PtMlg4zkay2A9Uf_zIG4NJX7FHWNthRsiz0zw6BAOcb7lP6s7iLwAIEHrhXDLzRiu_DHnOzriba65e'
  }
});
```

2. **Track your 40-60% improvement goal**:
   - Set baseline in week 1
   - Monitor weekly improvement
   - Adjust campaigns based on data

3. **Optimize for Dutch market**:
   - Track performance by region
   - A/B test Dutch vs English ad copy
   - Monitor time-of-day performance

## 🆘 Need Help?
- Supermetrics Support: support@supermetrics.com
- API Docs: https://supermetrics.com/docs
- Your dashboard: [Open Sheet](https://docs.google.com/spreadsheets/d/1gbo-7RJSCakhqaoicxwMops9yK0BHUsQWbWl5adxB3Q)