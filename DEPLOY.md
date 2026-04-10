# Deployment Guide - Render

This guide will help you deploy the AI Resume Pro application to Render.

## Prerequisites

1. **GitHub Account** - Push your code to GitHub
2. **Render Account** - Sign up at https://render.com
3. **Google Gemini API Key** - Get from https://ai.google.dev
4. **Git installed** - For version control

## Step 1: Prepare GitHub Repository

1. Make sure all files are committed:
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin master
   ```

2. Verify your repository is public or has Render access

## Step 2: Deploy on Render

### 2.1 Connect GitHub to Render

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Select **Connect a repository**
4. Authorize Render to access your GitHub account
5. Find and select your AI Resume repository

### 2.2 Configure the Web Service

1. **Name**: `ai-resume-pro` (or your preferred name)
2. **Environment**: Python
3. **Region**: Choose closest to your users
4. **Branch**: `master`
5. **Build Command**: `pip install -r requirements.txt && python -m nltk.downloader punkt`
6. **Start Command**: Leave blank (Procfile will be used automatically)
7. **Instance Type**: Free (for testing) or Starter+ (recommended)

### 2.3 Add Environment Variables

Click **Environment** and add these variables:

```
FLASK_ENV=production
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

⚠️ **CRITICAL**: 
- Get your API key from: https://ai.google.dev/aistudio/
- Never commit API keys - always use environment variables

### 2.4 Deploy

1. Click **Create Web Service**
2. Wait for build to complete (2-5 minutes)
3. Check logs for errors at the bottom of the dashboard
4. Once deployed, you'll get a URL like: `https://ai-resume-pro.onrender.com`

## Step 3: Verify Deployment

1. Visit your Render URL
2. Test the analyzer feature
3. Upload a PDF resume
4. Check console for any errors

## Troubleshooting

### Common Issues

**1. "ModuleNotFoundError: No module named 'nltk'"**
- The build command includes: `python -m nltk.downloader punkt`
- This downloads required NLTK data during build

**2. "API Key not available"**
- Go to Render Dashboard → Environment
- Verify `GOOGLE_API_KEY` is set correctly
- Restart the service

**3. PDF Upload Fails**
- Check file size (must be 10KB-5MB)
- Ensure it's valid PDF format
- Check Render logs for details

**4. Slow First Request**
- Free tier goes to sleep after 15 min inactivity
- First request wakes it up (can be 30+ seconds)
- Upgrade to Starter+ for always-on instance

### View Logs

In Render Dashboard:
1. Click your service
2. Scroll to bottom for **Logs**
3. Check for error messages

## Important Notes

### File Storage
- Uploaded files are stored in `/uploads` directory
- **On Render free tier**: Files are ephemeral (deleted after deploy)
- **Solution**: For production, add cloud storage (AWS S3, Google Cloud Storage)

### Database
- Current app uses no database
- Files are temporary
- For persistence, add a database later

### API Rate Limits
- Google Gemini has usage limits (free tier: 60 requests/minute)
- Monitor usage at https://ai.google.dev/aistudio/

### Cost Estimation
- **Render Free Tier**: $0/month (with limitations)
- **Starter+ ($7/month)**: Always-on, better performance
- **Deployment**: $0 for bandwidth on free tier
- **API Costs**: Depends on Google Gemini usage

## Performance Optimization (Optional)

For faster deployments:
1. Consider Starter+ instance ($7/month)
2. Add Redis cache for repeated analysis
3. Pre-download NLTK data in build
4. Use CloudFlare for CDN

## Next Steps

1. Set up custom domain (optional)
   - Go to Render → Settings → Custom Domain
   - Point your domain to Render

2. Monitor usage
   - Check Render dashboard regularly
   - Monitor API calls and errors

3. Upgrade if needed
   - Switch from free to paid tier
   - Render maintains your URL

## Quick Redeploy

If you make changes and want to deploy:

```bash
git add .
git commit -m "Description of changes"
git push origin master
```

Render automatically rebuilds when you push to `master` branch.

## Need Help?

- Render Docs: https://render.com/docs
- Flask Deployment: https://flask.palletsprojects.com/deploying/
- Google AI: https://ai.google.dev/

---

**Your app will be live at**: `https://[your-service-name].onrender.com`
