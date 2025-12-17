# 🚨 URGENTE FIX VOOR KANDIDATENTEKORT.NL

## PROBLEEM:
- Je hebt **kandidatentekortv2** Netlify site (niet de originele)
- GitHub pushes naar oude repo werken niet
- Modern design staat nog steeds online

## SNELSTE OPLOSSING (1 minuut):

### Optie 1: Direct Upload in Netlify
1. Ga naar: https://app.netlify.com/sites/kandidatentekortv2/deploys
2. Sleep deze hele folder naar de browser:
   ```
   /Users/wouterarts/projects/kandidatentekort-automation/old-design/kandidatentekort-automation/
   ```
3. Klaar! Het oude design is dan live met juiste pixel

### Optie 2: Rollback naar oude deploy
1. Ga naar: https://app.netlify.com/sites/kandidatentekortv2/deploys
2. Scroll naar beneden naar deploys van **voor 10 december**
3. Klik op een oude deploy
4. Klik "Publish deploy"

### Optie 3: Check welke GitHub repo gekoppeld is
1. Ga naar: https://app.netlify.com/sites/kandidatentekortv2/settings/deploys
2. Kijk welke GitHub repository gekoppeld is
3. Push naar DIE repository (niet de oude)

## ✅ HET OUDE DESIGN HEEFT:
- Correcte pixel: 238226887541404
- Assessment form
- Klassiek design (geen gradient)

**FOLDER MET JUISTE BESTANDEN:**
`/Users/wouterarts/projects/kandidatentekort-automation/old-design/kandidatentekort-automation/`