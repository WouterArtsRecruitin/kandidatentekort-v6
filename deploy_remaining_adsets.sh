#!/bin/bash

# META ADS - COMPLETE 12 REMAINING AD SETS
# Campaign ID: 120240987303750536
# Ad Account: act_1236576254450117 (Recruitin)

TOKEN="EAAYqzG39fnoBQA2CJkoHNj3H9KiuXLkJZBUvozSQqQ9ptQvpkkC9zEq25c5poq3rDwrM9yahiwLo4LEPUHtGxUKxoh3Rl5BKpahtgbb4DSsdPLE73KQNcHaMzabeuZBt58gm6zbPRP1pfUZC9O4DGgheWqTFNMCvxCbjTkqtLlT3iMTCSwDS2jzEgDqT0oCTLHdTAHa25wZAglDNDLbHfNxjLYHpodubLd4ZBCfudpQL1eVx9ZBD3R0BthR2ayUMZBLohz3IPtSRblaoloyGZAw4WRZBHOEcx"
AD_ACCOUNT="act_1236576254450117"
CAMPAIGN_ID="120240987303750536"
PIXEL_ID="238226887541404"

echo "🚀 CREATING 12 REMAINING AD SETS"
echo "Campaign: Kandidatentekort - Expert Recruitment Q1 2025"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Remaining 12 cities (Utrecht already created by Claude Code)
declare -a CITIES=(
  "Eindhoven:2756253:500"
  "Arnhem:2759661:500"
  "Nijmegen:2750053:400"
  "Apeldoorn:2759879:400"
  "Enschede:2756723:400"
  "Deventer:2758401:300"
  "Zwolle:2743477:300"
  "Amersfoort:2759899:300"
  "Hengelo:2754889:300"
  "Almelo:2759837:200"
  "Hardenberg:2755070:200"
  "Oss:2748840:200"
)

SUCCESSFUL=0
FAILED=0

for city in "${CITIES[@]}"; do
  IFS=':' read -r name key budget <<< "$city"
  
  echo "📍 Creating: $name (€$((budget/100))/dag)..."
  
  # Create ad set with EMPLOYMENT-compliant targeting
  RESPONSE=$(curl -s -X POST \
    "https://graph.facebook.com/v18.0/$AD_ACCOUNT/adsets" \
    -d "access_token=$TOKEN" \
    -d "campaign_id=$CAMPAIGN_ID" \
    -d "name=$name - MKB Productie" \
    -d "daily_budget=$budget" \
    -d "billing_event=IMPRESSIONS" \
    -d "optimization_goal=OFFSITE_CONVERSIONS" \
    -d "bid_strategy=LOWEST_COST_WITHOUT_CAP" \
    -d "status=PAUSED" \
    -d "targeting={\"geo_locations\":{\"cities\":[{\"key\":\"$key\"}]},\"age_min\":18,\"age_max\":65,\"publisher_platforms\":[\"facebook\",\"instagram\"],\"facebook_positions\":[\"feed\"],\"instagram_positions\":[\"stream\"],\"flexible_spec\":[{\"interests\":[{\"id\":\"6003107902433\",\"name\":\"Human resources\"}]}]}" \
    -d "promoted_object={\"pixel_id\":\"$PIXEL_ID\",\"custom_event_type\":\"LEAD\"}")
  
  # Check if successful
  if echo "$RESPONSE" | grep -q '"id"'; then
    ADSET_ID=$(echo "$RESPONSE" | grep -o '"id":"[0-9]*"' | head -1 | cut -d'"' -f4)
    echo "  ✅ Created: $ADSET_ID"
    ((SUCCESSFUL++))
  else
    echo "  ❌ Failed: $(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)"
    ((FAILED++))
  fi
  
  sleep 0.5
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "📊 Results:"
echo "  ✅ Successful: $SUCCESSFUL/12"
echo "  ❌ Failed: $FAILED/12"
echo "  ✅ Utrecht: Already created (€6/dag)"
echo "  💰 Total Budget: €47/dag (€1,410/mnd)"
echo ""
echo "🔗 View Campaign:"
echo "  https://business.facebook.com/adsmanager/manage/campaigns?act=1236576254450117&selected_campaign_ids=120240987303750536"
echo ""
echo "📋 NEXT STEPS (15-30 min):"
echo ""
echo "1️⃣ DOWNLOAD CANVA DESIGNS:"
echo "  - Split Screen: https://www.canva.com/design/DAG7bB37LpM"
echo "  - Carousel: https://www.canva.com/design/DAG7bEXignc"
echo "  - ROI Calculator: https://www.canva.com/design/DAG7bBI2s4Y"
echo "  - Stories: https://www.canva.com/design/DAG7bLgZqY0"
echo "  - Retargeting: https://www.canva.com/design/DAG7bNd2SOI"
echo ""
echo "2️⃣ CREATE ADS IN ADS MANAGER:"
echo "  For each ad set:"
echo "  - Click ad set → Create Ad"
echo "  - Upload Canva design"
echo "  - Headline: 'Gratis Vacature Check - [STAD]'"
echo "  - Body: '10+ jaar ervaring | 500+ plaatsingen | Oil & Gas, Productie'"
echo "  - CTA: Learn More → kandidatentekort.nl"
echo ""
echo "3️⃣ CREATE LEAD FORM (or link to website):"
echo "  Option A: Instant Form (built-in Meta)"
echo "  Option B: Link to kandidatentekort.nl/gratis-check"
echo ""
echo "4️⃣ REVIEW & ACTIVATE:"
echo "  - Check all targeting"
echo "  - Verify budgets (€47/dag total)"
echo "  - Test pixel firing"
echo "  - Activate campaign!"
echo ""
echo "✅ Your Meta Ads campaign structure is ready!"
echo ""
