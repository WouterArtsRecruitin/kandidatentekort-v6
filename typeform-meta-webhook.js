// Typeform Webhook Handler for Meta Conversions API
// Deploy this as a Netlify Function or similar

const crypto = require('crypto');
const axios = require('axios');

// Meta Configuration
const META_PIXEL_ID = '238226887541404';
const META_ACCESS_TOKEN = process.env.META_ACCESS_TOKEN; // Set in Netlify
const META_API_VERSION = 'v18.0';

exports.handler = async (event, context) => {
  // Only accept POST requests
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    // Parse Typeform webhook data
    const typeformData = JSON.parse(event.body);
    
    // Extract form responses
    const formResponse = typeformData.form_response;
    const answers = formResponse.answers || [];
    const hidden = formResponse.hidden || {};
    
    // Map Typeform fields to Meta user data
    const userData = {
      email: getAnswerByFieldId(answers, 'email'),
      phone: getAnswerByFieldId(answers, 'phone'),
      fn: getAnswerByFieldId(answers, 'first_name'),
      ln: getAnswerByFieldId(answers, 'last_name'),
      ct: hidden.stad || hidden.utm_content, // City from UTM
      country: 'nl', // Netherlands
    };

    // Hash user data for Meta
    const hashedUserData = {
      em: userData.email ? hashData(userData.email.toLowerCase()) : null,
      ph: userData.phone ? hashData(userData.phone.replace(/\D/g, '')) : null,
      fn: userData.fn ? hashData(userData.fn.toLowerCase()) : null,
      ln: userData.ln ? hashData(userData.ln.toLowerCase()) : null,
      ct: userData.ct ? hashData(userData.ct.toLowerCase()) : null,
      country: hashData(userData.country),
    };

    // Remove null values
    Object.keys(hashedUserData).forEach(key => 
      hashedUserData[key] === null && delete hashedUserData[key]
    );

    // Prepare Meta Conversions API event
    const metaEvent = {
      event_name: 'Lead',
      event_time: Math.floor(Date.now() / 1000),
      event_source_url: `https://kandidatentekort.nl?utm_source=${hidden.utm_source}&utm_medium=${hidden.utm_medium}&utm_campaign=${hidden.utm_campaign}&utm_content=${hidden.utm_content}`,
      user_data: hashedUserData,
      custom_data: {
        currency: 'EUR',
        value: 249.00, // Value of a lead
        content_name: 'Vacature Analyse',
        content_category: 'Lead Generation',
        utm_source: hidden.utm_source,
        utm_medium: hidden.utm_medium,
        utm_campaign: hidden.utm_campaign,
        utm_content: hidden.utm_content,
        form_id: formResponse.form_id,
        submitted_at: formResponse.submitted_at,
      },
      action_source: 'website',
      event_id: formResponse.token, // Unique ID for deduplication
    };

    // Send to Meta Conversions API
    const metaUrl = `https://graph.facebook.com/${META_API_VERSION}/${META_PIXEL_ID}/events`;
    
    const response = await axios.post(metaUrl, {
      data: [metaEvent],
      access_token: META_ACCESS_TOKEN,
    });

    // Log success
    console.log('Meta Conversions API Response:', response.data);

    return {
      statusCode: 200,
      body: JSON.stringify({
        success: true,
        event_id: metaEvent.event_id,
        events_received: response.data.events_received,
      }),
    };

  } catch (error) {
    console.error('Error processing webhook:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Failed to process webhook',
        message: error.message,
      }),
    };
  }
};

// Helper function to extract answer by field ID
function getAnswerByFieldId(answers, fieldId) {
  const answer = answers.find(a => a.field.id === fieldId);
  if (!answer) return null;
  
  // Handle different answer types
  if (answer.type === 'text') return answer.text;
  if (answer.type === 'email') return answer.email;
  if (answer.type === 'phone_number') return answer.phone_number;
  if (answer.type === 'choice') return answer.choice.label;
  
  return null;
}

// Hash data using SHA256 for Meta
function hashData(data) {
  if (!data) return null;
  return crypto.createHash('sha256').update(data).digest('hex');
}

/* 
SETUP INSTRUCTIONS:

1. Deploy this as a Netlify Function:
   - Save as: netlify/functions/typeform-webhook.js
   - Set META_ACCESS_TOKEN in Netlify environment variables

2. Configure Typeform Webhook:
   - Go to your Typeform: https://admin.typeform.com/form/kalFRTCA/connect
   - Add webhook URL: https://kandidatentekort.nl/.netlify/functions/typeform-webhook
   
3. Test with:
   curl -X POST https://kandidatentekort.nl/.netlify/functions/typeform-webhook \
     -H "Content-Type: application/json" \
     -d '{"form_response": {"token": "test123", "hidden": {"utm_source": "facebook"}}}'

4. Benefits:
   - Real-time lead tracking in Meta
   - Better attribution for campaigns
   - Custom audiences based on form submissions
   - Lookalike audiences from high-quality leads
*/