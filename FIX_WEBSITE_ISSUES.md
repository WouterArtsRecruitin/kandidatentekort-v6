# 🚨 KANDIDATENTEKORT.NL - WEBSITE FIXES NEEDED

## ❌ PROBLEEM 1: Verkeerde Facebook Pixel
**Huidige situatie:**
- Website heeft 2 pixels: `517991158551582` (FOUT) en `238226887541404` (GOED)
- Alleen `238226887541404` moet blijven

**Fix via Netlify:**
1. Ga naar: https://app.netlify.com/sites/kandidatentekort/settings/env
2. Update/Check deze variables:
   - `FACEBOOK_PIXEL_ID` = `238226887541404`
   - `REACT_APP_FB_PIXEL_ID` = `238226887541404`
   - `NEXT_PUBLIC_FB_PIXEL_ID` = `238226887541404`

## ❌ PROBLEEM 2: Verkeerd Design (Nieuw i.p.v. Oud)
**Moet terug naar oude design met:**
- "Gratis Analyse" button
- Assessment formulier
- Originele layout

**Mogelijke oplossingen:**

### Optie A: Rollback in Netlify
1. Ga naar: https://app.netlify.com/sites/kandidatentekort/deploys
2. Zoek een oudere deploy van voor het nieuwe design
3. Klik "Publish deploy" op de oude versie

### Optie B: Check Git Branches
```bash
# In je kandidatentekort repository:
git branch -a  # Lijst alle branches
git checkout main  # Of master
git log --oneline | head -20  # Bekijk commits

# Rollback naar oudere commit:
git checkout <oude-commit-hash>
git push netlify HEAD:main --force
```

### Optie C: Environment Variable
Check of er een feature flag is:
- `REACT_APP_NEW_DESIGN=false`
- `USE_OLD_DESIGN=true`
- `FEATURE_NEW_UI=false`

## 📋 QUICK FIXES VIA NETLIFY UI:

1. **Login Netlify:** https://app.netlify.com
2. **Open Site:** kandidatentekort
3. **Go to Deploys:** Kies oude werkende versie
4. **Environment Variables:** 
   - Verwijder alle pixel IDs behalve `238226887541404`
   - Zet feature flags voor oude design

## 🔧 DIRECTE ACTIE:
1. Netlify > Deploys > Rollback naar versie van ~2 weken geleden
2. Netlify > Environment > Fix Pixel ID
3. Clear cache en test

---

**Site ID:** 3c89912a-f1be-4c6c-ba73-03ba7fdc8dc7
**Juiste Pixel:** 238226887541404