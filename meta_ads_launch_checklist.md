# 🚀 META ADS - FINAL LAUNCH CHECKLIST

**Campaign:** Kandidatentekort - Expert Recruitment Q1 2025  
**Budget:** €47/dag = €1,410/mnd  
**Target:** 56-70 leads @ €20-25 CPL

---

## ✅ PRE-LAUNCH CHECKLIST (voor je activeert)

### 1. ADS MANAGER REVIEW (5 min)

**Open:** https://business.facebook.com/adsmanager/manage/campaigns?act=1236576254450117&selected_campaign_ids=120240987303750536

**Check per ad:**
- [ ] Image loaded correctly (niet blurry/gecropped)
- [ ] Primary text zichtbaar en compleet
- [ ] Headline: "Gratis Vacature Check"
- [ ] CTA button: "Learn More"
- [ ] Landing page URL correct (met UTM parameters)
- [ ] Mobile preview OK (70% van traffic!)

**Quick fixes als iets niet klopt:**
- Image issue → Re-upload via "Edit Ad"
- Copy issue → Edit primary text/headline
- URL issue → Update destination URL

---

### 2. KANDIDATENTEKORT.NL CHECK (10 min)

**Test landing page:**
- [ ] Website laadt (<2s load time)
- [ ] HTTPS actief (groene slotje browser)
- [ ] Mobile responsive (test op iPhone)
- [ ] Lead form zichtbaar above fold
- [ ] CTA button werkt ("Start Gratis Check")
- [ ] Form submission werkt (test met je eigen email)

**Meta Pixel test:**
1. Install Chrome extension: "Meta Pixel Helper"
2. Visit kandidatentekort.nl
3. Should see: Pixel 238226887541404 - PageView event
4. Green checkmark = working ✅

**Als pixel niet werkt:**
```html
<!-- Add to kandidatentekort.nl <head> -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '238226887541404');
fbq('track', 'PageView');
</script>
```

---

### 3. PIPEDRIVE INTEGRATION CHECK (5 min)

**Test flow:**
1. Submit test lead via kandidatentekort.nl
2. Check Jotform submission ontvangen
3. Check Pipedrive → New deal created
4. Verify fields gemapped:
   - Bedrijfsnaam → Organization
   - Email → Person
   - Stad → Custom field "Locatie"
   - Source → "Meta Ads"

**Als iets niet werkt:**
- Check Jotform → Pipedrive integration in Zapier
- Verify custom fields mapped correct
- Test manual submission

---

### 4. UTM TRACKING SETUP (3 min)

**Test UTM parameters werken:**

Visit each URL manually:
```
https://kandidatentekort.nl?utm_source=meta&utm_medium=paid_social&utm_campaign=expert_q1_2025&utm_content=utrecht
```

**Check in Google Analytics (if you use it):**
- Real-time → Traffic Sources
- Should show: meta / paid_social

**Check in Jotform:**
- Hidden fields should capture UTM values
- These should flow to Pipedrive deal

---

## 🎯 ACTIVATION STRATEGY

### Option A: FULL LAUNCH (recommended)
**Activate all 13 ad sets at once**

**Pros:**
✅ Quick data gathering
✅ Test all markets simultaneously
✅ Clear winners/losers within 3 days

**Cons:**
❌ Higher initial spend if CPL is bad
❌ Need to monitor closely first 48h

**Budget:** €47/dag from day 1

---

### Option B: PHASED ROLLOUT (safer)

**Phase 1 (Days 1-3): Top 3 cities**
- Utrecht (€6/dag)
- Eindhoven (€5/dag)
- Arnhem (€5/dag)
- **Total: €16/dag**

**Phase 2 (Days 4-7): Add Tier 2**
- + Nijmegen, Apeldoorn, Enschede
- **Total: €28/dag**

**Phase 3 (Day 8+): Full rollout**
- + All remaining 7 cities
- **Total: €47/dag**

**Pros:**
✅ Lower risk
✅ Learn from top cities first
✅ Optimize before scaling

**Cons:**
❌ Slower data gathering
❌ Takes 2 weeks to full budget

---

### Option C: BUDGET CAPS (most conservative)

**Week 1 limits:**
- Max €100/week total spend
- Auto-pause if CPL >€40
- Scale only if CPL <€20

**Pros:**
✅ Maximum safety
✅ No surprise costs

**Cons:**
❌ Very slow learning
❌ Takes month to optimize

---

## 📊 MONITORING DASHBOARD (eerste 72 uur)

### Metrics to watch HOURLY (first 24h):

```
URL: https://business.facebook.com/adsmanager/reporting

Filter: Last 24 Hours

Key Metrics:
─────────────────────────────────────
Spend         → Should be ~€47/dag
Impressions   → Target: 15,000-20,000
Link Clicks   → Target: 200-300
CTR           → Target: 2-3%
CPC           → Target: €0.50-0.75
Leads         → Target: 10-15 (first day)
CPL           → Target: €20-25
─────────────────────────────────────
```

### RED FLAGS (pause immediately if):

❌ **CPL >€40** after 50 clicks
❌ **CTR <0.5%** after 1,000 impressions
❌ **Zero leads** after €100 spend
❌ **CPC >€2** sustained for 4 hours

### GREEN FLAGS (scale up if):

✅ **CPL <€15** after 10 leads
✅ **CTR >3%** sustained
✅ **Conversion rate >12%** (clicks to leads)

---

## 🔧 QUICK OPTIMIZATIONS (first week)

### If CPL too high (>€30):

**Test 1: Simplify ad copy**
```
Before: Long explanation
After:  "Vacature moeilijk in te vullen?
         Gratis analyse → kandidatentekort.nl"
```

**Test 2: Change CTA**
```
From: "Learn More"
To:   "Get Quote" or "Sign Up"
```

**Test 3: Adjust targeting**
```
Current: HR interests
Add:    Manufacturing, Business owners, Small business
```

**Test 4: Landing page optimization**
```
- Reduce form fields (max 3)
- Make CTA bigger
- Add urgency ("Nog 5 gratis checks deze week")
```

---

### If CTR too low (<1%):

**Test 1: New images**
- Try carousel design for all cities
- Add urgency text on image
- Test with human faces

**Test 2: Ad copy hooks**
```
Option A: "€23K verloren door langdurige vacature?"
Option B: "67% bedrijven vindt geen technisch personeel"
Option C: "Recruitin vond 500+ kandidaten in jouw regio"
```

**Test 3: Headlines**
```
Current: "Gratis Vacature Check"
Test:    "Vind Technisch Talent - Gratis Check"
Test:    "500+ Plaatsingen - Gratis Advies"
```

---

## 📈 SUCCESS METRICS

### Week 1 Targets:
```
Spend:        €329 (€47/dag × 7 dagen)
Clicks:       200-300
CTR:          2-3%
Leads:        13-16
CPL:          €20-25
Conversion:   8-12%
```

### Month 1 Targets:
```
Spend:          €1,410
Leads:          56-70
Qualified:      14-20 (25% conversion)
Meetings:       10-15 (70% show rate)
Won Deals:      3-5 (20-30% close)
Revenue:        €12,000-22,500
ROI:            8-16×
```

---

## 🚨 EMERGENCY PROCEDURES

### If campaign tanks (CPL >€50):

**Immediate actions:**
1. Pause all ad sets
2. Check kandidatentekort.nl is live
3. Verify pixel is firing
4. Test form submission works
5. Review ad copy for errors

**Then:**
- Reduce budget to €10/dag
- Test only Utrecht ad set
- Optimize landing page
- Fix issues before re-launch

---

### If you get tons of leads (CPL <€10):

**This is GOOD but:**
1. Check lead quality (not spam)
2. Verify Pipedrive receiving correctly
3. Scale budget +20% per day
4. Monitor quality doesn't drop
5. Prepare for follow-up volume

**Scale strategy:**
```
Day 1: €47/dag → 10 leads @ €10 CPL
Day 2: €56/dag (+20%)
Day 3: €67/dag (+20%)
Day 4: €80/dag (+20%)
Week 2: €100/dag (if quality stays high)
```

---

## 📞 LEAD FOLLOW-UP PLAN

### Response time targets:
```
<15 min:  50% of leads (auto-email)
<1 hour:  100% of leads (personal call)
<24 hour: Follow-up if no answer
```

### Auto-email template (via Jotform):
```
Subject: Je gratis vacature analyse [BEDRIJFSNAAM]

Hoi [NAAM],

Bedankt voor je aanvraag! 

Binnen 24 uur ontvang je:
✅ Marktanalyse voor [STAD]
✅ Salaris benchmarks [FUNCTIE]
✅ Kandidaten beschikbaarheid
✅ Recruitment advies op maat

Ik bel je vandaag nog voor vragen.

Groet,
Wouter Arts
DGA - Recruitin B.V.
06 XXXX XXXX
```

---

## 🎯 FINAL DECISION POINT

**You need to choose NOW:**

### A) FULL LAUNCH (€47/dag from day 1)
→ Fastest learning, higher risk
→ Best if: You trust landing page + have capacity for 10-15 leads/dag

### B) PHASED (€16 → €28 → €47/dag over 2 weeks)
→ Safer, slower learning
→ Best if: Want to test water first, limited follow-up capacity

### C) BUDGET CAP (€100/week max)
→ Safest, slowest
→ Best if: Very risk-averse, want to learn gradually

**My recommendation: OPTION A (Full Launch)**

**Why:**
- Campaign structure is solid
- 13 ad sets allow quick A/B testing
- Can pause individual cities if needed
- €1,410/mnd is acceptable risk for potential €12-22K revenue

---

## ✅ ACTIVATION STEPS (when ready)

**In Ads Manager:**

1. **Select campaign** (120240987303750536)
2. **Click "Edit"** (top right)
3. **Change status:** PAUSED → ACTIVE
4. **Confirm delivery estimate**
5. **Click "Publish"**

**Then immediately:**
- Set calendar reminder: Check every 4 hours (first 48h)
- Create monitoring spreadsheet (CPL per city)
- Set up phone for lead calls
- Prepare Pipedrive follow-up workflow

---

## 🎉 YOU'RE READY TO LAUNCH!

**Final checklist:**
- [X] 13 ad sets created (Claude Code)
- [X] 5 Canva designs uploaded
- [X] Ads created with correct copy
- [ ] Kandidatentekort.nl live + pixel working
- [ ] Lead form → Pipedrive tested
- [ ] UTM tracking verified
- [ ] Monitoring plan set up
- [ ] Follow-up process ready

**Missing items?** Fix before activating.

**All checked?** → Activate campaign! 🚀

---

*Setup by Wouter Arts - Recruitin B.V.*  
*Campaign: Kandidatentekort Expert Q1 2025*  
*Budget: €1,410/mnd | Target: 56-70 leads*  
*Launch date: December 2025*
