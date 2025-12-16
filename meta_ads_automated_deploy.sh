#!/bin/bash

# 🎨 META ADS - AUTOMATED CANVA TO META DEPLOYMENT
# Automatically downloads from Canva and uploads to Meta Ads with ad creation

TOKEN="EAAYqzG39fnoBQA2CJkoHNj3H9KiuXLkJZBUvozSQqQ9ptQvpkkC9zEq25c5poq3rDwrM9yahiwLo4LEPUHtGxUKxoh3Rl5BKpahtgbb4DSsdPLE73KQNcHaMzabeuZBt58gm6zbPRP1pfUZC9O4DGgheWqTFNMCvxCbjTkqtLlT3iMTCSwDS2jzEgDqT0oCTLHdTAHa25wZAglDNDLbHfNxjLYHpodubLd4ZBCfudpQL1eVx9ZBD3R0BthR2ayUMZBLohz3IPtSRblaoloyGZAw4WRZBHOEcx"
AD_ACCOUNT="act_1236576254450117"
CAMPAIGN_ID="120240987303750536"
PAGE_ID="3802862666677831"

echo "🚀 META ADS AUTOMATED DEPLOYMENT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📥 Downloading 5 Canva designs..."
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Download all 5 designs from Canva export URLs
# These URLs are from Canva export jobs (valid for ~2 hours)

echo "  1/5 Split Screen..."
curl -sL "https://export-download.canva.com/37LpM/DAG7bB37LpM/-1/0/0001-7402153658655436902.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20251214%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251214T235011Z&X-Amz-Expires=7757&X-Amz-Signature=196fbce32a21a5b172125ce74833259747e218276422af4a7cef709fdeac5d05&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2015%20Dec%202025%2001%3A59%3A28%20GMT" -o split_screen.png

echo "  2/5 Carousel..."
curl -sL "https://export-download.canva.com/xoh7k/DAG6NKxoh7k/-1/0/0001-7040739785745363585.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20251214%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251214T175620Z&X-Amz-Expires=29681&X-Amz-Signature=9a1904b339d491c31e0105663c23a0a236144e0aabf33b968d2b882549a26776&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2015%20Dec%202025%2002%3A11%3A01%20GMT" -o carousel.png

echo "  3/5 ROI Calculator..."  
curl -sL "https://export-download.canva.com/I2s4Y/DAG7bBI2s4Y/-1/0/0001-6786286408638518913.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20251214%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251214T021208Z&X-Amz-Expires=87857&X-Amz-Signature=97b03185869f084c7970ac90416dd764acdeb91d5e62bf5873cb807afce9c062&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2015%20Dec%202025%2002%3A36%3A25%20GMT" -o roi_calculator.png

echo "  4/5 Stories..."
curl -sL "https://export-download.canva.com/gZqY0/DAG7bLgZqY0/-1/0/0001-6918016695975390166.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20251215%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251215T002328Z&X-Amz-Expires=6542&X-Amz-Signature=16197a550ff8f7ae28b854da92ca5b45e3d8049e31cebcf5af87f4519c60d7d5&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2015%20Dec%202025%2002%3A12%3A30%20GMT" -o stories.png

echo "  5/5 Retargeting..."
curl -sL "https://export-download.canva.com/d2SOI/DAG7bNd2SOI/-1/0/0001-3613500471599697450.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20251214%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20251214T220128Z&X-Amz-Expires=15310&X-Amz-Signature=2afe4db6b7280edb0f24b207ff9a9ce04a4a85807aa151637cc105df001e57e7&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Mon%2C%2015%20Dec%202025%2002%3A16%3A38%20GMT" -o retargeting.png

echo ""
echo "✅ Downloads complete"
echo ""
echo "📤 Uploading to Meta Ad Account..."
echo ""

# Upload images and store hashes
declare -A IMAGE_HASHES

upload_to_meta() {
    local file=$1
    local name=$2
    
    if [ ! -f "$file" ]; then
        echo "  ❌ $name: File not found"
        return 1
    fi
    
    echo "  📤 $name..."
    
    RESPONSE=$(curl -s -X POST \
        "https://graph.facebook.com/v18.0/$AD_ACCOUNT/adimages" \
        -F "access_token=$TOKEN" \
        -F "bytes=@$file")
    
    HASH=$(echo "$RESPONSE" | grep -o '"hash":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$HASH" ]; then
        IMAGE_HASHES[$name]=$HASH
        echo "    ✅ Hash: $HASH"
        return 0
    else
        echo "    ❌ Failed: $(echo "$RESPONSE" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)"
        return 1
    fi
}

upload_to_meta "split_screen.png" "split_screen"
upload_to_meta "carousel.png" "carousel"
upload_to_meta "roi_calculator.png" "roi_calculator"
upload_to_meta "stories.png" "stories"
upload_to_meta "retargeting.png" "retargeting"

echo ""
echo "✅ Uploaded ${#IMAGE_HASHES[@]}/5 images to Meta"
echo ""

# Get all ad sets
echo "📋 Getting ad sets from campaign..."
echo ""

ADSETS=$(curl -s -G \
    "https://graph.facebook.com/v18.0/$CAMPAIGN_ID/adsets" \
    -d "access_token=$TOKEN" \
    -d "fields=id,name" \
    -d "limit=20")

echo "$ADSETS" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | nl
echo ""

# Create ads for each ad set
echo "🎯 Creating ads for each ad set..."
echo ""

SUCCESSFUL=0
FAILED=0

# City to image mapping (based on tier)
declare -A CITY_IMAGE
CITY_IMAGE["Utrecht"]="split_screen"
CITY_IMAGE["Eindhoven"]="split_screen"
CITY_IMAGE["Arnhem"]="split_screen"
CITY_IMAGE["Nijmegen"]="carousel"
CITY_IMAGE["Apeldoorn"]="carousel"
CITY_IMAGE["Enschede"]="carousel"
CITY_IMAGE["Deventer"]="roi_calculator"
CITY_IMAGE["Zwolle"]="roi_calculator"
CITY_IMAGE["Amersfoort"]="roi_calculator"
CITY_IMAGE["Hengelo"]="stories"
CITY_IMAGE["Almelo"]="stories"
CITY_IMAGE["Hardenberg"]="retargeting"
CITY_IMAGE["Oss"]="retargeting"

while IFS= read -r line; do
    ADSET_ID=$(echo "$line" | grep -o '"id":"[0-9]*"' | cut -d'"' -f4)
    ADSET_NAME=$(echo "$line" | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
    
    if [ -z "$ADSET_ID" ]; then
        continue
    fi
    
    # Extract city name
    CITY=$(echo "$ADSET_NAME" | cut -d' ' -f1)
    CITY_LOWER=$(echo "$CITY" | tr '[:upper:]' '[:lower:]')
    
    # Get appropriate image for this city
    IMAGE_NAME="${CITY_IMAGE[$CITY]}"
    IMAGE_HASH="${IMAGE_HASHES[$IMAGE_NAME]}"
    
    if [ -z "$IMAGE_HASH" ]; then
        echo "  ❌ $CITY: No image hash available"
        ((FAILED++))
        continue
    fi
    
    echo "  📍 $CITY → $IMAGE_NAME"
    
    # Create creative
    CREATIVE=$(curl -s -X POST \
        "https://graph.facebook.com/v18.0/$AD_ACCOUNT/adcreatives" \
        -d "access_token=$TOKEN" \
        -d "name=$CITY - Gratis Vacature Check" \
        -d "object_story_spec={\"page_id\":\"$PAGE_ID\",\"link_data\":{\"image_hash\":\"$IMAGE_HASH\",\"link\":\"https://kandidatentekort.nl?utm_source=meta&utm_medium=paid_social&utm_campaign=expert_q1_2025&utm_content=$CITY_LOWER\",\"message\":\"Vacature in $CITY moeilijk te vervullen?\n\n✅ 10+ jaar technisch recruitment\n✅ 500+ succesvolle plaatsingen\n✅ Specialist in Oil & Gas, Productie, Automation\n\nOntvang gratis vacature-analyse voor $CITY regio.\nKlik voor gratis check →\",\"name\":\"Gratis Vacature Check\",\"description\":\"10+ jaar | 500+ plaatsingen\",\"call_to_action\":{\"type\":\"LEARN_MORE\"}}}")
    
    CREATIVE_ID=$(echo "$CREATIVE" | grep -o '"id":"[0-9]*"' | head -1 | cut -d'"' -f4)
    
    if [ -z "$CREATIVE_ID" ]; then
        echo "    ❌ Creative failed"
        ((FAILED++))
        continue
    fi
    
    # Create ad
    AD=$(curl -s -X POST \
        "https://graph.facebook.com/v18.0/$AD_ACCOUNT/ads" \
        -d "access_token=$TOKEN" \
        -d "name=$CITY - Gratis Vacature Check" \
        -d "adset_id=$ADSET_ID" \
        -d "creative={\"creative_id\":\"$CREATIVE_ID\"}" \
        -d "status=PAUSED")
    
    AD_ID=$(echo "$AD" | grep -o '"id":"[0-9]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$AD_ID" ]; then
        echo "    ✅ Ad created: $AD_ID"
        ((SUCCESSFUL++))
    else
        echo "    ❌ Ad failed: $(echo "$AD" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)"
        ((FAILED++))
    fi
    
    sleep 0.5
    
done < <(echo "$ADSETS" | grep -o '{[^}]*}')

# Cleanup
cd ~
rm -rf "$TEMP_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "📊 Final Results:"
echo "  ✅ Ads created: $SUCCESSFUL"
echo "  ❌ Failed: $FAILED"
echo "  📸 Images used: ${#IMAGE_HASHES[@]}/5"
echo "  💰 Total budget: €47/dag (€1,410/mnd)"
echo ""
echo "🔗 View Campaign:"
echo "  https://business.facebook.com/adsmanager/manage/campaigns?act=1236576254450117&selected_campaign_ids=120240987303750536"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1️⃣  Review all ads in Ads Manager"
echo "2️⃣  Check image quality and copy"
echo "3️⃣  Test kandidatentekort.nl landing page"
echo "4️⃣  Activate campaign (PAUSED → ACTIVE)"
echo "5️⃣  Monitor CPL for first 24-48 hours"
echo ""
echo "🎯 Performance Targets:"
echo "  • CPL: €20-25"
echo "  • CTR: 2-3%"
echo "  • Leads/month: 56-70"
echo "  • Revenue/month: €12,000-22,500"
echo ""
echo "✅ Campaign ready to launch! 🚀"
echo ""
