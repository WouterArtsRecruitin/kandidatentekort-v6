# 🚀 Kandidatentekort V6 - Manual Render Deployment

Since the API token is invalid, here's how to deploy using Render's GitHub integration:

## Step 1: Sign in to Render
1. Go to https://dashboard.render.com
2. Sign in with your account

## Step 2: Create New Web Service
1. Click **"New +"** button in the dashboard
2. Select **"Web Service"**

## Step 3: Connect GitHub Repository
1. Select **"Build and deploy from a Git repository"**
2. Click **"Connect GitHub"** (if not already connected)
3. Search for: `kandidatentekort-v6`
4. Select the repository: `WouterArtsRecruitin/kandidatentekort-v6`

## Step 4: Configure Service
Render will auto-detect the `render.yaml` file and suggest these settings:

- **Name**: kandidatentekort-v6
- **Region**: Frankfurt (EU Central)
- **Branch**: main
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

## Step 5: Set Environment Variables
Add these environment variables in the Render dashboard:

1. **CLAUDE_API_KEY** = `[Your Claude API Key]`
2. **RESEND_API_KEY** = `[Your Resend API Key]`
3. **PIPEDRIVE_API_TOKEN** = `[Your Pipedrive Token]`
4. **SLACK_WEBHOOK_URL** = `[Your Slack Webhook]`
5. **MANUAL_REVIEW_MODE** = `false`
6. **FLASK_ENV** = `production`
7. **PYTHON_VERSION** = `3.11.0`

## Step 6: Select Plan
- Choose **"Starter"** plan ($7/month) or **"Free"** for testing

## Step 7: Deploy
1. Click **"Create Web Service"**
2. Render will start building and deploying automatically
3. Wait 3-5 minutes for deployment to complete

## 📊 Monitor Deployment
- View logs: https://dashboard.render.com/web/[service-id]/logs
- Check metrics: https://dashboard.render.com/web/[service-id]/metrics

## 🔗 Your Service URL
Once deployed, your service will be available at:
```
https://kandidatentekort-v6.onrender.com
```

## ✅ Verify Deployment
Test your deployment:
```bash
curl https://kandidatentekort-v6.onrender.com/
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-12-16T...",
  "version": "6.0.1",
  "claude_available": true,
  "manual_review_mode": false
}
```

## 🔑 Get New API Key (if needed)
1. Go to: https://dashboard.render.com/account/api-keys
2. Click **"Create API Key"**
3. Give it a name: "kandidatentekort-deployment"
4. Copy the FULL key immediately (shown only once!)
5. Save it securely

## 🎉 Success!
Your V6.0+ Enhanced Production API is now live!