# FOMO Campaign Images Guide

## 🖼️ Image Strategy for FOMO Campaigns

### Option 1: Use Existing High-Performing Images
The script is designed to work with your existing images. Simply add image URLs or media IDs to the creative section.

### Option 2: Create New FOMO-Specific Images

#### Cold Audience Images (KT25--FOMO--Cold--500PerDag)
1. **Calculator/Money Visual**
   - Show a calculator displaying "€500 x 30 = €15,000"
   - Red background with white numbers
   - Add clock icon showing time passing

2. **Graph Showing Loss**
   - Downward trend line showing productivity loss
   - Red area under curve labeled "€500/dag verlies"
   - Professional business setting

3. **Split Screen Visual**
   - Left: Empty desk (vacancy)
   - Right: Money burning/disappearing
   - Text overlay: "Elke dag = €500 weg"

#### Warm Audience Images (KT25--FOMO--Warm--Urgency)
1. **Countdown Timer Visual**
   - Large "48 UUR" countdown
   - Orange/red urgent colors
   - "Bespaar €15.000" prominently displayed

2. **Before/After Comparison**
   - Before: Stressed team, red numbers
   - After: Happy team, green checkmarks
   - "Start NU" call-to-action

3. **Calendar Visual**
   - Current month with days crossed off
   - Each day shows "-€500"
   - Today highlighted with "LAATSTE KANS"

#### Hot Audience Images (KT25--FOMO--Hot--LastChance)
1. **Limited Time Offer Badge**
   - "VANDAAG ALLEEN" in bold
   - Clock showing 23:59
   - "€2.500 VOORDEEL" highlighted

2. **Urgency Meter**
   - Gauge showing "almost full"
   - "Nog 3 plekken beschikbaar"
   - Red/orange warning colors

3. **Bonus Stack Visual**
   - Show all bonuses being offered
   - Strike-through on regular price
   - "GRATIS vandaag alleen"

## 📸 Image Specifications

### Technical Requirements:
- **Format**: JPG or PNG
- **Size**: 1200 x 628px (1.91:1 ratio)
- **File size**: Under 30MB
- **Text**: Less than 20% of image area

### Design Principles:
1. **High Contrast**: Use red/orange for urgency
2. **Clear Numbers**: Make €500/day loss prominent
3. **Simple**: One clear message per image
4. **Professional**: Match your brand style
5. **Mobile-First**: Test on small screens

## 🎨 Quick Creation Tools

### Canva Templates:
Create these templates in Canva for quick editing:
1. Money Loss Calculator Template
2. Countdown Timer Template  
3. Before/After Split Template
4. Limited Offer Badge Template

### Color Palette:
```css
/* FOMO Campaign Colors */
--fomo-urgent-red: #DC2626;
--fomo-warning-orange: #EA580C;
--fomo-loss-dark: #1F2937;
--fomo-save-green: #059669;
--fomo-background: #FEF2F2;
```

## 🔧 Adding Images to the Script

Update the creative creation function in the main script:

```javascript
// In createAdCreative function, add:
object_story_spec: {
  page_id: PAGE_ID,
  link_data: {
    link: `https://kandidatentekort.nl?${utmParams}`,
    message: adCopy.primary_text,
    name: adCopy.headline,
    description: adCopy.link_description,
    call_to_action: {
      type: 'LEARN_MORE'
    },
    // Add your image here:
    picture: 'https://your-domain.com/fomo-images/cold-audience-1.jpg'
    // OR use uploaded image hash:
    // image_hash: 'your_uploaded_image_hash'
  }
}
```

## 📊 A/B Testing Images

Test these variations:
1. **Numbers vs Emotions**: €500 calculator vs stressed team
2. **Red vs Orange**: Urgency color testing
3. **Text overlay vs Clean**: Message in image vs in ad copy
4. **People vs Graphics**: Human faces vs infographics

## 💡 Pro Tips

1. **Create Image Sets**: 3 images per campaign for testing
2. **Use Dynamic Creative**: Let Facebook optimize image/copy combinations
3. **Track Performance**: Monitor CTR by image after 48 hours
4. **Refresh Weekly**: Swap underperforming images to prevent ad fatigue

## 🚀 Quick Start

1. Choose 3 images per campaign from existing library OR
2. Create new FOMO-specific images using the templates above
3. Upload to Facebook Ads Manager
4. Get image hashes or URLs
5. Add to the script before running

Remember: The €500/day message should be visually reinforced in your images for maximum FOMO impact!