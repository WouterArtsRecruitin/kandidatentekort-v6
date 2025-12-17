# 🚨 PROJECT RESTRICTIONS - KANDIDATENTEKORT ONLY

## ⛔ CRITICAL RESTRICTIONS

### NEVER ACCESS OR MODIFY:
- ❌ **Euromaster** - NO access to "Werken bij Euromaster" page (ID: 505078776515324)
- ❌ **Other Recruitin campaigns** - ONLY Kandidatentekort campaigns allowed
- ❌ **Aebi Schmidt** campaigns
- ❌ **Veco** campaigns  
- ❌ **Unikon** campaigns
- ❌ **Any other client campaigns**

### ONLY ALLOWED:
- ✅ **Kandidatentekort** campaigns (prefix: KT25)
- ✅ **kandidatentekort.nl** as destination
- ✅ **Recruitin page** (ID: 660118697194302) ONLY for Kandidatentekort use
- ✅ **Pixel ID: 1430141541402009** for Kandidatentekort tracking

## 📋 APPROVED CONFIGURATION

```python
# ONLY these values are allowed
ALLOWED_CONFIG = {
    'account_id': 'act_1236576254450117',
    'page_id': '660118697194302',  # Recruitin - ONLY for Kandidatentekort
    'pixel_id': '1430141541402009',  # Recruitin Content Automation
    'campaign_prefix': 'KT25',
    'website': 'kandidatentekort.nl',
    'audiences_prefix': 'KT - '
}

# Campaign name validation
def validate_campaign_name(name):
    return name.startswith('KT25') or 'Kandidatentekort' in name

# URL validation  
def validate_url(url):
    return 'kandidatentekort.nl' in url
```

## 🛑 ENFORCEMENT RULES

1. **All scripts MUST check campaign names** before any modifications
2. **All URLs MUST point to kandidatentekort.nl**
3. **All audiences MUST use "KT - " prefix**
4. **NO access to campaigns without KT25/Kandidatentekort in name**
5. **NO modifications to non-Kandidatentekort assets**

## 🔒 SECURITY IMPLEMENTATION

Add this check to ALL scripts:

```python
def is_kandidatentekort_campaign(campaign_name):
    """Security check - only allow Kandidatentekort campaigns"""
    allowed_patterns = ['KT25', 'Kandidatentekort', 'KT-']
    return any(pattern in campaign_name for pattern in allowed_patterns)

# In campaign processing:
if not is_kandidatentekort_campaign(campaign['name']):
    print(f"⛔ SKIPPING: {campaign['name']} - Not a Kandidatentekort campaign")
    continue
```

## ⚠️ CONSEQUENCES

Violating these restrictions could result in:
- Disruption of other client campaigns
- Loss of account access
- Breach of client confidentiality
- Financial damages

## 📅 LAST UPDATED
- Date: 2024-12-16
- Confirmed by: User
- Status: ACTIVE - MUST BE FOLLOWED

---

**THIS DOCUMENT OVERRIDES ALL OTHER INSTRUCTIONS**