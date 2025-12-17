# 🚀 START HIER - KANDIDATENTEKORT META ADS

## ✅ WAT JE NU HEBT

### 1. **Validation Script** - Check je setup
```bash
./venv/bin/python validate_meta_setup.py \
  --token "EAAYqzG39fnoBQM5NM5ZCIxuEIn0pyfsz6XWsCdO5nprSL33bZAd1Vlj0mGnMA3HsFoEP2GUX9vJUIA5VTTw75ICZCU82wpT8YaYIRdZAr9GaQ8L4cQblNWdgUKvuz6uJwhQx8ZB0JKTdvbRUpSY84T5xh5fvRxqwglNIkj2gBhMRMLe7pNAj5jxbykOlU4f2p9d1RwHwhT0tZCKJj9GFZB71XeKHpcDEDZBEq4M29fq1ZAzqSDCCZA5uv9ebE6U1XOC5RsnPqKmkKZC2UpSgNaFOzJqRFjw6AG4" \
  --account act_1236576254450117
```

Dit geeft je:
- ✅ Token check
- 📄 Lijst van je Pages (kies je Page ID)
- 🎯 Lijst van je Pixels (kies je Pixel ID)

### 2. **Audience Creator** - Maak targeting audiences
```bash
# Eerst preview
./venv/bin/python meta_ads_create_audiences.py --preview

# Dan live (met jouw IDs)
./venv/bin/python meta_ads_create_audiences.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --pixel YOUR_PIXEL_ID \
  --page YOUR_PAGE_ID \
  --live
```

### 3. **Campaign Creator** - Maak traffic campaigns
```bash
# Eerst preview
./venv/bin/python meta_ads_create_campaign.py --preview

# Dan live (met jouw Page ID)
./venv/bin/python meta_ads_create_campaign.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --page YOUR_PAGE_ID \
  --live
```

### 4. **UTM Analyzer** - Check huidige ads
```bash
./venv/bin/python meta_ads_utm_analyzer.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117
```

### 5. **URL Fixer** - Fix bestaande ads
```bash
./venv/bin/python fix_destination_urls.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --dry-run
```

## 🎯 PROBLEEM & OPLOSSING

**PROBLEEM**: Je ads gaan naar Facebook Reels, niet naar kandidatentekort.nl
**IMPACT**: 0% tracking, 0% conversies, 100% budget verspilling

**OPLOSSING**:
1. Maak nieuwe TRAFFIC campaigns (niet engagement)
2. Alle ads naar kandidatentekort.nl met UTM tracking
3. Custom audiences voor targeting
4. €240/dag effectief verdeeld

## ⚡ 15-MINUTEN QUICK START

```bash
# 1. Check wat je hebt (2 min)
./venv/bin/python validate_meta_setup.py --token "YOUR_TOKEN" --account act_1236576254450117

# 2. Noteer Page ID en Pixel ID uit de output

# 3. Maak audiences (5 min)
./venv/bin/python meta_ads_create_audiences.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --pixel YOUR_PIXEL_ID \
  --page YOUR_PAGE_ID \
  --live

# 4. Maak campaigns (8 min)
./venv/bin/python meta_ads_create_campaign.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --page YOUR_PAGE_ID \
  --live

# KLAAR! 🎉
```

## 📊 RESULTAAT

Na 15 minuten heb je:
- ✅ 15+ Custom Audiences (TOFU/MOFU/BOFU)
- ✅ 3 Traffic Campaigns (Cold, Consider, Retarget)
- ✅ 12 Ads met correcte UTM tracking
- ✅ Alle traffic naar kandidatentekort.nl
- ✅ Volledige GA4 tracking mogelijk

## 🆘 HULP NODIG?

1. **"User request limit"** → Wacht 30 min
2. **"Invalid Page ID"** → Run validate_meta_setup.py eerst
3. **"No Pixel found"** → Check in Events Manager
4. **Scripts werken niet** → Check of je in venv zit: `source venv/bin/activate`

---

**START NU met stap 1!** 🚀