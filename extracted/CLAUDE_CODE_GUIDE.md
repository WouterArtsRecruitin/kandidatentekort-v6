# 🤖 CLAUDE CODE DEPLOYMENT GUIDE

**Automated kandidatentekort.nl tracking deployment via Claude Code CLI**

---

## 🚀 QUICK START

### Optie 1: Direct Uitvoeren (AANBEVOLEN)

```bash
# Download script
curl -o deploy.sh https://raw.githubusercontent.com/WouterArtsRecruitin/Kandidatentekortfull/main/deploy_with_claude_code.sh

# Make executable
chmod +x deploy.sh

# Run met Claude Code
claude code run ./deploy.sh
```

**Klaar in 5 minuten!** 🎉

---

### Optie 2: Via Claude Code Chat

Start Claude Code en zeg:

```
Deploy kandidatentekort.nl tracking v2.0:

1. Clone/update repo: WouterArtsRecruitin/Kandidatentekortfull
2. Backup index.html
3. Inject tracking code voor </head>:
   - Google Consent Mode v2
   - Cookiebot: 255025f6-3932-479b-a9d7-6a4fac614cb8
   - GA4: G-67PJ02SXVN
   - Meta Pixel: 517991158551582
   - UTM capture + 7 custom events
4. Git commit & push
5. Wait 3 min voor Netlify build
6. Verify deployment

Execute nu!
```

---

## 📋 WAT DOET HET SCRIPT?

### Automated Steps

1. **Repository Setup**
   - Clone of pull latest van GitHub
   - Switch naar main branch

2. **Backup**
   - Maakt timestamped backup van index.html
   - Safety first!

3. **Tracking Code Genereren**
   - Google Consent Mode v2
   - Cookiebot GDPR compliance
   - GA4 tracking
   - Meta Pixel
   - UTM parameter capture
   - 7 custom events

4. **Index.html Updaten**
   - Remove old tracking (als aanwezig)
   - Inject nieuwe code voor `</head>`
   - Preserve alle andere content

5. **Git Commit & Push**
   - Stage changes
   - Commit met detailed message
   - Push naar main branch

6. **Netlify Deployment**
   - Netlify detecteert GitHub push
   - Auto-build triggered
   - Wait 3 minutes

7. **Verification**
   - Fetch live site
   - Check voor GA4 ID
   - Check voor Meta Pixel
   - Check voor Cookiebot
   - Check voor gtag/fbq functions
   - Check voor UTM capture
   - Check voor custom events

8. **Summary Report**
   - Deployment status
   - Verification results
   - Next steps
   - Expected impact

---

## ✅ VERIFICATION CHECKLIST

Script voert automatisch uit:

```
✅ GA4 tracking found (G-67PJ02SXVN)
✅ Meta Pixel found (517991158551582)
✅ Cookiebot found (255025f6-3932-479b-a9d7-6a4fac614cb8)
✅ gtag function found
✅ fbq function found
✅ UTM capture script found
✅ Custom events found
```

**Score:** 7/7 checks = Deployment successful! 🎉

---

## 🔧 TROUBLESHOOTING

### Script Fails: "index.html not found"
**Fix:**
```bash
cd Kandidatentekortfull
ls -la index.html  # Should exist
```

### Script Fails: "Could not find </head>"
**Fix:**
- Check index.html heeft valid HTML
- Search voor `</head>` tag

### Verification Fails: Checks 0/7
**Fix:**
- Wait extra 2-3 minuten voor Netlify
- Hard refresh: Cmd+Shift+R
- Check Netlify deploy logs

### Git Push Fails: Authentication
**Fix:**
```bash
# Setup GitHub token
git config --global credential.helper store
# Paste token when prompted
```

---

## 🎯 MANUAL VERIFICATION

Na script completion:

### Browser Console
```
1. Open: https://kandidatentekort.nl
2. F12 → Console
3. Should see:
   "✅ Tracking active"
   
4. Check functions:
   typeof gtag  // → "function"
   typeof fbq   // → "function"
```

### Network Tab
```
1. F12 → Network
2. Filter: "gtag"
3. Refresh page
4. Should see:
   - gtag/js?id=G-67PJ02SXVN
   - collect?v=2... (after interactions)
```

### Event Test
```
1. Click CTA button
2. Console: "🎯 CTA clicked"
3. Network: collect?v=2... (GA4 event)
```

### GA4 Realtime
```
1. https://analytics.google.com
2. Property: kandidatentekort.nl
3. Reports → Realtime
4. Should see: 1 active user
```

### Meta Pixel Helper
```
1. Install Chrome extension
2. Visit site
3. Extension icon: Green ✅
4. Events: PageView firing
```

---

## 📊 POST-DEPLOYMENT SETUP

### Week 1: GA4 Configuration

**Custom Dimensions:**
```
GA4 → Admin → Custom definitions → Create:
- utm_source (Event, parameter: utm_source)
- utm_medium (Event, parameter: utm_medium)
- utm_campaign (Event, parameter: utm_campaign)
- utm_content (Event, parameter: utm_content)
- utm_term (Event, parameter: utm_term)
```

**Mark Conversion:**
```
GA4 → Admin → Events → generate_lead → Mark as conversion
```

**Data Retention:**
```
GA4 → Admin → Data settings → Data retention → 26 months
```

### Week 2: Meta Ads Launch

**Campaign Setup:**
```
- Campaign: KT_VacatureAnalyse_Dec24
- Objective: Leads
- Budget: €600/maand
- Ad Sets: 15 (€1.33/day each)
- Ads: 20 variants (4 groups × 5)
```

**Audiences:** (zie META_ADS_UTM_TRACKING.md)
- HR Managers 30-50 Gelderland
- Operations Directors Oil & Gas
- HR Tech Companies 50-200 FTE
- Recruiters Overijssel
- etc. (15 total)

**Ad Variants:** (zie META_ADS_UTM_TRACKING.md)
- Problem-focused (5 ads)
- Solution-focused (5 ads)
- Social proof (5 ads)
- Urgency/scarcity (5 ads)

---

## 🔄 ROLLBACK PROCEDURE

Als deployment mis gaat:

### Via Script Backup
```bash
cd Kandidatentekortfull

# List backups
ls -lt index.html.backup.*

# Restore latest backup
cp index.html.backup.20251214_143022 index.html

# Commit & push
git add index.html
git commit -m "rollback: restore previous version"
git push origin main
```

### Via GitHub History
```bash
cd Kandidatentekortfull

# View commit history
git log --oneline

# Revert to previous commit
git revert HEAD

# Push
git push origin main
```

### Via Netlify Dashboard
```
1. https://app.netlify.com
2. Select kandidatentekort site
3. Deploys tab
4. Find previous successful deploy
5. Click "Publish deploy"
```

---

## 💰 EXPECTED IMPACT

### Conservative (Month 1)
```
Budget: €600
Leads: 30 @ €20 CPL
Conversion: 3%
Deals: 0.9
Revenue: €7,191
ROI: 1,199%
```

### Optimized (Month 3)
```
Budget: €600
Leads: 60 @ €10 CPL
Conversion: 5%
Deals: 3
Revenue: €23,970
ROI: 3,995%
```

### Scale (€2,000/month)
```
Budget: €2,000
Leads: 200 @ €10 CPL
Conversion: 5%
Deals: 10
Revenue: €79,900
ROI: 3,995%
```

---

## 📚 DOCUMENTATION

**Master Index:**
`README_MASTER_INDEX.md` - Complete overview

**Deployment Guides:**
- `DEPLOYMENT_GUIDE.md` - Manual deployment
- `DEPLOYMENT_SUMMARY.md` - Complete summary
- `EXECUTE_NOW.md` - Quick start guide
- `CLAUDE_CODE_GUIDE.md` - **← YOU ARE HERE**

**Configuration:**
- `META_ADS_UTM_TRACKING.md` - 15 audiences × 20 ads
- `GA4_DASHBOARD_CONFIG.md` - Dashboard setup

**Scripts:**
- `deploy_with_claude_code.sh` - Claude Code automation
- `deploy_tracking.sh` - Bash automation
- `deploy_full_stack.js` - Node.js automation

---

## 🎯 RECOMMENDED WORKFLOW

**TODAY (5 min):**
```bash
# Execute deployment
claude code run ./deploy_with_claude_code.sh

# Verify in browser
open https://kandidatentekort.nl
# F12 → Console → Check "✅ Tracking active"
```

**THIS WEEK (3 hours):**
```
□ Setup GA4 custom dimensions
□ Mark generate_lead as conversion
□ Create basic dashboard
```

**NEXT WEEK (6 hours):**
```
□ Launch Meta Ads campaign
□ Build full GA4 dashboard
□ Setup email reports
```

**THIS MONTH:**
```
□ Optimize ad performance
□ Scale winners, pause losers
□ Achieve 30+ leads
□ Close first deals
```

---

## ✨ FEATURES

### What Script Does Automatically

✅ **Repository Management**
- Clone/update from GitHub
- Branch management
- Backup creation

✅ **Code Generation**
- Dynamic tracking code
- Timestamp injection
- ID substitution

✅ **File Updates**
- Safe backup before changes
- Precise injection point
- Content preservation

✅ **Git Operations**
- Intelligent staging
- Detailed commit messages
- Automatic push

✅ **Deployment Trigger**
- Netlify auto-detection
- Build monitoring
- Wait for completion

✅ **Verification**
- 7-point checklist
- Live site testing
- Component validation

✅ **Reporting**
- Deployment summary
- Verification results
- Next steps guidance

---

## 🔒 SAFETY FEATURES

### Backup Strategy
- Timestamped backups before changes
- Preserve in Git history
- Easy rollback

### Verification
- Multi-point checking
- Live site validation
- Component testing

### Error Handling
- Exit on error (set -e)
- Validation checks
- Clear error messages

---

## 🚀 ADVANTAGES VS MANUAL

| Aspect | Manual | Claude Code Script |
|--------|--------|-------------------|
| **Time** | 30-60 min | 5 min |
| **Errors** | High risk | Low risk |
| **Consistency** | Variable | 100% |
| **Verification** | Manual | Automatic |
| **Documentation** | None | Complete |
| **Rollback** | Complex | Simple |
| **Repeatability** | Difficult | Easy |

---

## 📞 SUPPORT

**Documentation:**
- Master Index: `README_MASTER_INDEX.md`
- Deployment Guide: `DEPLOYMENT_GUIDE.md`
- Execute Now: `EXECUTE_NOW.md`

**Tools:**
- GitHub: https://github.com/WouterArtsRecruitin/Kandidatentekortfull
- Netlify: https://app.netlify.com
- GA4: https://analytics.google.com
- Meta: https://business.facebook.com/events_manager

**Scripts:**
- Claude Code: `deploy_with_claude_code.sh`
- Bash: `deploy_tracking.sh`
- Node.js: `deploy_full_stack.js`

---

## ✅ FINAL CHECKLIST

### Pre-Run
- [x] Claude Code CLI installed
- [ ] GitHub access configured
- [ ] Script downloaded
- [ ] Script made executable

### Run
- [ ] Execute: `claude code run ./deploy_with_claude_code.sh`
- [ ] Wait for completion (5 min)
- [ ] Review verification results

### Post-Run
- [ ] Open site in browser
- [ ] Check console for "✅ Tracking active"
- [ ] Test CTA click
- [ ] Verify GA4 Realtime
- [ ] Check Meta Pixel Helper

### Week 1
- [ ] Setup GA4 custom dimensions
- [ ] Mark conversions
- [ ] Create dashboard

### Week 2
- [ ] Launch Meta Ads
- [ ] Monitor performance
- [ ] Optimize campaigns

---

**🎉 READY TO DEPLOY!**

```bash
claude code run ./deploy_with_claude_code.sh
```

**Expected time:** 5 minutes  
**Expected impact:** €23,970/maand  
**Expected ROI:** 3,995%

**LET'S GO! 🚀**
