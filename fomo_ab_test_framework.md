# 🚀 FOMO/SCARCITY A/B TESTING FRAMEWORK - KANDIDATENTEKORT

## 📊 Campaign Structure Overview

### Campaign Hierarchy
```
Kandidatentekort FOMO Campaign
├── COLD Audience Campaign
│   └── Cold-Awareness AdSet (€80/day)
│       ├── Ad A: €500/Day Loss (€20/day)
│       ├── Ad B: Competitor Threat (€20/day)
│       ├── Ad C: 3 Months Pain (€20/day)
│       └── Ad D: 24h Urgency (€20/day)
│
├── WARM Audience Campaign  
│   └── Warm-Engaged AdSet (€80/day)
│       ├── Ad A: Calculator Shock (€20/day)
│       ├── Ad B: Social Urgency (€20/day)
│       ├── Ad C: Price Anchor (€20/day)
│       └── Ad D: Waiting Costs (€20/day)
│
└── HOT Audience Campaign
    └── Hot-Retargeting AdSet (€80/day)
        ├── Ad A: Analysis Ready (€20/day)
        ├── Ad B: Spot Expires (€20/day)
        ├── Ad C: Bonus Offer (€20/day)
        └── Ad D: Final Warning (€20/day)
```

## 🎯 FOMO Ad Copy Matrix

### COLD AUDIENCE - Pain Discovery
| Variant | Hook | Pain Point | CTA |
|---------|------|-----------|-----|
| A | €500/dag verlies | Productiviteit drain | Stop het bloeden → |
| B | Concurrenten pikken kandidaten | FOMO on talent | Krijg direct inzicht → |
| C | 3 maanden = €36k | Accumulated loss | Stop het NU → |
| D | LAATSTE 24 UUR | Scarcity trigger | Claim gratis analyse → |

### WARM AUDIENCE - Cost Awareness  
| Variant | Hook | Pain Amplification | CTA |
|---------|------|-------------------|-----|
| A | €847/dag calculator | Shock value | Check jouw kosten → |
| B | 127 bedrijven deze week | Social proof + urgency | Claim jouw plek → |
| C | Morgen €297 | Price anchoring | Grijp vandaag kans → |
| D | €3.500/week verlies | Time pressure | Start NU → |

### HOT AUDIENCE - Decision Pressure
| Variant | Hook | Urgency Driver | CTA |
|---------|------|---------------|-----|
| A | Analyse staat KLAAR | Availability | Check inbox NU → |
| B | Vervalt over 48 uur | Expiration | Claim of verlies → |
| C | BONUS €500 waarde | Added value | Alleen vandaag → |
| D | LAATSTE WAARSCHUWING | Final chance | Dit is het moment → |

## 📈 Performance Tracking Setup

### UTM Structure
```
Base URL: https://kandidatentekort.nl/

UTM Parameters:
- utm_source=meta
- utm_medium=paid  
- utm_campaign=kt_[audience]_fomo
- utm_content=[variant_identifier]
- utm_term=v2_[date]

Example:
https://kandidatentekort.nl/?utm_source=meta&utm_medium=paid&utm_campaign=kt_cold_fomo&utm_content=500eur_loss&utm_term=v2_dec2024
```

### KPI Targets by Audience

#### COLD Audience
- **CTR Target**: 3-4%
- **CPC Target**: €2-3
- **CVR Target**: 2-3%
- **CPA Target**: €10-15

#### WARM Audience  
- **CTR Target**: 4-5%
- **CPC Target**: €1.50-2.50
- **CVR Target**: 5-7%
- **CPA Target**: €8-12

#### HOT Audience
- **CTR Target**: 5-7%
- **CPC Target**: €1-2
- **CVR Target**: 10-15%
- **CPA Target**: €5-8

## 🧪 A/B Testing Protocol

### Week 1: Baseline Establishment
- Run all variants with equal budget (€20/day each)
- No changes for first 7 days
- Collect minimum 100 clicks per variant

### Week 2: Initial Optimization
- Pause bottom 25% performers
- Reallocate budget to top 75%
- Introduce new challenger variants

### Week 3: Scale Winners
- Double budget on top 2 variants per audience
- Test new creative formats (video/carousel)
- Implement dynamic retargeting

### Week 4: Full Optimization
- Focus 80% budget on proven winners
- 20% budget for continuous testing
- Roll out to lookalike audiences

## 📱 Creative Best Practices

### Visual Guidelines
```
COLD Ads:
- Dark background (urgency)
- Red accents (€ loss focus)
- Bold numbers prominent
- Calculator/clock icons

WARM Ads:
- Split screen designs
- Before/after visualization  
- Green success indicators
- Company logos for trust

HOT Ads:
- Countdown timers
- "Limited spots" badges
- Urgent color schemes
- Personal touches
```

### Copy Formula
```
[HOOK - Max 40 chars]
[PAIN - Specific number/timeframe]
[SOLUTION - What we do]
[URGENCY - Time/availability limit]
[CTA - Action verb]
```

## 📊 Reporting Dashboard

### Daily Metrics
```sql
Campaign Performance:
- Impressions by variant
- CTR by hook type
- CPC trends
- Quality Score

Conversion Tracking:
- Form starts vs completions
- Drop-off points
- Time to convert
- Device breakdown
```

### Weekly Analysis
1. **Winner Identification**
   - Top CTR variant per audience
   - Lowest CPA variant
   - Highest CVR variant

2. **Loser Analysis**  
   - Why did they fail?
   - salvageable elements?
   - Learnings for next iteration

3. **Budget Reallocation**
   - Shift to performers
   - Maintain test budget
   - Scale considerations

## 🎯 Quick Implementation Checklist

### Pre-Launch
- [ ] Ad account access confirmed
- [ ] Pixel installed and firing
- [ ] UTM template created
- [ ] GA4 goals configured
- [ ] Landing page optimized

### Launch Day
- [ ] All ads uploaded
- [ ] Budgets set equally  
- [ ] Scheduling configured
- [ ] Tracking verified
- [ ] Team notified

### Daily Tasks
- [ ] Check spend pacing
- [ ] Monitor CTR trends
- [ ] Verify tracking
- [ ] Note observations
- [ ] Screenshot top performers

### Weekly Tasks
- [ ] Full performance review
- [ ] Budget reallocation
- [ ] New variant creation
- [ ] Report generation
- [ ] Strategy adjustment

## 💰 Budget Scaling Framework

### Performance Thresholds
```
Scale UP when:
- CTR > 4% for 3+ days
- CPA < €10 for 50+ conversions
- CVR > 5% consistent

Scale DOWN when:
- CTR < 2% for 3+ days
- CPA > €20 for 7 days
- Quality Score < 5/10

PAUSE when:
- CTR < 1%
- 0 conversions after €100 spend
- Negative feedback > 1%
```

### Scaling Rules
1. **20% Rule**: Increase by max 20% daily
2. **3-Day Rule**: Wait 3 days between changes
3. **Variant Rule**: Always keep 1 test variant
4. **Budget Cap**: Max €500/day without approval

## 📋 Emergency Protocols

### If Performance Drops
1. Check tracking first (90% of issues)
2. Verify landing page is up
3. Review ad rejection notices
4. Check competitive landscape
5. Pause and investigate

### If Costs Spike
1. Check for audience overlap
2. Review placement performance
3. Verify bid cap settings
4. Check time of day patterns
5. Implement hourly budgets

## 🚀 Go-Live Commands

```bash
# Deploy FOMO campaigns
python update_campaigns_fomo_scarcity.py \
  --token YOUR_TOKEN \
  --campaigns COLD_ID WARM_ID HOT_ID

# Quick deploy (simplified)
python quick_deploy_fomo_ads.py

# Monitor performance
python track_fomo_performance.py --hours 24
```

## ✅ Success Metrics

**Week 1 Success**:
- All ads approved and running
- CTR baseline established
- Tracking 100% accurate

**Month 1 Success**:
- 30% CTR improvement
- 25% CPA reduction  
- 2x conversion volume

**Quarter 1 Success**:
- €5-8 CPA achieved
- 500+ conversions/month
- 5x ROAS maintained

---

**Ready to launch? The €500/day message is locked and loaded! 🎯**