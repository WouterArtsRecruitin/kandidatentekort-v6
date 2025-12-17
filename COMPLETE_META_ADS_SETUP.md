# 🚀 COMPLETE META ADS SETUP - KANDIDATENTEKORT

## 📋 OVERZICHT

Dit is je complete setup voor een werkende Meta Ads funnel met correcte tracking:

1. **Custom Audiences** → Targeting per funnel stage
2. **Traffic Campaigns** → Ads naar kandidatentekort.nl (niet Reels!)
3. **UTM Tracking** → Volledige conversie tracking in GA4
4. **Budget Optimalisatie** → €240/dag effectief verdeeld

## 🎯 STAP-VOOR-STAP IMPLEMENTATIE

### STAP 1: Verkrijg Benodigde IDs

#### A. Facebook Page ID
1. Ga naar je Facebook pagina
2. Klik op "About" → "Page transparency" 
3. Kopieer de Page ID

#### B. Pixel ID
1. Ga naar [Events Manager](https://business.facebook.com/events_manager)
2. Selecteer je pixel
3. Kopieer de Pixel ID uit de URL of settings

### STAP 2: Maak Custom Audiences

```bash
# Preview audiences (geen token nodig)
./venv/bin/python meta_ads_create_audiences.py --preview

# Check bestaande audiences
./venv/bin/python meta_ads_create_audiences.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --list

# Maak alle audiences (dry run)
./venv/bin/python meta_ads_create_audiences.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --pixel YOUR_PIXEL_ID \
  --page YOUR_PAGE_ID

# Maak alle audiences (live)
./venv/bin/python meta_ads_create_audiences.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --pixel YOUR_PIXEL_ID \
  --page YOUR_PAGE_ID \
  --live
```

### STAP 3: Analyseer Huidige Campaigns

```bash
# Deep dive analyse
./venv/bin/python meta_ads_utm_analyzer.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117
```

Dit toont:
- ❌ Welke ads naar Facebook Reels gaan
- ❌ Welke ads geen UTM tracking hebben
- ✅ Welke ads correct zijn ingesteld

### STAP 4: Maak Traffic Campaigns

```bash
# Preview nieuwe campaigns
./venv/bin/python meta_ads_create_campaign.py --preview

# Maak campaigns (dry run)
./venv/bin/python meta_ads_create_campaign.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --page YOUR_PAGE_ID

# Maak campaigns (live)
./venv/bin/python meta_ads_create_campaign.py \
  --token "YOUR_TOKEN" \
  --account act_1236576254450117 \
  --page YOUR_PAGE_ID \
  --live
```

### STAP 5: Update Campaign Targeting

Na het maken van campaigns en audiences, update de targeting in Meta Ads Manager:

#### Cold Campaign (€80/dag):
- **Include**: KT - Lookalike 1% Website Visitors
- **Exclude**: 
  - KT - Website Visitors 30d
  - KT - Converters (Leads)

#### Consideration Campaign (€80/dag):
- **Include**: 
  - KT - Website Visitors 30d
  - KT - Video Viewers 50%
  - KT - Page Engaged 30d
- **Exclude**: 
  - KT - Website Visitors 7d
  - KT - Converters (Leads)

#### Retargeting Campaign (€80/dag):
- **Include**: 
  - KT - Website Visitors 7d
  - KT - Form Starters
  - KT - Video Viewers 95%
- **Exclude**: KT - Converters (Leads)

## 📊 COMPLETE FUNNEL STRUCTUUR

```
COLD AWARENESS (TOFU)
├── Audience: Lookalikes + Cold traffic
├── Budget: €80/dag
├── Ads: 4 varianten (Stats, Problem, Solution, Authority)
└── UTM: utm_campaign=cold_awareness

CONSIDERATION (MOFU)
├── Audience: Engaged maar nog niet hot
├── Budget: €80/dag
├── Ads: 4 varianten (Case Study, Features, Comparison, ROI)
└── UTM: utm_campaign=consideration

RETARGETING (BOFU)
├── Audience: Hot leads (7d visitors, form starters)
├── Budget: €80/dag
├── Ads: 4 varianten (Reminder, Urgency, Social, Bonus)
└── UTM: utm_campaign=retargeting
```

## 🔥 QUICK WINS

### Direct na implementatie:
1. **Pauzeer Reels campaigns** - Stop budget bleeding
2. **Activeer nieuwe Traffic campaigns** - Start tracking
3. **Monitor GA4** - Check of traffic binnenkomt
4. **Test conversie tracking** - Vul zelf een form in

### Na 48 uur:
1. **Check CTR** - Moet >1% zijn
2. **Check CPC** - Moet <€0.50 zijn
3. **Check landing page views** - Moet >80% van clicks zijn
4. **Optimaliseer underperformers** - Pauzeer slechte ads

### Na 1 week:
1. **Analyseer cost per lead** - Target: <€15
2. **Check audience overlap** - Max 20% overlap
3. **A/B test nieuwe creatives** - Vervang bottom 25%
4. **Scale winners** - Verhoog budget voor top performers

## 🛠️ TROUBLESHOOTING

### "User request limit reached"
- Wacht 30 minuten
- Gebruik kleinere batches

### "Invalid Page ID"
- Check of je page admin bent
- Gebruik numeric ID, niet username

### "Pixel not found"
- Verificeer pixel is geïnstalleerd op kandidatentekort.nl
- Check pixel ID in Events Manager

### "No traffic in GA4"
- Check UTM parameters in ad preview
- Verificeer GA4 is correct ingesteld
- Test link direct in browser

## 📈 SUCCES METRICS

Week 1 targets:
- ✅ 100+ website visitors per dag
- ✅ <€0.50 CPC
- ✅ >1% CTR
- ✅ <€15 cost per lead

Maand 1 targets:
- ✅ 40% meer applications
- ✅ 3x ROAS
- ✅ 500+ quality leads
- ✅ Scaling naar €500/dag

## 💡 PRO TIPS

1. **Creative Refresh**: Ververs ads elke 2 weken
2. **Audience Expansion**: Test 3% lookalikes na succes
3. **Landing Page**: A/B test verschillende headlines
4. **Follow-up**: Email automation voor leads
5. **Reporting**: Weekly dashboard in Google Sheets

---

**🚨 START NU**: Begin met Stap 2 (Custom Audiences) terwijl je wacht op Page/Pixel IDs!