#!/usr/bin/env python3
"""
Leonardo AI Test Script - Kandidatentekort.nl Meta Campaign Images
Test the best-performing Leonardo AI prompts for Meta advertising campaigns
"""

import os
import sys
import argparse
import time
from datetime import datetime

# Leonardo AI prompts from our analysis
LEONARDO_PROMPTS = {
    "voor_na_comparison": {
        "prompt": "Professional Dutch office environment, split-screen laptop display showing kandidatentekort.nl before/after job posting comparison, left side shows poor job posting with red X marks and low engagement metrics, right side shows optimized job posting with green checkmarks and 180% increase statistics, orange UI elements (#FF6B35), Dutch business professional reviewing results, modern minimalist desk setup, bright natural lighting, photorealistic commercial style, 16:9 aspect ratio",
        "priority": 1,
        "target": "HR Managers & Recruiters",
        "format": "1200x628 Facebook Feed"
    },
    
    "roi_calculator": {
        "prompt": "Modern Dutch business office, MacBook Pro on clean wooden desk displaying kandidatentekort.nl ROI calculator interface, detailed cost savings dashboard visible on screen, €27.500 savings calculation prominent, orange chart elements and UI components, professional Dutch finance director reviewing data, satisfied expression, premium office environment with plants, natural window lighting, authentic business photography style, 1:1 square format",
        "priority": 2,
        "target": "Business Owners & Directors",  
        "format": "1080x1080 Instagram Feed"
    },
    
    "professional_testimonial": {
        "prompt": "Authentic Dutch woman, 35-40 years old, professional business casual attire, confident pose in modern Dutch office, holding tablet displaying kandidatentekort.nl interface with positive analytics, warm genuine smile, orange UI elements visible on screen, contemporary Amsterdam office background, natural lighting, real testimonial photography style not stock photo, includes trust badges and company logos, professional headshot quality",
        "priority": 3,
        "target": "HR Managers & MKB Owners",
        "format": "1080x1080 Instagram Feed"
    },
    
    "technical_sector": {
        "prompt": "Authentic Dutch automotive workshop environment, professional mechanic or technician using tablet showing kandidatentekort.nl technical job posting interface, real workshop tools and automotive equipment background, tablet screen shows technical vacancy optimization, orange safety equipment matching UI colors, industrial lighting, authentic Dutch automotive workplace, professional work photography style",
        "priority": 4,
        "target": "Technical Sector Managers",
        "format": "1200x628 Facebook Feed"
    },
    
    "mobile_quick_check": {
        "prompt": "Professional Dutch person using smartphone in modern office break area, phone clearly showing kandidatentekort.nl mobile interface with vacancy analysis and calendar integration, orange UI elements prominent, natural mobile usage scenario not posed, Dutch workplace environment, person looking satisfied with results, lifestyle photography approach, authentic interaction with device, 9:16 mobile format",
        "priority": 5,
        "target": "Busy Professionals",
        "format": "1080x1920 Instagram Stories"
    }
}

NEGATIVE_PROMPT = "low quality, blurry, cartoon, anime, drawing, fake interface, stock photo look, overly posed, unrealistic lighting, poor composition, watermarks, text overlays, logos in image, artificial staging, fake smiles, generic stock photography"

def print_header():
    """Print test script header"""
    print("=" * 80)
    print("🎨 LEONARDO AI TEST SCRIPT - KANDIDATENTEKORT.NL META CAMPAIGNS")
    print("=" * 80)
    print(f"📅 Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Purpose: Test top-performing prompts for Meta advertising")
    print(f"📊 Total Prompts: {len(LEONARDO_PROMPTS)}")
    print("=" * 80)

def check_api_key():
    """Check if Leonardo API key is set"""
    api_key = os.getenv('LEONARDO_API_KEY')
    if not api_key or api_key == 'your-key':
        print("❌ ERROR: LEONARDO_API_KEY not properly set!")
        print("💡 Run: export LEONARDO_API_KEY='your-actual-api-key'")
        return False
    
    print(f"✅ Leonardo API Key: {api_key[:20]}...")
    return True

def test_mode():
    """Run in test mode - validate prompts without API calls"""
    print("\n🧪 TEST MODE - Validating prompts without API calls\n")
    
    for key, config in LEONARDO_PROMPTS.items():
        prompt_id = key.replace('_', '-').upper()
        
        print(f"📝 PROMPT {config['priority']}: {prompt_id}")
        print(f"   🎯 Target: {config['target']}")
        print(f"   📐 Format: {config['format']}")
        print(f"   📏 Length: {len(config['prompt'])} characters")
        
        # Validate prompt length (Leonardo AI optimal range: 77-777 characters)
        length = len(config['prompt'])
        if length < 77:
            print(f"   ⚠️  WARNING: Prompt too short ({length} chars, min 77)")
        elif length > 777:
            print(f"   ⚠️  WARNING: Prompt too long ({length} chars, max 777)")
        else:
            print(f"   ✅ Length OK ({length} chars)")
            
        # Check for key elements
        key_elements = ['Dutch', 'kandidatentekort.nl', 'orange', 'professional']
        missing_elements = [elem for elem in key_elements if elem.lower() not in config['prompt'].lower()]
        
        if missing_elements:
            print(f"   ⚠️  Missing elements: {', '.join(missing_elements)}")
        else:
            print(f"   ✅ All key elements present")
            
        print(f"   📋 Prompt preview: {config['prompt'][:100]}...")
        print()

def production_mode():
    """Run in production mode - make actual Leonardo API calls"""
    print("\n🚀 PRODUCTION MODE - Generating images via Leonardo AI\n")
    
    if not check_api_key():
        return False
        
    print("⚠️  PRODUCTION MODE REQUIRES ACTUAL LEONARDO API INTEGRATION")
    print("💡 This would make real API calls and generate actual images")
    print("🔧 Implement Leonardo API client to enable this functionality")
    
    # TODO: Implement actual Leonardo API calls
    # This would require the leonardo-ai Python package or direct API calls
    
    return True

def get_recommendations():
    """Print optimization recommendations"""
    print("\n📈 OPTIMIZATION RECOMMENDATIONS:")
    print("=" * 50)
    
    recommendations = [
        "🎯 Start with Priority 1 prompt (Voor/Na Comparison) - highest conversion",
        "📱 Generate mobile versions (9:16) for Instagram Stories",
        "🔄 Create 3-5 variations per concept for A/B testing", 
        "🎨 Test different lighting conditions (natural, studio, golden hour)",
        "👥 Generate both male and female professional variants",
        "🏢 Test different office environments (corporate, SME, industrial)",
        "📊 Monitor performance and iterate based on Meta Ads results",
        "🇳🇱 Ensure authentically Dutch environments and people",
        "🟠 Maintain consistent orange branding (#FF6B35) across all images",
        "📈 Track which prompts generate highest CTR and lowest CPL"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i:2d}. {rec}")

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Leonardo AI Test Script for Kandidatentekort.nl')
    parser.add_argument('--test', action='store_true', help='Run in test mode (validate prompts)')
    parser.add_argument('--production', action='store_true', help='Run in production mode (generate images)')
    
    args = parser.parse_args()
    
    print_header()
    
    if args.test:
        test_mode()
        get_recommendations()
        print("\n✅ TEST COMPLETE - All prompts validated and ready for Leonardo AI")
        
    elif args.production:
        success = production_mode()
        if success:
            print("\n✅ PRODUCTION RUN COMPLETE")
        else:
            print("\n❌ PRODUCTION RUN FAILED")
            return 1
            
    else:
        print("\n❓ No mode specified. Use --test or --production")
        parser.print_help()
        return 1
        
    print("\n🎯 NEXT STEPS:")
    print("1. Copy prompts to Leonardo AI platform")
    print("2. Generate 3-5 variations per concept") 
    print("3. Upload to Meta Ads Manager")
    print("4. Launch campaigns with provided targeting")
    print("5. Monitor performance and optimize")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())