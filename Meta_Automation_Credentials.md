# Meta Campaign Automation - Complete Credentials & Configuration

## ⚠️ SECURITY WARNING
Dit document bevat gevoelige API credentials. Bewaar veilig en deel niet publiek!

---

## 🔑 FACEBOOK / META API CREDENTIALS

### Core Credentials

| Credential | Value | Status |
|------------|-------|--------|
| **Facebook Pixel ID** | `238226887541404` | ✅ Actief |
| **Ad Account ID** | `act_1443564313411457` | ✅ Geconfigureerd |
| **App ID** | `1735907367288442` | ✅ Geconfigureerd |
| **App Secret** | `9ee40f5aa3ba931320ac3c3e61233401` | ✅ Toegevoegd |
| **Access Token** | `EAASX9Iy8fL8BPYsXtZBnl8nCHRZBFirORx0H6fe9ColghZC2ZCLtWISBnP8fYdkICv9cbTPl9YYLmcKI4sZB42l9PjIr6bj9gD74X0E6qtGMETAfAcEo50bNnqiEZB8S0hZBDVNsmwumHjLXn31ptOCoZCQWZBiCiR2HhJ6iDrqOsNlZB6Ew0ALCuF9tFEJA0IgQZDZD` | ✅ Long-lived token |

### Secondary App ID (Conversions API)
| Credential | Value |
|------------|-------|
| **Conversions API App ID** | `1136518731699168` |

---

## 📍 LINKEDIN CREDENTIALS

| Credential | Value | Status |
|------------|-------|--------|
| **LinkedIn Insight Tag** | `1830706` | ✅ Geïmplementeerd |

---

## 🌐 NETLIFY CONFIGURATION

| Setting | Value |
|---------|-------|
| **Site ID (recruitmentapk-ab-test)** | `9a753352-210d-4a12-934f-48bd5e0ed3ed` |
| **Site ID (kandidatentekort)** | `3c89912a-f1be-4c6c-ba73-03ba7fdc8dc7` |

### Environment Variables (Netlify)
- `FACEBOOK_PIXEL_ID`: 238226887541404
- `FACEBOOK_ACCESS_TOKEN`: [Configured]
- `FACEBOOK_APP_ID`: 1136518731699168

---

## 🔧 API CONFIGURATION BLOCK

```python
CONFIG = {
    "meta": {
        "access_token": "EAASX9Iy8fL8BPYsXtZBnl8nCHRZBFirORx0H6fe9ColghZC2ZCLtWISBnP8fYdkICv9cbTPl9YYLmcKI4sZB42l9PjIr6bj9gD74X0E6qtGMETAfAcEo50bNnqiEZB8S0hZBDVNsmwumHjLXn31ptOCoZCQWZBiCiR2HhJ6iDrqOsNlZB6Ew0ALCuF9tFEJA0IgQZDZD",
        "app_secret": "9ee40f5aa3ba931320ac3c3e61233401",
        "ad_account_id": "act_1443564313411457",
        "pixel_id": "238226887541404",
        "app_id": "1735907367288442"
    }
}
```

---

## 📱 FACEBOOK PIXEL IMPLEMENTATION

### Base Code
```html
<!-- Facebook Pixel Base Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window,document,'script',
'https://connect.facebook.net/en_US/fbevents.js');

fbq('init', '238226887541404');
fbq('track', 'PageView');
</script>
<noscript>
<img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=238226887541404&ev=PageView&noscript=1"/>
</noscript>
```

---

## 🎯 EVENT TRACKING SETUP

| User Action | Facebook Event | Value | Trigger |
|-------------|----------------|-------|---------|
| Page Load | PageView | - | Automatic |
| Start Assessment | InitiateCheckout | €45 | Button click |
| Complete Assessment | CompleteRegistration | €45 | Form submit |
| Download Report | Purchase | €45 | Download button |

---

## 🔗 API ENDPOINTS

### Meta Graph API
```
Base URL: https://graph.facebook.com/v18.0/
Campaign: GET/POST /act_{ad_account_id}/campaigns
Ad Sets: GET/POST /act_{ad_account_id}/adsets
Ads: GET/POST /act_{ad_account_id}/ads
Insights: GET /{campaign_id}/insights
```

### Test API Connection
```bash
curl "https://graph.facebook.com/v18.0/me/adaccounts?access_token=EAASX9Iy8fL8BPYsXtZBnl8nCHRZBFirORx0H6fe9ColghZC2ZCLtWISBnP8fYdkICv9cbTPl9YYLmcKI4sZB42l9PjIr6bj9gD74X0E6qtGMETAfAcEo50bNnqiEZB8S0hZBDVNsmwumHjLXn31ptOCoZCQWZBiCiR2HhJ6iDrqOsNlZB6Ew0ALCuF9tFEJA0IgQZDZD"
```

---

## 📊 CAMPAIGN CONFIGURATION

### Budget Tiers (13 Regio's)
| Tier | Steden | Budget/dag |
|------|--------|------------|
| Tier 1 | Utrecht, Eindhoven | €5-6/dag |
| Tier 2 | Almere, Zwolle, Apeldoorn | €3-4/dag |
| Tier 3 | Overige regio's | €2-3/dag |

### Campaign Settings
- **Total Daily Budget:** €50/dag (€1.500/maand)
- **Objective:** Lead Generation
- **Optimization:** Conversion (Assessment Starts)
- **Pixel Events:** InitiateCheckout, CompleteRegistration

---

## ✅ VALIDATION CHECKLIST

- [x] Facebook Pixel ID: 238226887541404
- [x] Ad Account ID: act_1443564313411457
- [x] App ID: 1735907367288442
- [x] App Secret: Configured
- [x] Access Token: Long-lived token active
- [x] LinkedIn Insight Tag: 1830706
- [x] Netlify Environment Variables: Set

---

## 🚨 TOKEN REFRESH REMINDER

**Access tokens verlopen!** Check regelmatig:
1. Ga naar developers.facebook.com/tools/explorer
2. Genereer nieuwe token indien nodig
3. Update Netlify environment variables
4. Test API connectivity

---

## 📁 PROJECT LOCATIONS

```
Meta Campaign Automation:
/Users/wouterarts/.claude-worktrees/Kandidatentekortfull/pensive-hugle/projects/meta-campaign-automation

Key Files:
- complete_meta_flow.py
- meta_campaign_generator.py
- meta_api_client.py
- main_server.py
```

---

*Document gegenereerd uit chat historie - November 2025*
