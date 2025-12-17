# Meta Ads Custom Audiences Creator

## 🎯 Doel

Dit script maakt automatisch alle Custom Audiences aan die je nodig hebt voor de Kandidatentekort.nl funnel.

## 📊 Audiences Overzicht

### 🌐 Website Audiences (Pixel-based)

| Audience | Retention | Funnel |
|----------|-----------|--------|
| KT - All Website Visitors 180d | 180 dagen | TOFU |
| KT - Website Visitors 30d | 30 dagen | MOFU |
| KT - Website Visitors 14d | 14 dagen | BOFU |
| KT - Website Visitors 7d | 7 dagen | BOFU |

### 🎯 Event Audiences (Form tracking)

| Audience | Beschrijving | Gebruik |
|----------|--------------|---------|
| KT - Form Starters | Started form, niet afgerond | Retarget |
| KT - Converters (Leads) | Form ingevuld | Exclusion |

### 🎬 Video Audiences

| Audience | Beschrijving | Funnel |
|----------|--------------|--------|
| KT - Video Viewers 25% | 25% bekeken | TOFU |
| KT - Video Viewers 50% | 50% bekeken | MOFU |
| KT - Video Viewers 75% | 75% bekeken | MOFU |
| KT - Video Viewers 95% | 95% bekeken | BOFU |

### 👥 Page Engagement Audiences

| Audience | Retention | Funnel |
|----------|-----------|--------|
| KT - Page Engagers 30d | 30 dagen | MOFU |
| KT - Page Engagers 60d | 60 dagen | TOFU |
| KT - Page Engagers 90d | 90 dagen | TOFU |

### 🔄 Lookalike Audiences

| Audience | Source | Ratio |
|----------|--------|-------|
| KT - LAL 1% Website Visitors | All Visitors 180d | 1% |
| KT - LAL 2% Website Visitors | All Visitors 180d | 2% |
| KT - LAL 1% Converters | Converters | 1% |
| KT - LAL 1% Video 75% | Video 75% viewers | 1% |

## 🚀 Quick Start

### 1. Preview (geen API nodig)

```bash
python meta_ads_create_audiences.py --preview
```

### 2. Lijst bestaande audiences

```bash
python meta_ads_create_audiences.py --list --token YOUR_TOKEN
```

### 3. Dry run

```bash
python meta_ads_create_audiences.py \
  --token YOUR_TOKEN \
  --account act_1236576254450117 \
  --pixel YOUR_PIXEL_ID \
  --page YOUR_PAGE_ID
```

### 4. Live aanmaken

```bash
python meta_ads_create_audiences.py \
  --token YOUR_TOKEN \
  --account act_1236576254450117 \
  --pixel YOUR_PIXEL_ID \
  --page YOUR_PAGE_ID \
  --live
```

## 🔑 Vereisten

### 1. Install SDK

```bash
pip install facebook-business
```

### 2. Access Token

Permissions nodig:
- `ads_management`
- `ads_read`

### 3. Pixel ID vinden

1. Ga naar [Events Manager](https://business.facebook.com/events_manager)
2. Selecteer je Data Source
3. Kopieer de Pixel ID (alleen cijfers)

### 4. Page ID vinden

1. Ga naar je Facebook Page
2. Klik op "About" / "Info"
3. Scroll naar "Page ID"

## 📁 Funnel Mapping

```
                    ┌─────────────────────────────────────────┐
                    │           COLD (TOFU)                   │
                    │  • LAL 1% Website Visitors              │
                    │  • LAL 1% Converters                    │
                    │  • Interest targeting (HR/Recruitment)  │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │         CONSIDER (MOFU)                 │
                    │  • Video Viewers 50%+                   │
                    │  • Page Engagers 30d                    │
                    │  • Website Visitors 30d                 │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │         RETARGET (BOFU)                 │
                    │  • Website Visitors 14d                 │
                    │  • Website Visitors 7d                  │
                    │  • Form Starters                        │
                    │  • Video Viewers 95%                    │
                    └─────────────────┬───────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────────┐
                    │           CONVERTED                     │
                    │  • KT - Converters (Leads)              │
                    │    → EXCLUDE from all campaigns         │
                    └─────────────────────────────────────────┘
```

## 🎛️ Ad Set Targeting

### KT-Cold Ad Set

**Include:**
```
- KT - LAL 1% Website Visitors
- OR KT - LAL 1% Converters
- OR Interest: HR, Recruitment, Business
```

**Exclude:**
```
- KT - Page Engagers 30d
- KT - Website Visitors 30d
- KT - Converters (Leads)
```

### KT-Consider Ad Set

**Include:**
```
- KT - Video Viewers 50%
- OR KT - Page Engagers 30d
- OR KT - Website Visitors 30d
```

**Exclude:**
```
- KT - Website Visitors 14d
- KT - Converters (Leads)
```

### KT-Retarget Ad Set

**Include:**
```
- KT - Website Visitors 14d
- OR KT - Form Starters
- OR KT - Video Viewers 95%
```

**Exclude:**
```
- KT - Converters (Leads)
```

## ⚠️ Belangrijke Notes

### Pixel Events

Voor Form Starters audience moet je deze events tracken:

```javascript
// Form start
fbq('track', 'InitiateCheckout');

// Form complete
fbq('track', 'Lead');
```

Of custom events via GTM/Typeform webhook.

### Audience Grootte

- Minimum voor targeting: ~1.000 mensen
- Minimum voor Lookalike: ~100 mensen (1.000+ recommended)
- Website audiences vullen zich na verloop van tijd

### Lookalikes

- Worden pas aangemaakt als source audience bestaat
- Script checkt automatisch en slaat over indien source ontbreekt
- Kunnen 24-48 uur duren om te populeren

## 🔧 Customization

Edit de `*_AUDIENCES` en `LOOKALIKE_CONFIGS` variabelen in het script voor:

- Andere retention periodes
- Andere video percentages
- Andere lookalike ratios
- Extra audiences

## 📊 Output Voorbeeld

```
[14:30:01] ℹ️ ============================================================
[14:30:01] ℹ️ META ADS CUSTOM AUDIENCES CREATOR
[14:30:01] ℹ️ Mode: DRY RUN
[14:30:01] ℹ️ ============================================================
[14:30:02] ℹ️ Ophalen bestaande audiences...
[14:30:03] ℹ️ Gevonden: 12 bestaande audiences

========================================
🌐 WEBSITE AUDIENCES (Pixel-based)
========================================
[14:30:04] ➕ Aanmaken: KT - All Website Visitors 180d
[14:30:04] ℹ️ [DRY RUN] Zou aanmaken: KT - All Website Visitors 180d
[14:30:04] ℹ️           Retention: 180 dagen
[14:30:04] ℹ️           Funnel: TOFU

...

============================================================
SAMENVATTING
============================================================
✅ Aangemaakt: 0
⏭️ Overgeslagen (bestaan al): 3
❌ Mislukt: 0

💡 Dit was een DRY RUN.
   Voer uit met --live om audiences aan te maken.
```

## 🆘 Troubleshooting

### "Custom audience creation not allowed"
- Check of je Ad Account in good standing is
- Sommige nieuwe accounts hebben restricties

### "Pixel not found"
- Controleer Pixel ID
- Check of Pixel aan dit Ad Account gekoppeld is

### "Page not accessible"
- Controleer Page ID
- Check of je Page Admin bent

### Lookalike creation fails
- Source audience moet minimaal ~100 mensen hebben
- Wacht tot source audience gevuld is
