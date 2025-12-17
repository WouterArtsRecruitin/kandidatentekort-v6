# 🚀 DEPLOY NU - KANDIDATENTEKORT.NL FIX

## ✅ WAT IS GEDAAN:
1. **Pixel gefixed:** Alleen 238226887541404 (juiste pixel)
2. **Oude design:** Met "Gratis Vacature Analyse" titel

## 📁 BESTANDEN KLAAR:
- **Zip bestand:** `/Users/wouterarts/projects/kandidatentekort-automation/kandidatentekort-old-design-fixed-pixel.zip`
- **Of folder:** `/Users/wouterarts/projects/kandidatentekort-automation/kandidatentekort-automation/`

## 🌐 DEPLOY STAPPEN:

### OPTIE A: Drag & Drop (Makkelijkst)
1. Ga naar: https://app.netlify.com/sites/kandidatentekort/deploys
2. Sleep de **kandidatentekort-old-design-fixed-pixel.zip** naar het browser venster
3. Wacht tot deploy klaar is
4. KLAAR!

### OPTIE B: Via Netlify CLI
```bash
cd /Users/wouterarts/projects/kandidatentekort-automation/kandidatentekort-automation
netlify deploy --prod --dir=.
```

## ⚙️ ENVIRONMENT VARIABLES (indien nodig):
In Netlify > Site Settings > Environment variables:
- `FACEBOOK_PIXEL_ID` = `238226887541404`
- Verwijder alle andere pixel IDs

## ✅ RESULTAAT:
- Oude design met Gratis Analyse button
- Alleen correcte pixel (238226887541404)
- Geen dubbele pixels meer

---
**ZIP LOCATIE:** `/Users/wouterarts/projects/kandidatentekort-automation/kandidatentekort-old-design-fixed-pixel.zip`