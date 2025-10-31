# 🚀 Fashion Store - Render Free Tier Deployment Guide

This guide will help you deploy your Django Fashion Store to Render's free tier.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Environment Variables**: Prepare your secrets and API keys

## 🔧 Deployment Steps

### Step 1: Prepare Your Repository

1. Ensure all files are committed to your GitHub repository:
   ```bash
   git add .
   git commit -m "Add Render deployment configuration"
   git push origin main
   ```

### Step 2: Create Render Services

#### Option A: Using Render Dashboard (Recommended for beginners)

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)

2. **Create PostgreSQL Database**:
   - Click "New" → "PostgreSQL"
   - Name: `fashion-store-db`
   - Database Name: `fashion_store`
   - User: `fashion_store_user`
   - Plan: Free
   - Click "Create Database"
   - **Copy the Database URL** for later use

3. **Create Web Service**:
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select your `fashion_store` repository
   - Configure:
     - **Name**: `fashion-store`
     - **Runtime**: `Python 3`
     - **Build Command**: `./build.sh`
     - **Start Command**: `./start.sh`
     - **Plan**: Free

4. **Set Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE=fashion_store.production_settings
   SECRET_KEY=<generate-a-secure-random-key>
   DEBUG=False
   DATABASE_URL=<paste-your-database-url-from-step-2>
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@fashionstore.com
   DJANGO_SUPERUSER_PASSWORD=<choose-secure-password>
   ```

5. **Deploy**: Click "Create Web Service"

#### Option B: Using render.yaml (Infrastructure as Code)

1. **Go to Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
2. **Click "New" → "Blueprint"**
3. **Connect your GitHub repository**
4. **Select your repository** and the `render.yaml` file will be automatically detected
5. **Set environment variables** as needed
6. **Click "Apply"**

### Step 3: Configure Environment Variables

Add these environment variables in your Render service settings:

```bash
# Required
DJANGO_SETTINGS_MODULE=fashion_store.production_settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False

# Database (auto-provided by Render PostgreSQL)
DATABASE_URL=postgresql://...

# Admin User (optional)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=secure-password

# Email (optional - for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=Fashion Store <noreply@yourdomain.com>
```

### Step 4: Domain Setup

1. **Default Domain**: Your app will be available at `https://fashion-store-XXXX.onrender.com`
2. **Custom Domain**: Add your domain in Service Settings → Custom Domains

### Step 5: Post-Deployment

1. **Access Admin Panel**: Go to `https://your-app.onrender.com/admin/`
2. **Login**: Use the superuser credentials you set
3. **Add Products**: Import your products via admin or CSV upload
4. **Test Features**: Verify search, cart, authentication work properly

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check build logs in Render dashboard
   - Ensure `requirements.txt` has all dependencies
   - Verify `build.sh` has execute permissions

2. **Static Files Not Loading**:
   - Ensure `STATIC_ROOT` is set correctly
   - Check WhiteNoise configuration in settings
   - Verify `collectstatic` runs in build script

3. **Database Connection Error**:
   - Verify `DATABASE_URL` environment variable
   - Check PostgreSQL service is running
   - Ensure database migrations completed

4. **502 Bad Gateway**:
   - Check application logs
   - Verify `start.sh` script
   - Ensure Gunicorn starts properly

### Monitoring

- **Logs**: Available in Render dashboard
- **Metrics**: Monitor CPU, memory usage
- **Health Checks**: Automatic monitoring included

## 💡 Optimization Tips

1. **Free Tier Limitations**:
   - Apps sleep after 15 minutes of inactivity
   - 512MB RAM limit
   - 750 hours/month (enough for 1 app)

2. **Performance**:
   - Use database indexes for queries
   - Optimize images before upload
   - Enable browser caching with WhiteNoise

3. **Cost Management**:
   - Monitor usage in dashboard
   - Consider upgrading for production apps

## 🆘 Support

- **Render Docs**: [render.com/docs](https://render.com/docs)
- **Django Deployment**: [docs.djangoproject.com](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- **GitHub Issues**: Create issues in your repository

## 🎉 Success!

Your Fashion Store should now be live on Render! 

Visit your app at: `https://your-app-name.onrender.com`

Admin panel: `https://your-app-name.onrender.com/admin/`

## 📁 Files Created for Deployment

- `build.sh` - Render build script
- `start.sh` - Render start script  
- `render.yaml` - Infrastructure as Code
- `production_settings.py` - Production Django settings
- `.env.render` - Environment variables template
- `requirements.txt` - Updated with production dependencies

## 🚀 Quick Deploy Commands

After making changes:
```bash
git add .
git commit -m "Update Fashion Store"
git push origin main
```

Render will automatically redeploy your changes!