const axios = require('axios');

// Facebook Marketing API configuration
const ACCESS_TOKEN = 'EAAYqzG39fnoBQI36ltDvwpuGHU9TJpa6DSe4ZCr5Twrv6nHGwdOQnOVEtXez6Md7lYFTdsPq3ZA9IWjAU49eXcGmtDrA6GdiicwT5faw4vHQqWcg5q2Eof5AN3naiBXBueSE7RBbMIrdxvYjpu7t0TOahFDDkruV1DTUkTrsv5H6oZCkqn1F2UPAsZB0yQ83sVpe2Y2unEFoapJRSJssZCfpKuGb0NK5bT27VdS22rYmnMZAGgbCIKqer8keYj4t9stUqDh1tpObdOZBoIWFc2eZCCvVzrZC3';
const AD_ACCOUNT_ID = 'act_1234567890'; // Replace with your actual Ad Account ID
const PAGE_ID = 'YOUR_PAGE_ID'; // Replace with your Facebook Page ID
const PIXEL_ID = 'YOUR_PIXEL_ID'; // Replace with your Facebook Pixel ID

// FOMO Ad Copy Templates
const fomoAdCopy = {
  cold: {
    primary_text: [
      "⚠️ Bedrijven verliezen €500/dag door vacatures die te lang openstaan.\n\nDe kosten stapelen zich op:\n• Week 1: €3.500 verlies\n• Maand 1: €15.000 verlies\n• Kwartaal 1: €45.000 verlies\n\nElke dag uitstel = €500 minder omzet.",
      "🚨 Wist je dat je €500 per dag verliest met elke vacature?\n\nReken maar uit:\n→ 5 dagen = €2.500 weg\n→ 30 dagen = €15.000 weg\n→ 90 dagen = €45.000 weg\n\nStop het bloeden. Start vandaag.",
      "💸 €500 verdampt. Elke. Dag. Opnieuw.\n\nZolang die vacature openstaat:\n✗ Productiviteit daalt\n✗ Team raakt overbelast\n✗ Klanten wachten langer\n\nDe oplossing? Vul die vacature. NU."
    ],
    headline: [
      "Stop Het €500/Dag Verlies",
      "Vacatures Kosten €500 Per Dag",
      "Elke Dag = €500 Verlies"
    ],
    link_description: "Ontdek waarom vacatures je €500/dag kosten"
  },
  warm: {
    primary_text: [
      "⏰ LAATSTE KANS deze week!\n\nBedrijven die NU actie ondernemen besparen €15.000/maand aan vacaturekosten.\n\nWacht je tot volgende week?\nDan ben je weer €3.500 kwijt.\n\nDe klok tikt. Wat doe je?",
      "🔥 48 UUR om €15.000 te besparen\n\nElke maand dat je vacature openstaat kost €15.000.\n\nBedrijven die deze week starten:\n✓ Vacature binnen 30 dagen gevuld\n✓ €15.000 bespaard\n✓ Team weer op volle kracht\n\nJij ook?",
      "📊 87% vult vacatures binnen 30 dagen\n(De rest verliest €45.000 per kwartaal)\n\nWil je bij die 87% horen?\nDan moet je NU actie ondernemen.\n\nMorgen is weer €500 weg."
    ],
    headline: [
      "48 Uur: Bespaar €15.000",
      "NU Actie = €15k Bespaard", 
      "Laatste Kans Deze Week"
    ],
    link_description: "Start vandaag en bespaar direct"
  },
  hot: {
    primary_text: [
      "🚨 VANDAAG je laatste kans!\n\n✓ Gratis Arbeidsmarkt Analyse (t.w.v. €1.500)\n✓ Directe toegang tot ons netwerk\n✓ Gegarandeerd binnen 30 dagen gevuld\n\nDeze aanbieding vervalt om MIDDERNACHT.\n\nMorgen betaal je de volle prijs.",
      "⚡ NOG 12 UUR!\n\nSpeciale aanbieding:\n• Gratis intake gesprek\n• Gratis marktanalyse\n• Geen opstartkosten\n\nTotale waarde: €2.500\nVandaag: €0\n\nMorgen weer €500/dag verlies.",
      "🔴 STOPT VANAVOND 23:59\n\nLaatste kans om €45.000 te besparen dit kwartaal.\n\n→ Start vandaag = bespaar direct\n→ Wacht tot morgen = €500 weg\n\nKies verstandig. De tijd dringt."
    ],
    headline: [
      "⏰ Laatste 12 Uur",
      "VANDAAG: €2.500 Voordeel",
      "Stopt Om Middernacht"
    ],
    link_description: "Claim je plek voordat het te laat is"
  }
};

// Campaign configurations
const campaignConfigs = [
  {
    name: 'KT25--FOMO--Cold--500PerDag',
    objective: 'OUTCOME_TRAFFIC',
    status: 'PAUSED',
    daily_budget: 6000, // €60 in cents
    bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
    optimization_goal: 'LINK_CLICKS',
    targeting: {
      geo_locations: { countries: ['NL'] },
      age_min: 25,
      age_max: 55,
      targeting_optimization: 'none',
      publisher_platforms: ['facebook', 'instagram'],
      facebook_positions: ['feed', 'instant_article', 'marketplace'],
      instagram_positions: ['stream', 'story', 'reels']
    },
    adType: 'cold'
  },
  {
    name: 'KT25--FOMO--Warm--Urgency',
    objective: 'OUTCOME_TRAFFIC',
    status: 'PAUSED',
    daily_budget: 6000,
    bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
    optimization_goal: 'LINK_CLICKS',
    targeting: {
      geo_locations: { countries: ['NL'] },
      age_min: 25,
      age_max: 55,
      targeting_optimization: 'none',
      publisher_platforms: ['facebook', 'instagram'],
      facebook_positions: ['feed', 'instant_article', 'marketplace'],
      instagram_positions: ['stream', 'story', 'reels'],
      custom_audiences: [
        { id: 'YOUR_WARM_AUDIENCE_ID' } // Replace with actual warm audience ID
      ]
    },
    adType: 'warm'
  },
  {
    name: 'KT25--FOMO--Hot--LastChance',
    objective: 'OUTCOME_TRAFFIC',
    status: 'PAUSED',
    daily_budget: 6000,
    bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
    optimization_goal: 'CONVERSIONS',
    targeting: {
      geo_locations: { countries: ['NL'] },
      age_min: 25,
      age_max: 55,
      targeting_optimization: 'none',
      publisher_platforms: ['facebook', 'instagram'],
      facebook_positions: ['feed', 'instant_article'],
      instagram_positions: ['stream', 'reels'],
      custom_audiences: [
        { id: 'YOUR_HOT_AUDIENCE_ID' } // Replace with actual hot audience ID
      ]
    },
    adType: 'hot'
  }
];

// Helper function to create campaign
async function createCampaign(config) {
  try {
    console.log(`Creating campaign: ${config.name}`);
    
    const campaignData = {
      name: config.name,
      objective: config.objective,
      status: config.status,
      special_ad_categories: ['EMPLOYMENT'],
      daily_budget: config.daily_budget,
      bid_strategy: config.bid_strategy,
      access_token: ACCESS_TOKEN
    };

    const response = await axios.post(
      `https://graph.facebook.com/v18.0/${AD_ACCOUNT_ID}/campaigns`,
      campaignData
    );

    return response.data.id;
  } catch (error) {
    console.error(`Error creating campaign ${config.name}:`, error.response?.data || error);
    throw error;
  }
}

// Helper function to create ad set
async function createAdSet(campaignId, config) {
  try {
    console.log(`Creating ad set for campaign: ${config.name}`);
    
    const adSetData = {
      name: `${config.name}--AdSet`,
      campaign_id: campaignId,
      daily_budget: config.daily_budget,
      optimization_goal: config.optimization_goal,
      billing_event: 'IMPRESSIONS',
      bid_strategy: config.bid_strategy,
      targeting: config.targeting,
      status: config.status,
      promoted_object: {
        pixel_id: PIXEL_ID,
        custom_event_type: 'LEAD'
      },
      access_token: ACCESS_TOKEN
    };

    const response = await axios.post(
      `https://graph.facebook.com/v18.0/${AD_ACCOUNT_ID}/adsets`,
      adSetData
    );

    return response.data.id;
  } catch (error) {
    console.error(`Error creating ad set for ${config.name}:`, error.response?.data || error);
    throw error;
  }
}

// Helper function to create ad creative
async function createAdCreative(adCopy, utmParams, adIndex) {
  try {
    const creativeData = {
      name: `FOMO Creative ${adIndex + 1}`,
      object_story_spec: {
        page_id: PAGE_ID,
        link_data: {
          link: `https://kandidatentekort.nl?${utmParams}`,
          message: adCopy.primary_text,
          name: adCopy.headline,
          description: adCopy.link_description,
          call_to_action: {
            type: 'LEARN_MORE'
          }
        }
      },
      degrees_of_freedom_spec: {
        creative_features_spec: {
          standard_enhancements: {
            enroll_status: 'OPT_OUT'
          }
        }
      },
      access_token: ACCESS_TOKEN
    };

    const response = await axios.post(
      `https://graph.facebook.com/v18.0/${AD_ACCOUNT_ID}/adcreatives`,
      creativeData
    );

    return response.data.id;
  } catch (error) {
    console.error('Error creating ad creative:', error.response?.data || error);
    throw error;
  }
}

// Helper function to create ads
async function createAds(adSetId, config, campaignType) {
  try {
    console.log(`Creating ads for ad set: ${config.name}`);
    
    const adCopyVariants = fomoAdCopy[config.adType];
    const ads = [];

    for (let i = 0; i < 3; i++) {
      // Create UTM parameters
      const utmParams = new URLSearchParams({
        utm_source: 'facebook',
        utm_medium: 'paid',
        utm_campaign: `fomo_${campaignType}_${config.adType}`,
        utm_content: `variant_${i + 1}`,
        utm_term: config.adType
      }).toString();

      // Create ad copy variant
      const adCopy = {
        primary_text: adCopyVariants.primary_text[i],
        headline: adCopyVariants.headline[i],
        link_description: adCopyVariants.link_description
      };

      // Create creative
      const creativeId = await createAdCreative(adCopy, utmParams, i);

      // Create ad
      const adData = {
        name: `${config.name}--Ad${i + 1}`,
        adset_id: adSetId,
        creative: { creative_id: creativeId },
        status: config.status,
        tracking_specs: [
          {
            action.type: ['link_click'],
            page: [PAGE_ID]
          }
        ],
        access_token: ACCESS_TOKEN
      };

      const response = await axios.post(
        `https://graph.facebook.com/v18.0/${AD_ACCOUNT_ID}/ads`,
        adData
      );

      ads.push(response.data.id);
    }

    return ads;
  } catch (error) {
    console.error(`Error creating ads for ${config.name}:`, error.response?.data || error);
    throw error;
  }
}

// Main execution function
async function createFOMOCampaigns() {
  console.log('🚀 Starting FOMO Campaign Creation...\n');
  console.log('⚡ Creating 3 NEW campaigns with €500/day loss messaging\n');

  const results = {
    campaigns: [],
    errors: [],
    summary: {
      totalBudget: 180,
      campaignsCreated: 0,
      adsCreated: 0
    }
  };

  for (const config of campaignConfigs) {
    try {
      console.log(`\n📊 Processing: ${config.name}`);
      console.log(`   Budget: €${config.daily_budget / 100}/day`);
      console.log(`   Type: ${config.adType} audience`);
      console.log(`   Status: ${config.status}\n`);

      // Create campaign
      const campaignId = await createCampaign(config);
      console.log(`   ✅ Campaign created: ${campaignId}`);

      // Create ad set
      const adSetId = await createAdSet(campaignId, config);
      console.log(`   ✅ Ad set created: ${adSetId}`);

      // Create ads (3 variants per campaign)
      const adIds = await createAds(adSetId, config, 'kt25');
      console.log(`   ✅ ${adIds.length} ads created`);

      results.campaigns.push({
        name: config.name,
        campaignId,
        adSetId,
        adIds,
        dailyBudget: config.daily_budget / 100,
        status: config.status
      });

      results.summary.campaignsCreated++;
      results.summary.adsCreated += adIds.length;

    } catch (error) {
      console.error(`\n❌ Failed to create ${config.name}`);
      results.errors.push({
        campaign: config.name,
        error: error.message
      });
    }
  }

  // Print summary
  console.log('\n' + '='.repeat(50));
  console.log('📈 FOMO CAMPAIGN CREATION SUMMARY');
  console.log('='.repeat(50));
  console.log(`✅ Campaigns created: ${results.summary.campaignsCreated}/3`);
  console.log(`✅ Total ads created: ${results.summary.adsCreated}`);
  console.log(`💰 Total daily budget: €${results.summary.totalBudget}`);
  console.log(`📊 Status: All campaigns PAUSED (ready for review)`);
  
  if (results.errors.length > 0) {
    console.log(`\n⚠️  Errors encountered: ${results.errors.length}`);
    results.errors.forEach(err => {
      console.log(`   - ${err.campaign}: ${err.error}`);
    });
  }

  console.log('\n📝 Next Steps:');
  console.log('1. Review campaigns in Facebook Ads Manager');
  console.log('2. Update custom audience IDs in the script');
  console.log('3. Test one campaign at a time');
  console.log('4. Monitor cost per result closely');
  console.log('5. Activate best performing FOMO angle after 48 hours');

  return results;
}

// Error handling wrapper
async function main() {
  try {
    console.log('🔧 IMPORTANT: Update these values before running:');
    console.log('- AD_ACCOUNT_ID (line 5)');
    console.log('- PAGE_ID (line 6)');
    console.log('- PIXEL_ID (line 7)');
    console.log('- Custom audience IDs (lines 89 and 104)\n');
    
    console.log('Press Ctrl+C to cancel or wait 5 seconds to continue...\n');
    
    await new Promise(resolve => setTimeout(resolve, 5000));
    
    const results = await createFOMOCampaigns();
    
    // Save results to file
    const fs = require('fs');
    fs.writeFileSync(
      'fomo-campaigns-results.json',
      JSON.stringify(results, null, 2)
    );
    
    console.log('\n✅ Results saved to fomo-campaigns-results.json');
    
  } catch (error) {
    console.error('\n❌ Fatal error:', error.message);
    process.exit(1);
  }
}

// Run the script
if (require.main === module) {
  main();
}

module.exports = { createFOMOCampaigns, fomoAdCopy };