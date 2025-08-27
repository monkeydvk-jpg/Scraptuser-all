# 🚀 Deployment Guide

## Vercel Deployment Options

### Option 1: Deploy V2-Web Subdirectory (Recommended)

Since you're getting a 404 error, the easiest solution is to deploy the V2-Web folder as a separate project:

1. **Create a new repository for V2-Web only:**
   ```bash
   cd V2-Web
   git init
   git add .
   git commit -m "Initial V2-Web deployment"
   git remote add origin https://github.com/monkeydvk-jpg/adobe-stock-web.git
   git push -u origin main
   ```

2. **Deploy from Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import the new repository
   - Vercel will auto-detect Next.js
   - Deploy automatically

### Option 2: Deploy from Current Repository

If you want to deploy from the current repository structure:

1. **In Vercel Dashboard:**
   - Go to your project settings
   - Set **Root Directory** to `V2-Web`
   - Set **Build Command** to `npm run build`
   - Set **Install Command** to `npm install`
   - Set **Output Directory** to `.next`

2. **Alternative: Use Vercel CLI**
   ```bash
   cd V2-Web
   npx vercel --prod
   ```

### Option 3: Monorepo Deployment (Current Setup)

The root `vercel.json` is configured for monorepo deployment. If this doesn't work:

1. **Try deploying with Vercel CLI from root:**
   ```bash
   npx vercel --prod
   ```

2. **Or specify the project directory:**
   ```bash
   vercel --cwd V2-Web --prod
   ```

## 🔧 Troubleshooting Common Issues

### 404 NOT_FOUND Error
- **Cause**: Vercel can't find the Next.js app
- **Solution**: Set correct Root Directory in Vercel settings to `V2-Web`

### Build Failures
- **Cause**: Missing dependencies or wrong build commands
- **Solution**: Ensure `V2-Web/package.json` exists and all deps are listed

### Function Timeout
- **Cause**: Puppeteer taking too long
- **Solution**: The `vercel.json` sets maxDuration to 300s (5 minutes)

## 📋 Quick Deploy Checklist

- [ ] V2-Web folder contains all necessary files
- [ ] package.json has correct dependencies
- [ ] Next.js app builds successfully locally
- [ ] Vercel project settings point to correct directory
- [ ] Environment variables set (if needed)

## 🌟 Recommended Approach

**Create a separate repository for V2-Web:**
This is the cleanest approach and avoids monorepo complexity.

```bash
# Navigate to V2-Web
cd V2-Web

# Initialize new git repository
git init

# Add all files
git add .

# Commit
git commit -m "🚀 Adobe Stock Prompt Generator Web v2.0"

# Create new repository on GitHub: adobe-stock-web
# Add remote
git remote add origin https://github.com/monkeydvk-jpg/adobe-stock-web.git

# Push
git push -u origin main

# Deploy to Vercel from this new repository
```

This approach ensures the cleanest deployment and fastest build times.
