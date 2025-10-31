# 🔐 Social Authentication Setup Guide

## Overview
Your Django Fashion Store now supports Google and Facebook login using Django Allauth. Users can register and login using their social media accounts in addition to traditional email/password authentication.

## ✅ What's Already Configured

### 🛠️ Installed & Configured
- ✅ **Django Allauth** - Social authentication framework
- ✅ **Google OAuth** provider
- ✅ **Facebook Login** provider
- ✅ **Updated Login/Register** templates with social buttons
- ✅ **Database migrations** applied
- ✅ **Site configuration** set to localhost:8000

### 🎨 UI Updates
- ✅ **Login Page**: Now includes Google & Facebook buttons
- ✅ **Register Page**: Now includes Google & Facebook buttons
- ✅ **Modern Design**: Bootstrap-styled social login buttons

## 🔧 Setup Instructions

### Method 1: Using Management Command (Recommended)

#### Set up Google OAuth
```bash
# 1. Get credentials from Google Console
# Visit: https://console.developers.google.com/

# 2. Add Google app
python manage.py setup_social_auth --add-google \
  --google-client-id "YOUR_GOOGLE_CLIENT_ID" \
  --google-secret "YOUR_GOOGLE_CLIENT_SECRET"
```

#### Set up Facebook Login
```bash
# 1. Get credentials from Facebook Developers
# Visit: https://developers.facebook.com/

# 2. Add Facebook app
python manage.py setup_social_auth --add-facebook \
  --facebook-app-id "YOUR_FACEBOOK_APP_ID" \
  --facebook-secret "YOUR_FACEBOOK_APP_SECRET"
```

### Method 2: Django Admin Interface

1. **Access Admin**: Go to `http://localhost:8000/admin/`
2. **Login**: Use your superuser credentials
3. **Configure Site**:
   - Go to `Sites` → `Sites`
   - Edit the site to use domain: `localhost:8000`
4. **Add Social Applications**:
   - Go to `Social Applications` → `Social applications`
   - Click "Add Social Application"
   - Select provider (Google or Facebook)
   - Enter your app credentials
   - Select the site

## 🔑 Getting OAuth Credentials

### Google OAuth Setup
1. **Visit**: [Google Console](https://console.developers.google.com/)
2. **Create Project**: Or select existing one
3. **Enable APIs**: Enable Google+ API or Google Identity
4. **Create Credentials**:
   - Go to Credentials → Create → OAuth 2.0 Client ID
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`
5. **Copy**: Client ID and Client Secret

### Facebook App Setup
1. **Visit**: [Facebook Developers](https://developers.facebook.com/)
2. **Create App**: Choose "Consumer" type
3. **Add Product**: Facebook Login
4. **Configure**:
   - Valid OAuth Redirect URIs: `http://localhost:8000/accounts/facebook/login/callback/`
   - App Domains: `localhost`
5. **Get Credentials**: App ID and App Secret from Settings → Basic

## 🚀 How It Works

### User Experience
1. **Visit Login/Register**: Users see traditional form + social buttons
2. **Click Social Button**: Redirected to Google/Facebook
3. **Authorize**: User grants permission
4. **Auto-Registration**: If new user, account created automatically
5. **Profile Creation**: UserProfile created via signals
6. **Redirect**: Back to homepage logged in

### Technical Flow
```
User clicks → OAuth Provider → Authorization → Callback → Account Creation/Login → Redirect
```

## 🧪 Testing

### With Demo Credentials (UI Only)
```bash
# Current demo setup shows buttons but won't work for actual login
python manage.py setup_social_auth --list-apps
```

### With Real Credentials
1. Set up real Google/Facebook apps
2. Update credentials using management command
3. Test login flow

## 📋 Available Commands

### Setup Commands
```bash
# Set up site
python manage.py setup_social_auth --setup-site

# List configured apps
python manage.py setup_social_auth --list-apps

# Show setup instructions
python manage.py setup_social_auth
```

### Management Commands
```bash
# Add/Update Google app
python manage.py setup_social_auth --add-google --google-client-id ID --google-secret SECRET

# Add/Update Facebook app
python manage.py setup_social_auth --add-facebook --facebook-app-id ID --facebook-secret SECRET
```

## 🔧 Configuration Details

### Settings Configuration
```python
# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
LOGIN_REDIRECT_URL = '/'
SOCIALACCOUNT_AUTO_SIGNUP = True
```

### URL Configuration
```python
# Main URLs include allauth
path('accounts/', include('allauth.urls')),
```

## 🌐 Production Deployment

### Update Settings
1. **Change Site Domain**: From `localhost:8000` to your domain
2. **Update OAuth Apps**: Change redirect URIs to production URLs
3. **Environment Variables**: Store secrets securely
4. **HTTPS**: Ensure OAuth apps use HTTPS in production

### Environment Variables Example
```bash
# .env file
GOOGLE_CLIENT_ID=your_production_google_client_id
GOOGLE_CLIENT_SECRET=your_production_google_secret
FACEBOOK_APP_ID=your_production_facebook_app_id
FACEBOOK_APP_SECRET=your_production_facebook_secret
```

## 🔍 Troubleshooting

### Common Issues

**Social buttons not appearing**
- Check that allauth is in INSTALLED_APPS
- Verify templates load socialaccount tags
- Ensure apps are configured and assigned to site

**OAuth errors**
- Verify redirect URIs match exactly
- Check app is in correct mode (development/production)
- Ensure credentials are correct

**Permission denied**
- Check OAuth app permissions
- Verify app is approved for production (Facebook)
- Check domain restrictions

## 📊 User Management

### Admin Interface
- **Users**: Standard Django user management
- **Social Accounts**: View linked social accounts
- **Social Applications**: Manage OAuth apps
- **Social Tokens**: View access tokens

### Programmatic Access
```python
# Check if user has social account
user.socialaccount_set.filter(provider='google').exists()

# Get social account data
social_account = user.socialaccount_set.get(provider='google')
extra_data = social_account.extra_data
```

## 🔗 URLs

### Authentication URLs
- **Login**: `/login/` or `/accounts/login/`
- **Register**: `/register/` or `/accounts/signup/`
- **Google OAuth**: `/accounts/google/login/`
- **Facebook OAuth**: `/accounts/facebook/login/`
- **Logout**: `/logout/` or `/accounts/logout/`

### Admin URLs
- **Admin Panel**: `/admin/`
- **Social Apps**: `/admin/socialaccount/socialapp/`
- **Sites**: `/admin/sites/site/`

## 📞 Support

### Quick Diagnostics
```bash
# Check current configuration
python manage.py setup_social_auth --list-apps

# Verify site setup
python manage.py shell -c "from django.contrib.sites.models import Site; print(Site.objects.get(id=1))"
```

### Further Help
- Django Allauth Documentation: https://django-allauth.readthedocs.io/
- Google OAuth Documentation: https://developers.google.com/identity/protocols/oauth2
- Facebook Login Documentation: https://developers.facebook.com/docs/facebook-login/