# 🚨 KANDIDATENTEKORT UTM FIX - ACTIEPLAN

## 🔴 KRITIEK PROBLEEM
Je Meta ads linken naar **Facebook Reels**, NIET naar kandidatentekort.nl!
- **Impact**: 0% tracking, 0% conversies, 100% budget verspilling

## ✅ OPLOSSING IN 3 STAPPEN

### Stap 1: Analyseer Huidige Situatie
```bash
# Check welke ads naar Reels gaan
./venv/bin/python meta_ads_utm_analyzer.py \
  --token "EAAYqzG39fnoBQM5NM5ZCIxuEIn0pyfsz6XWsCdO5nprSL33bZAd1Vlj0mGnMA3HsFoEP2GUX9vJUIA5VTTw75ICZCU82wpT8YaYIRdZAr9GaQ8L4cQblNWdgUKvuz6uJwhQx8ZB0JKTdvbRUpSY84T5xh5fvRxqwglNIkj2gBhMRMLe7pNAj5jxbykOlU4f2p9d1RwHwhT0tZCKJj9GFZB71XeKHpcDEDZBEq4M29fq1ZAzqSDCCZA5uv9ebE6U1XOC5RsnPqKmkKZC2UpSgNaFOzJqRFjw6AG4" \
  --account act_1236576254450117
```

### Stap 2: Maak NIEUWE Traffic Campaigns

#### A. Preview (geen token nodig)
```bash
./venv/bin/python meta_ads_create_campaign.py --preview
```

#### B. Dry Run (met jouw page ID)
```bash
# Eerst: Vind je Page ID
# Ga naar: https://www.facebook.com/[jouw-pagina]
# Klik About → Page transparency → Page ID

./venv/bin/python meta_ads_create_campaign.py \
  --token "EAAYqzG39fnoBQM5NM5ZCIxuEIn0pyfsz6XWsCdO5nprSL33bZAd1Vlj0mGnMA3HsFoEP2GUX9vJUIA5VTTw75ICZCU82wpT8YaYIRdZAr9GaQ8L4cQblNWdgUKvuz6uJwhQx8ZB0JKTdvbRUpSY84T5xh5fvRxqwglNIkj2gBhMRMLe7pNAj5jxbykOlU4f2p9d1RwHwhT0tZCKJj9GFZB71XeKHpcDEDZBEq4M29fq1ZAzqSDCCZA5uv9ebE6U1XOC5RsnPqKmkKZC2UpSgNaFOzJqRFjw6AG4" \
  --account act_1236576254450117 \
  --page YOUR_PAGE_ID
```

#### C. Live Creation
```bash
./venv/bin/python meta_ads_create_campaign.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --page YOUR_PAGE_ID \
  --live
```

### Stap 3: Fix Bestaande Ads (Optioneel)

#### A. Check wat gefixed moet worden
```bash
./venv/bin/python fix_destination_urls.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --dry-run
```

#### B. Fix live
```bash
./venv/bin/python fix_destination_urls.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --live
```

## 📊 NIEUWE CAMPAIGN STRUCTUUR

### 3 Traffic Campaigns (€80/dag elk):

1. **KT25--Traffic--Cold-Awareness--Dec2025**
   - 4 ads met verschillende angles
   - UTM: `utm_campaign=cold_awareness`

2. **KT25--Traffic--Consideration--Dec2025**
   - 4 ads met case studies en ROI
   - UTM: `utm_campaign=consideration`

3. **KT25--Traffic--Retargeting--Dec2025**
   - 4 ads met urgency en social proof
   - UTM: `utm_campaign=retargeting`

### Elke Ad krijgt:
```
https://kandidatentekort.nl/?utm_source=meta&utm_medium=paid&utm_campaign={campaign}&utm_content={ad_variation}
```

## 🎯 RESULTAAT NA IMPLEMENTATIE

### In Meta Ads Manager:
- ✅ 3 nieuwe Traffic campaigns
- ✅ 12 ads met website links
- ✅ Correcte UTM tracking

### In Google Analytics 4:
- ✅ Traffic zichtbaar onder Acquisition
- ✅ Campagne performance tracking
- ✅ Conversion tracking mogelijk

### Dashboard Metrics:
- ✅ Cost per application
- ✅ ROAS berekening
- ✅ 40-60% improvement tracking

## ⚡ QUICK START COMMANDO'S

```bash
# 1. Activeer virtual environment
source venv/bin/activate

# 2. Preview nieuwe campaigns
python meta_ads_create_campaign.py --preview

# 3. Analyseer huidige ads
python meta_ads_utm_analyzer.py --token "YOUR_TOKEN" --account act_1236576254450117

# 4. Maak nieuwe campaigns (met jouw page ID!)
python meta_ads_create_campaign.py --token "YOUR_TOKEN" --account act_1236576254450117 --page YOUR_PAGE_ID --live
```

## 🚨 BELANGRIJK

1. **Stop huidige Reels campaigns** zodra nieuwe Traffic campaigns live zijn
2. **Monitor eerste 48 uur** voor performance
3. **Check GA4** of traffic binnenkomt
4. **Optimaliseer** na learning phase (3-7 dagen)

---

**Hulp nodig?** De scripts hebben uitgebreide error handling en geven duidelijke instructies!