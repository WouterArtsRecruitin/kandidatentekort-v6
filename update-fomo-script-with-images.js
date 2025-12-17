// Extended version of createAdCreative function with image support

const imageLibrary = {
  cold: [
    // Option 1: Using existing images from your library
    {
      image_hash: 'YOUR_EXISTING_IMAGE_HASH_1', // Calculator/money image
      picture: 'https://kandidatentekort.nl/images/vacature-kosten-calculator.jpg'
    },
    {
      image_hash: 'YOUR_EXISTING_IMAGE_HASH_2', // Team stress image
      picture: 'https://kandidatentekort.nl/images/team-overbelast.jpg'
    },
    {
      image_hash: 'YOUR_EXISTING_IMAGE_HASH_3', // Clock/time image
      picture: 'https://kandidatentekort.nl/images/tijd-is-geld.jpg'
    }
  ],
  warm: [
    {
      image_hash: 'YOUR_WARM_IMAGE_HASH_1', // Countdown timer
      picture: 'https://kandidatentekort.nl/images/48-uur-countdown.jpg'
    },
    {
      image_hash: 'YOUR_WARM_IMAGE_HASH_2', // Before/after
      picture: 'https://kandidatentekort.nl/images/voor-na-vergelijking.jpg'
    },
    {
      image_hash: 'YOUR_WARM_IMAGE_HASH_3', // Calendar urgency
      picture: 'https://kandidatentekort.nl/images/kalender-verlies.jpg'
    }
  ],
  hot: [
    {
      image_hash: 'YOUR_HOT_IMAGE_HASH_1', // Limited time badge
      picture: 'https://kandidatentekort.nl/images/vandaag-alleen.jpg'
    },
    {
      image_hash: 'YOUR_HOT_IMAGE_HASH_2', // Urgency meter
      picture: 'https://kandidatentekort.nl/images/laatste-plekken.jpg'
    },
    {
      image_hash: 'YOUR_HOT_IMAGE_HASH_3', // Bonus stack
      picture: 'https://kandidatentekort.nl/images/gratis-bonus.jpg'
    }
  ]
};

// Updated createAdCreative function with images
async function createAdCreativeWithImage(adCopy, utmParams, adIndex, adType) {
  try {
    const image = imageLibrary[adType][adIndex];
    
    const creativeData = {
      name: `FOMO Creative ${adType} ${adIndex + 1}`,
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
          // Use either image_hash (for pre-uploaded images) or picture URL
          ...(image.image_hash ? { image_hash: image.image_hash } : { picture: image.picture })
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
    console.error('Error creating ad creative with image:', error.response?.data || error);
    throw error;
  }
}

// Quick function to upload images to Facebook if needed
async function uploadImageToFacebook(imagePath) {
  const FormData = require('form-data');
  const fs = require('fs');
  
  const form = new FormData();
  form.append('filename', fs.createReadStream(imagePath));
  form.append('access_token', ACCESS_TOKEN);
  
  try {
    const response = await axios.post(
      `https://graph.facebook.com/v18.0/${AD_ACCOUNT_ID}/adimages`,
      form,
      {
        headers: form.getHeaders()
      }
    );
    
    return response.data.images[Object.keys(response.data.images)[0]].hash;
  } catch (error) {
    console.error('Error uploading image:', error.response?.data || error);
    throw error;
  }
}

// Example: How to use existing images from Facebook Page posts
async function getImagesFromPagePosts() {
  try {
    // Get recent posts with images
    const response = await axios.get(
      `https://graph.facebook.com/v18.0/${PAGE_ID}/posts`,
      {
        params: {
          fields: 'full_picture,message,created_time',
          limit: 50,
          access_token: ACCESS_TOKEN
        }
      }
    );
    
    // Filter posts with images that mention costs/urgency
    const fomoImages = response.data.data.filter(post => {
      const hasImage = post.full_picture;
      const hasFomoContent = post.message && (
        post.message.includes('€') ||
        post.message.includes('verlies') ||
        post.message.includes('kost') ||
        post.message.includes('bespaar')
      );
      return hasImage && hasFomoContent;
    });
    
    console.log(`Found ${fomoImages.length} potential FOMO images from page posts`);
    return fomoImages;
    
  } catch (error) {
    console.error('Error fetching page images:', error.response?.data || error);
    return [];
  }
}

// Add this to your main script to check for existing images
async function checkExistingImages() {
  console.log('\n🖼️  Checking for existing images...\n');
  
  // Check Facebook Page for existing images
  const pageImages = await getImagesFromPagePosts();
  if (pageImages.length > 0) {
    console.log('Found existing images on Facebook Page:');
    pageImages.slice(0, 5).forEach((post, index) => {
      console.log(`${index + 1}. ${post.message?.substring(0, 50)}...`);
      console.log(`   Image: ${post.full_picture}`);
    });
  }
  
  // Check ad account for uploaded images
  try {
    const response = await axios.get(
      `https://graph.facebook.com/v18.0/${AD_ACCOUNT_ID}/adimages`,
      {
        params: {
          fields: 'hash,url,created_time,name',
          limit: 100,
          access_token: ACCESS_TOKEN
        }
      }
    );
    
    console.log(`\n📁 Found ${response.data.data.length} images in ad account`);
    
  } catch (error) {
    console.log('Could not retrieve ad account images');
  }
}

module.exports = { 
  createAdCreativeWithImage, 
  uploadImageToFacebook, 
  getImagesFromPagePosts,
  checkExistingImages,
  imageLibrary 
};