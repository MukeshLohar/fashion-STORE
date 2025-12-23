# 📜 Scripts Quick Reference Guide

> All scripts and commands available in Sri Devi Fashion Jewellery project

---

## 🚀 Deployment Scripts

### build.sh
**Purpose:** Build application for Render.com deployment
```bash
./build.sh
```
**What it does:**
- Installs dependencies
- Collects static files
- Runs migrations
- Creates superuser (if none exists)

**Environment Variables:**
- `DJANGO_SUPERUSER_USERNAME` (optional, default: admin)
- `DJANGO_SUPERUSER_EMAIL` (optional, default: admin@fashionstore.com)
- `DJANGO_SUPERUSER_PASSWORD` (optional, default: admin123)

---

### start.sh
**Purpose:** Start Gunicorn server on Render.com
```bash
./start.sh
```
**Configuration:**
- Workers: 2
- Port: $PORT (from Render)
- Settings: production_settings

---

### deploy_to_render.sh
**Purpose:** Quick deploy to Render via GitHub push
```bash
./deploy_to_render.sh
```
**What it does:**
- Commits changes
- Pushes to GitHub
- Triggers Render auto-deploy

---

## 🔧 Django Management Commands

### Server & Setup

**Run Development Server**
```bash
python manage.py runserver
# Access at: http://localhost:8000
```

**Make Migrations**
```bash
python manage.py makemigrations
```

**Run Migrations**
```bash
python manage.py migrate
```

**Create Superuser**
```bash
python manage.py createsuperuser
```

**Collect Static Files**
```bash
python manage.py collectstatic --no-input
```

**Django Shell**
```bash
python manage.py shell
```

---

### Data Management

**Create Sample Data**
```bash
# Create sample categories and products
python manage.py create_sample_data

# Clear existing data first
python manage.py create_sample_data --clear
```

**Add Single Product**
```bash
python manage.py add_product \
  --name "Product Name" \
  --category "Category Name" \
  --price 1999 \
  --stock 50 \
  --weight 0.5 \
  --description "Product description" \
  --size M \
  --color blue
```

**Import Products from CSV**
```bash
python manage.py import_products sample_products.csv
```

**CSV Format:**
```csv
name,category,price,stock,description,size,color,material,brand,weight_kg
Product1,Category1,999,50,Description,M,red,Cotton,Brand1,0.3
```

**Update Inventory**
```bash
python manage.py update_inventory <product_id> <new_stock>
```

---

### Shipping Configuration

**Setup Basic Shipping Rates**
```bash
python manage.py setup_shipping
```
Creates standard shipping rates.

**Setup India Zone-Based Shipping**
```bash
python manage.py setup_zone_shipping
```
Creates 5 zones (North, South, East, West, Central) with sample pincodes.

**Setup International Shipping**
```bash
python manage.py setup_international_shipping
```
Creates shipping rates for USA, UK, Canada, Australia, UAE, etc.

**Setup International Pincodes**
```bash
python manage.py setup_international_pincodes
```
Adds postal codes for international countries.

---

### Social Authentication

**Setup Social Auth Providers**
```bash
python manage.py setup_social_auth
```
Configures Google and Facebook OAuth providers.

---

## 🐳 Docker Commands

**Build Image**
```bash
docker build -t fashion-store .
```

**Run Container**
```bash
docker run -d -p 8000:8000 --name fashion-store fashion-store
```

**Run with Environment Variables**
```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret \
  -e DEBUG=False \
  -e DATABASE_URL=postgres://... \
  --name fashion-store \
  fashion-store
```

**Stop Container**
```bash
docker stop fashion-store
```

**Remove Container**
```bash
docker rm fashion-store
```

**View Logs**
```bash
docker logs fashion-store
```

---

## 🗄️ Database Commands

**SQLite (Development)**
```bash
# Access SQLite database
sqlite3 db.sqlite3

# Backup database
cp db.sqlite3 db.sqlite3.backup

# Restore database
cp db.sqlite3.backup db.sqlite3
```

**PostgreSQL (Production)**
```bash
# Create backup
pg_dump -h <host> -U <user> -d <database> > backup.sql

# Restore backup
psql -h <host> -U <user> -d <database> < backup.sql

# Connect to database
psql -h <host> -U <user> -d <database>
```

---

## 🧪 Testing Commands

**Run All Tests**
```bash
python manage.py test
```

**Run Specific App Tests**
```bash
python manage.py test shop
```

**Run Specific Test Class**
```bash
python manage.py test shop.tests.ProductTestCase
```

**Run with Coverage**
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

---

## 🔍 Debugging Commands

**Check for Issues**
```bash
python manage.py check
```

**Validate Models**
```bash
python manage.py validate
```

**Show Migrations**
```bash
python manage.py showmigrations
```

**SQL for Migration**
```bash
python manage.py sqlmigrate shop 0001
```

**Database Shell**
```bash
python manage.py dbshell
```

---

## 📊 Admin Commands

**Change User Password**
```bash
python manage.py changepassword <username>
```

**Clear Cache**
```bash
python manage.py clear_cache
```

**Flush Database (Careful!)**
```bash
python manage.py flush
```

---

## 🔧 Git Commands (for deployment)

**Initial Setup**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <github-url>
git push -u origin main
```

**Regular Updates**
```bash
git add .
git commit -m "Update message"
git push origin main
```

**Check Status**
```bash
git status
git log --oneline
```

---

## 🌐 Environment Setup

**Create .env File**
```bash
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

RAZORPAY_KEY_ID=rzp_test_xxxxx
RAZORPAY_KEY_SECRET=xxxxxxxx

PAYPAL_CLIENT_ID=xxxxxxxx
PAYPAL_CLIENT_SECRET=xxxxxxxx
PAYPAL_MODE=sandbox
EOF
```

**Virtual Environment**
```bash
# Create
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Deactivate
deactivate
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Freeze Dependencies**
```bash
pip freeze > requirements.txt
```

---

## 📝 Quick Start Cheat Sheet

**First Time Setup:**
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file (see above)

# 4. Run migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Load sample data
python manage.py create_sample_data

# 7. Run server
python manage.py runserver
```

**Daily Development:**
```bash
# Activate environment
source venv/bin/activate

# Make migrations if models changed
python manage.py makemigrations
python manage.py migrate

# Run server
python manage.py runserver
```

**Deployment:**
```bash
# Quick deploy to Render
./deploy_to_render.sh

# Or manual
git add .
git commit -m "Update"
git push origin main
```

---

## 🔗 Useful URLs

**Development:**
- Home: http://localhost:8000
- Admin: http://localhost:8000/admin
- Products: http://localhost:8000/products
- Cart: http://localhost:8000/cart

**Production (Render):**
- App: https://your-app.onrender.com
- Admin: https://your-app.onrender.com/admin

**Dashboards:**
- Render: https://dashboard.render.com
- Razorpay: https://dashboard.razorpay.com
- PayPal: https://www.paypal.com/merchantapps
- Google Console: https://console.cloud.google.com
- Facebook Developers: https://developers.facebook.com

---

## 🆘 Troubleshooting Commands

**Port Already in Use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database Locked (SQLite):**
```bash
# Stop server, delete db.sqlite3-journal
rm db.sqlite3-journal
```

**Static Files Not Loading:**
```bash
# Collect static files again
python manage.py collectstatic --clear --no-input
```

**Migration Conflicts:**
```bash
# Show migrations
python manage.py showmigrations

# Fake migration if needed
python manage.py migrate --fake shop 0001

# Or reset migrations (careful!)
python manage.py migrate shop zero
```

**Clear Sessions:**
```bash
python manage.py clearsessions
```

---

## 📚 Documentation References

- Complete Documentation: `PROJECT_DOCUMENTATION.md`
- Code Review: `CODE_REVIEW_SUMMARY.md`
- Setup Guide: `README.md`
- Deployment: `RENDER_DEPLOYMENT.md`
- Shipping: `SHIPPING_GUIDE.md`
- Social Auth: `SOCIAL_AUTH_GUIDE.md`

---

**Last Updated:** November 8, 2025  
**Project:** Sri Devi Fashion Jewellery  
**Framework:** Django 4.2.7
