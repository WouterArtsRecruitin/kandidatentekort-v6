# 📊 Supermetrics Google Sheets Integration Guide

## API Key Information
Your Supermetrics API key: `api_9BLJx4w6XC5b8ZmfHKLTT6PtMlg4zkay2A9Uf_zIG4NJX7FHWNthRsiz0zw6BAOcb7lP6s7iLwAIEHrhXDLzRiu_DHnOzriba65e`

## 🚀 Step-by-Step Setup Guide

### Step 1: Install Supermetrics Add-on
1. Open your Google Sheet: [Kandidatentekort Campaign Dashboard](https://docs.google.com/spreadsheets/d/1gbo-7RJSCakhqaoicxwMops9yK0BHUsQWbWl5adxB3Q/edit)
2. Go to **Extensions** → **Add-ons** → **Get add-ons**
3. Search for "**Supermetrics**"
4. Click **Install** and grant necessary permissions

### Step 2: Launch Supermetrics
1. In your Google Sheet, go to **Extensions** → **Supermetrics** → **Launch sidebar**
2. The Supermetrics sidebar will open on the right

### Step 3: Configure Data Sources
Connect your marketing platforms:

#### Facebook/Meta Ads
1. Click **Select data source** → **Facebook Ads**
2. Click **Connect** and log in with your Facebook account
3. Select the ad accounts you want to pull data from

#### Google Ads
1. Click **Select data source** → **Google Ads**
2. Connect your Google Ads account
3. Select campaigns to track

#### LinkedIn Ads
1. Click **Select data source** → **LinkedIn Ads**
2. Authenticate and select ad accounts

### Step 4: Set Up Your First Query

#### Basic Campaign Performance Query:
```
Data source: Facebook Ads
Select metrics:
- Impressions
- Clicks
- CTR
- Spend
- Conversions
- Cost per conversion
- ROAS

Select dimensions:
- Campaign name
- Ad set name
- Date

Date range: Last 30 days
```

### Step 5: Configure Automatic Refresh
1. In Supermetrics sidebar, click **Schedule refresh**
2. Set options:
   - **Frequency**: Daily at 6 AM
   - **Email notifications**: On errors
   - **Overwrite existing data**: Yes

### Step 6: Create Dashboard Views

#### Tab 1: Overview Dashboard
- Total spend across all platforms
- Total conversions
- Overall ROAS
- Cost per application

#### Tab 2: Platform Performance
- Performance by platform (Meta, Google, LinkedIn)
- Budget allocation
- Conversion rates by platform

#### Tab 3: Campaign Details
- Individual campaign performance
- Ad set breakdown
- Creative performance

#### Tab 4: Kandidatentekort Metrics
- Applications generated
- Cost per qualified candidate
- Conversion funnel metrics
- Regional performance (Netherlands)

### Step 7: API Configuration (Advanced)

For programmatic access, use your API key:

```javascript
// Example API request
const SUPERMETRICS_API_KEY = 'api_9BLJx4w6XC5b8ZmfHKLTT6PtMlg4zkay2A9Uf_zIG4NJX7FHWNthRsiz0zw6BAOcb7lP6s7iLwAIEHrhXDLzRiu_DHnOzriba65e';

const headers = {
  'Authorization': `Bearer ${SUPERMETRICS_API_KEY}`,
  'Content-Type': 'application/json'
};

// Fetch data endpoint
const apiUrl = 'https://api.supermetrics.com/enterprise/v2/query/data';
```

### 📊 Recommended Metrics for Recruitment Campaigns

#### Primary KPIs:
1. **Cost per Application**: Total spend / Applications
2. **Application Rate**: Applications / Clicks
3. **Quality Score**: Qualified candidates / Total applications
4. **Time to Fill**: Average days from ad to hire
5. **Regional Performance**: Applications by location

#### Secondary Metrics:
- Click-through rate (CTR)
- Cost per click (CPC)
- Impression share
- Ad frequency
- Audience overlap

### 🔄 Automation Setup

#### Google Apps Script for Custom Processing:
```javascript
function updateDashboard() {
  // This runs after Supermetrics refresh
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const dataSheet = sheet.getSheetByName('Raw Data');
  const dashboardSheet = sheet.getSheetByName('Dashboard');
  
  // Process recruitment metrics
  calculateRecruitmentKPIs();
  updateCharts();
  sendSlackNotification();
}

function calculateRecruitmentKPIs() {
  // Custom calculations for kandidatentekort metrics
  // - Cost per qualified candidate
  // - Conversion rates by job type
  // - Regional performance analysis
}
```

### 🎯 Kandidatentekort-Specific Setup

#### Custom Metrics:
1. **40-60% More Applications Tracking**:
   - Baseline applications (before optimization)
   - Current applications
   - Improvement percentage

2. **Campaign Performance by Type**:
   - Cold Awareness campaigns
   - Consideration campaigns
   - Retargeting campaigns

3. **Dutch Market Insights**:
   - Performance by Dutch regions
   - Age group performance (25-55)
   - Industry-specific metrics

### 📱 Alerts and Notifications

Set up alerts for:
- Daily spend exceeding €240
- Cost per application > €15
- CTR dropping below 1%
- Conversion rate < 5%

### 🛠️ Troubleshooting

#### Common Issues:
1. **Data not refreshing**: Check API limits and permissions
2. **Missing metrics**: Verify data source connections
3. **Incorrect calculations**: Review metric definitions
4. **Slow performance**: Optimize query complexity

#### API Rate Limits:
- 1000 requests per hour
- 10,000 rows per query
- 100 MB data per refresh

### 📧 Support Resources
- Supermetrics Support: support@supermetrics.com
- API Documentation: https://supermetrics.com/docs/product-api
- Community Forum: https://community.supermetrics.com

---

## Next Steps:
1. Install Supermetrics add-on
2. Connect your ad platforms
3. Set up initial queries
4. Configure automated refresh
5. Create dashboard visualizations
6. Set up alerts for key metrics