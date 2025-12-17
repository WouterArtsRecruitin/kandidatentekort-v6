# 🚨 UTM TRACKING DIAGNOSE - KANDIDATENTEKORT

## 🔴 KRITIEK PROBLEEM GEVONDEN

### Huidige Situatie:
| Probleem | Details |
|----------|---------|
| **Destination URL** | Alle ads linken naar **Facebook Reels** (`facebook.com/reel/...`) |
| **Landing Page** | NIET naar `kandidatentekort.nl` |
| **utm_campaign** | **LEEG** - niet ingesteld |
| **utm_content** | **LEEG** - niet ingesteld |
| **utm_medium** | Alleen `cpc` (Facebook default) |

### Impact:
- ❌ GA4 ziet maar 2 sessies van "meta / paid_social"
- ❌ Geen tracking van campagne performance
- ❌ Geen traffic naar kandidatentekort.nl
- ❌ ROI niet meetbaar

## 🎯 PROBLEEM VERKLAARD

Je ads zijn geconfigureerd als **Engagement campaigns** met Reels:
- Doel: Views/likes op Facebook Reels
- NIET: Traffic naar website

Dit verklaart waarom:
1. UTM parameters niet werken (blijven op Facebook)
2. GA4 geen traffic ziet
3. Conversies niet getrackt worden

## ✅ OPLOSSING STRATEGIE

### Optie 1: Hybrid Aanpak (Aanbevolen)
1. **Behoud Reels campaigns** voor awareness (top funnel)
2. **Voeg Traffic/Conversion campaigns toe** met:
   ```
   URL: https://kandidatentekort.nl/?utm_source=meta&utm_medium=paid&utm_campaign=kt25_cold&utm_content=ad1
   ```

### Optie 2: Convert Existing Campaigns
1. Wijzig campaign objective naar **OUTCOME_TRAFFIC**
2. Update alle ads met website links
3. Voeg UTM parameters toe

## 📊 CORRECTE UTM STRUCTUUR

Voor elke ad naar kandidatentekort.nl:
```
https://kandidatentekort.nl/?utm_source=meta&utm_medium=paid&utm_campaign={campaign_type}&utm_content={ad_variation}

Voorbeelden:
- Cold: ?utm_source=meta&utm_medium=paid&utm_campaign=kt25_cold_awareness&utm_content=intro_video
- Consideration: ?utm_source=meta&utm_medium=paid&utm_campaign=kt25_consideration&utm_content=social_proof
- Retargeting: ?utm_source=meta&utm_medium=paid&utm_campaign=kt25_retargeting&utm_content=urgency_cta
```

## 🛠️ ACTIEPLAN

### Stap 1: Audit Current Setup
```bash
python meta_ads_utm_analyzer.py --token YOUR_TOKEN --account act_1236576254450117
```

### Stap 2: Create Traffic Campaigns
```bash
python create_traffic_campaigns.py --token YOUR_TOKEN --account act_1236576254450117
```

### Stap 3: Update Existing Ads
```bash
python fix_destination_urls.py --token YOUR_TOKEN --account act_1236576254450117 --dry-run
```

### Stap 4: Verify in GA4
- Check Acquisition > Traffic acquisition
- Filter by utm_source = meta
- Verify all campaigns show up

## 📈 EXPECTED RESULTS

Na implementatie:
- ✅ 100% traffic tracking in GA4
- ✅ Campagne performance per type
- ✅ Cost per application berekening
- ✅ ROAS measurement
- ✅ 40-60% improvement tracking

## ⚠️ BELANGRIJKE NOTITIES

1. **Learning Phase**: Nieuwe campaigns gaan door learning phase (3-7 dagen)
2. **Budget Split**: 
   - 70% naar traffic/conversion campaigns
   - 30% naar awareness (Reels) campaigns
3. **Testing**: Test eerst met kleine budget (€20/dag)