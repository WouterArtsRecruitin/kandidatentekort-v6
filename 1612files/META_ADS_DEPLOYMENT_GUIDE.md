# ⚡ PRAKTISCHE DEPLOYMENT GUIDE - META ADS MANAGER

**Total Time:** 90 minuten  
**Budget:** €240/dag (€1,680/week)  
**Expected Results:** 70-100 leads/week

---

## 🔧 VOORBEREIDING (20 mins)

### STAP 1: Access Token Genereren
1. **Open:** https://developers.facebook.com/tools/explorer
2. **Select App:** Recruitment APK (1735907367288442)
3. **Permissions:** Voeg toe:
   - `ads_management` ✅
   - `ads_read` ✅
   - `business_management` ✅
4. **Generate Access Token** → **Get Long-Lived Token**
5. **Copy token** → Bewaar veilig

### STAP 2: Images Downloaden
**Google Drive Folder 1:** https://drive.google.com/drive/folders/1IgkGJk-ab4PkQ6XU0dXeYLig_jl_WqOz
**Google Drive Folder 2:** https://drive.google.com/drive/folders/1tAU4IRetVs9mufb8aMDtsowSG9rma7B6
**Google Drive Folder 3:** https://drive.google.com/drive/folders/1Q_6GSnSOTuds2-_atRRfLbFCINOkZQ2V

**Download deze 12 images:**
- `1_Instagram-bericht - Kandidatentekort.png` (Folder 3)
- `33_Facebook-bericht - Tekort aan engineers.png` (Folder 2)
- `split_screen_ad.png` (Folder 1)
- `12_Facebook-bericht - 15 jaar recruitmentervaring.png` (Folder 3)
- `10_Facebook-omslagfoto - 40-60% MEER SOLLICITATIES.png` (Folder 3)
- `25_Facebook-bericht - Proven Recruitment Performance.png` (Folder 2)
- `03_beige_problem_pain.png` (Folder 1)
- `45_Facebook-bericht - 150+ bedrijven gingen je voor.png` (Folder 2)
- `8_Instagram-bericht - Elke dag zonder operator.png` (Folder 3)
- `04_beige_urgency_roi.png` (Folder 1)
- `66_KandidatenTekort Social Proof Carousel.png` (Folder 2)
- `4_Facebook-bericht - Wacht niet. Check nu je vacature.png` (Folder 3)

### STAP 3: Custom Audiences Aanmaken
**Open:** https://business.facebook.com/adsmanager/audiences

#### Audience 1: Website Visitors 30 Days
1. **Create Audience** → **Custom Audience**
2. **Website Traffic**
3. **Name:** "Kandidatentekort - Website Visitors 30d"
4. **URL contains:** `kandidatentekort.nl`
5. **Past 30 days**
6. **Save**

#### Audience 2: Website Visitors 7 Days  
1. **Create Audience** → **Custom Audience**
2. **Website Traffic**
3. **Name:** "Kandidatentekort - Website Visitors 7d"
4. **URL contains:** `kandidatentekort.nl`
5. **Past 7 days**
6. **Save**

#### Audience 3: Form Submitters
1. **Create Audience** → **Custom Audience**
2. **Website Traffic**
3. **Name:** "Kandidatentekort - Form Submitters"
4. **URL contains:** `kandidatentekort.nl/bedankt`
5. **Past 180 days**
6. **Save**

---

## 🚀 CAMPAGNE 1: COLD AWARENESS (25 mins)

### STAP 1: Campaign Aanmaken
**Open:** https://business.facebook.com/adsmanager

1. **Create** → **Campaign**
2. **Objective:** Conversions
3. **Campaign Name:** `Kandidatentekort - Cold Awareness`
4. **Buying Type:** Auction
5. **Campaign Details:**
   - Special Ad Categories: None
   - Campaign Objective: Conversions
6. **Continue**

### STAP 2: Ad Set 1.1 - Brand Introduction
1. **Ad Set Name:** `Cold - Brand Introduction - Gelderland/Overijssel/NB`
2. **Conversion Event:** Complete Registration
3. **Pixel:** Recruitin Content Automation (757606233848402)

#### Budget & Schedule
- **Budget:** €20/day
- **Schedule:** Start today, no end date

#### Audience
- **Custom Audience:** None (cold traffic)
- **Location:** 
  - Gelderland ✅
  - Overijssel ✅
  - Noord-Brabant ✅
- **Age:** 28-55
- **Gender:** All
- **Languages:** Dutch
- **Detailed Targeting:**
  - Human resources ✅
  - Business management ✅
- **Exclude:** Kandidatentekort - Website Visitors 30d

#### Placements
- **Automatic Placements** (recommended)

### STAP 3: Ad Creative 1.1
1. **Ad Name:** `Brand Introduction - Kandidatentekort`
2. **Identity:** Select Recruitin page
3. **Format:** Single Image

#### Creative
- **Image:** Upload `1_Instagram-bericht - Kandidatentekort.png`
- **Headline:** `Kandidatentekort? Wij lossen het op`
- **Primary Text:** 
```
Elke dag dat jouw vacature open staat, kost je geld. Onze gratis analyse laat zien waarom 73% van technische vacatures geen reacties krijgt. 500+ bedrijven gingen je al voor.
```
- **Description:** `Ontdek gratis wat er mis gaat`
- **Call to Action:** Learn More
- **Website URL:** `https://kandidatentekort.nl/gratis-analyse?utm_source=meta&utm_medium=paid&utm_campaign=cold_awareness&utm_content=brand_intro`

4. **Publish**

### STAP 4: Duplicate Ad Set voor 1.2, 1.3, 1.4
**Duplicate Ad Set 1.1** → Wijzig alleen:

#### Ad Set 1.2: Problem Focus
- **Ad Set Name:** `Cold - Problem Focus - Gelderland/Overijssel/NB`
- **Image:** `33_Facebook-bericht - Tekort aan engineers.png`
- **Headline:** `Geen reacties op jouw technische vacature?`
- **Primary Text:**
```
87% van productiebedrijven worstelt met het vinden van technici. Het probleem zit vaak niet in de arbeidsmarkt, maar in hoe jouw vacature wordt gepresenteerd. Ontdek wat er mis gaat.
```
- **Description:** `Gratis vacature-analyse binnen 24 uur`
- **UTM Content:** `problem_focus`

#### Ad Set 1.3: Before/After Visual
- **Ad Set Name:** `Cold - Before/After - Gelderland/Overijssel/NB`
- **Image:** `split_screen_ad.png`
- **Headline:** `Van 0 naar 23 sollicitaties in 3 weken`
- **Primary Text:**
```
Een metaalbedrijf in Gelderland kreeg maandenlang geen reacties. Na onze analyse: 23 gekwalificeerde sollicitaties in 3 weken. Het verschil? Een paar eenvoudige aanpassingen.
```
- **Description:** `Bekijk wat er mogelijk is`
- **UTM Content:** `before_after`

#### Ad Set 1.4: Authority Builder
- **Ad Set Name:** `Cold - Authority - Gelderland/Overijssel/NB`
- **Image:** `12_Facebook-bericht - 15 jaar recruitmentervaring.png`
- **Headline:** `15 jaar technisch recruitment ervaring`
- **Primary Text:**
```
Sinds 2009 helpen wij bedrijven in Gelderland, Overijssel en Noord-Brabant met het vinden van technisch personeel. 500+ succesvolle plaatsingen, 21 dagen gemiddelde tijd-tot-invulling.
```
- **Description:** `Bewezen resultaten, geen risico`
- **UTM Content:** `authority`

---

## 🤔 CAMPAGNE 2: CONSIDERATION (25 mins)

### STAP 1: Campaign Aanmaken
1. **Create** → **Campaign**
2. **Objective:** Conversions
3. **Campaign Name:** `Kandidatentekort - Consideration`
4. **Continue**

### STAP 2: Shared Ad Set Settings
- **Conversion Event:** Complete Registration
- **Budget:** €20/day per ad set
- **Custom Audience:** Kandidatentekort - Website Visitors 30d ✅
- **Exclude:** Kandidatentekort - Form Submitters ✅

#### Ad Set 2.1: Results Promise
- **Image:** `10_Facebook-omslagfoto - 40-60% MEER SOLLICITATIES.png`
- **Headline:** `40-60% meer sollicitaties gegarandeerd`
- **Primary Text:**
```
Onze klanten krijgen gemiddeld 2.3x meer reacties na implementatie van onze aanbevelingen. Geen vage adviezen, maar concrete verbeteringen die direct impact hebben.
```
- **UTM Campaign:** `consideration`
- **UTM Content:** `results_promise`

#### Ad Set 2.2: Social Proof  
- **Image:** `25_Facebook-bericht - Proven Recruitment Performance.png`
- **Headline:** `150+ bedrijven gebruiken onze methode`
- **Primary Text:**
```
Van kleine machinebouwers tot grote productiebedrijven. Onze aanpak werkt in elke technische sector. 92% van onze klanten komt terug voor meer vacatures.
```
- **UTM Content:** `social_proof`

#### Ad Set 2.3: Pain Point Deep Dive
- **Image:** `03_beige_problem_pain.png`
- **Headline:** `Waarom solliciteert niemand op jouw vacature?`
- **Primary Text:**
```
De meeste bedrijven maken dezelfde 5 fouten in hun vacatureteksten. Deze fouten zorgen ervoor dat gekwalificeerde kandidaten jouw advertentie overslaan. Ontdek welke fouten jij maakt.
```
- **UTM Content:** `pain_deep`

#### Ad Set 2.4: FOMO Builder
- **Image:** `45_Facebook-bericht - 150+ bedrijven gingen je voor.png`
- **Headline:** `150+ bedrijven gingen je al voor`
- **Primary Text:**
```
Terwijl jij nog zoekt naar personeel, hebben 150+ bedrijven onze gratis analyse al gebruikt om hun vacatures te verbeteren. Zij krijgen nu structureel meer en betere sollicitaties.
```
- **UTM Content:** `fomo`

---

## 🎯 CAMPAGNE 3: RETARGETING (25 mins)

### STAP 1: Campaign Aanmaken
1. **Create** → **Campaign**
2. **Objective:** Conversions
3. **Campaign Name:** `Kandidatentekort - Retargeting`
4. **Continue**

### STAP 2: Shared Ad Set Settings
- **Conversion Event:** Complete Registration
- **Budget:** €20/day per ad set
- **Custom Audience:** Kandidatentekort - Website Visitors 7d ✅
- **Exclude:** Kandidatentekort - Form Submitters ✅

#### Ad Set 3.1: Urgency Focus
- **Image:** `8_Instagram-bericht - Elke dag zonder operator.png`
- **Headline:** `Elke dag kost je €180 aan gemiste productie`
- **Primary Text:**
```
Een gemiste operator kost het gemiddelde productiebedrijf €180 per dag aan verloren omzet. Stop met zoeken, start met de juiste aanpak. Onze analyse laat precies zien wat er moet veranderen.
```
- **UTM Campaign:** `retargeting`
- **UTM Content:** `urgency_cost`

#### Ad Set 3.2: ROI Calculator
- **Image:** `04_beige_urgency_roi.png`
- **Headline:** `€7.990 investering = €45.000+ besparing`
- **Primary Text:**
```
Gemiddeld bespaart een bedrijf €45.000+ op recruitment kosten door onze aanpak te gebruiken. Van dure bureaus naar eigen succesvolle werving in 30 dagen.
```
- **UTM Content:** `roi_calc`

#### Ad Set 3.3: Testimonial Carousel
- **Image:** `66_KandidatenTekort Social Proof Carousel.png`
- **Headline:** `Dit zeggen onze klanten`
- **Primary Text:**
```
'Binnen 2 weken hadden we 12 sollicitaties op onze lasser-vacature. Daarvoor kregen we er 0.' - Marcel, Productiebedrijf Gelderland. Ontdek wat er mogelijk is voor jouw bedrijf.
```
- **UTM Content:** `testimonials`

#### Ad Set 3.4: Final CTA
- **Image:** `4_Facebook-bericht - Wacht niet. Check nu je vacature.png`
- **Headline:** `Laatste kans: Gratis vacature-check`
- **Primary Text:**
```
Je hebt onze advertenties gezien, onze resultaten bekeken. Nu is het tijd voor actie. Krijg binnen 24 uur een complete analyse van jouw vacature. 100% gratis, geen verplichtingen.
```
- **UTM Content:** `final_cta`

---

## 📊 POST-LAUNCH SETUP (15 mins)

### STAP 1: Performance Monitoring
**Google Sheets Dashboard:** https://docs.google.com/spreadsheets/d/1Tp1Ygj9ZVeFYZS9yCoMHUcO5wL7nU_lhgLpJYV74Onw

Log deze gegevens:
- Campaign IDs
- Ad Set IDs  
- Daily budgets
- Launch timestamps
- UTM parameters

### STAP 2: Slack Notifications
**Channel:** #meta-campaign-alerts
**Message:**
```
🚀 KANDIDATENTEKORT CAMPAIGNS LIVE!

📊 Campaign Summary:
• Cold Awareness: 4 ads @ €20/day = €80/day
• Consideration: 4 ads @ €20/day = €80/day  
• Retargeting: 4 ads @ €20/day = €80/day
• TOTAL BUDGET: €240/day (€1,680/week)

🎯 Expected Results:
• 70-100 leads/week
• €17-24 CPA
• 2.5-3.5% CTR

⏰ Launch Time: [TIMESTAMP]
👀 Monitor: business.facebook.com/adsmanager
```

### STAP 3: Daily Monitoring Checklist
**Week 1 - Check elke dag:**
- [ ] Spend vs Budget (should be 95-105%)
- [ ] CTR (target: >2.0%)
- [ ] CPA (target: <€30)
- [ ] Ad approval status
- [ ] Landing page form submissions

**Week 2+ - Check 3x per week:**
- [ ] Performance trends
- [ ] Audience saturation (frequency <3.0)
- [ ] Creative fatigue (CTR declining)
- [ ] Conversion tracking

---

## 🚨 TROUBLESHOOTING

### Ads Stuck in Review (>24h)
1. Check ad content for policy violations
2. Verify landing page compliance
3. Contact Meta Support if needed

### Low CTR (<1.5%)
1. Test new headlines
2. Refresh creative images  
3. Adjust audience targeting

### High CPA (>€35)
1. Optimize for higher-funnel events (Page View)
2. Expand audience size
3. Increase budget for better optimization

### No Conversions  
1. Verify pixel firing correctly
2. Check landing page form functionality
3. Review conversion event setup

---

## ✅ SUCCESS METRICS

### Week 1 Targets
- **Total Spend:** €1,680
- **Total Leads:** 70-100
- **Average CPA:** €17-24
- **CTR:** 2.5-3.5%
- **Conversion Rate:** 4-7%

### Month 1 Targets  
- **Total Spend:** €7,200
- **Total Leads:** 300-360
- **Pipeline Value:** €150,000-180,000
- **ROI:** 2000-2400%

---

*Ready for immediate deployment!*  
*Total setup time: 90 minutes*  
*Expected first lead: Within 24-48 hours*