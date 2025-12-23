# 📚 Sri Devi Fashion Jewellery - Complete Project Documentation

> **Version:** 1.0  
> **Last Updated:** November 8, 2025  
> **Django Version:** 4.2.7  
> **Python Version:** 3.8+

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Code Integrity Analysis](#code-integrity-analysis)
3. [Application Architecture](#application-architecture)
4. [Database Models](#database-models)
5. [Workflow Documentation](#workflow-documentation)
6. [Scripts Reference](#scripts-reference)
7. [API Endpoints](#api-endpoints)
8. [Configuration Files](#configuration-files)
9. [Deployment Guide](#deployment-guide)
10. [Issues & Recommendations](#issues--recommendations)

---

## 🎯 Project Overview

**Sri Devi Fashion Jewellery** is a full-featured Django e-commerce platform for fashion retail with the following capabilities:

### Core Features
- ✅ User authentication with Django Allauth (Email, Google, Facebook)
- ✅ Product catalog with categories, filters, and search
- ✅ Session-based shopping cart
- ✅ Multi-payment gateway integration (Razorpay, PayPal)
- ✅ Weight-based shipping calculation
- ✅ Zone-based shipping for India
- ✅ International shipping support
- ✅ Order management and tracking
- ✅ Product reviews and ratings
- ✅ User wishlist functionality
- ✅ Multi-currency support (INR, USD, EUR, GBP)
- ✅ SEO optimization with sitemaps
- ✅ Responsive luxury UI design

### Technology Stack
- **Backend:** Django 4.2.7
- **Database:** SQLite (dev), PostgreSQL (production)
- **Payment:** Razorpay, PayPal REST SDK
- **Authentication:** Django Allauth
- **Frontend:** Bootstrap 5, vanilla JavaScript
- **Deployment:** Render.com, Docker support
- **Static Files:** WhiteNoise
- **Server:** Gunicorn

---

## 🔍 Code Integrity Analysis

### ✅ Issues Found & Status

#### 1. **CRITICAL: Duplicate Dependency in requirements.txt**
**Location:** `/home/coder/fashion_store/requirements.txt`
**Issue:** `django-allauth==0.57.0` appears twice (lines 13 and 21)

**Impact:** Low - pip handles duplicates, but it's poor practice
**Status:** ⚠️ NEEDS FIX

```python
# Current (lines 11-21):
gunicorn==21.2.0
whitenoise==6.6.0
requests==2.31.0
urllib3==2.1.0
cryptography
django-allauth==0.57.0  # ← First occurrence
dj-database-url==2.1.0
python-dateutil==2.8.2
openpyxl==3.1.2
# JSON handling
simplejson==3.19.2

# Social Authentication
django-allauth==0.57.0  # ← Duplicate (REMOVE THIS)
```

**Fix Required:**
```bash
# Remove line 21 from requirements.txt
```

#### 2. **Code Quality Issues**

**a) Missing CART_SESSION_ID in settings.py**
- **Location:** `shop/cart.py` line 19
- **Issue:** Falls back to 'cart' if not defined
- **Impact:** Low - works with default, but should be explicit
- **Recommendation:** Add to `settings.py`:
```python
CART_SESSION_ID = 'cart'
```

**b) Free Shipping Feature Disabled**
- **Location:** `shop/models.py` lines 372-374
- **Issue:** Free shipping code is commented out
- **Current behavior:** No free shipping regardless of threshold
- **Impact:** Medium - business decision, but should be documented

**c) Payment Method Choices Limited**
- **Location:** `shop/models.py` line 213
- **Issue:** Missing 'cod' (Cash on Delivery) option mentioned in README
- **Impact:** Medium - inconsistency between docs and code

#### 3. **Security Review**

✅ **Passed:**
- CSRF protection enabled
- SQL injection protection (Django ORM)
- XSS filters enabled
- Secure session cookies in production
- Environment variables for secrets
- Password validation configured

⚠️ **Warnings:**
- Email backend set to console (dev mode) - production needs SMTP
- Default superuser credentials in build.sh (should use env vars only)

#### 4. **Database Integrity**

✅ **All Models Validated:**
- Proper foreign key relationships
- Correct indexing on frequently queried fields
- Cascade deletes properly configured
- Unique constraints where needed
- Default values set appropriately

**Models Summary:**
```
Category (21 lines) ✅
Product (140 lines) ✅  
UserProfile (38 lines) ✅
Order (78 lines) ✅
OrderItem (16 lines) ✅
Review (18 lines) ✅
Wishlist (13 lines) ✅
ShippingRate (95 lines) ✅
ShippingZone (49 lines) ✅
PincodeZone (32 lines) ✅
```

---

## 🏗️ Application Architecture

### Directory Structure

```
fashion_store/                  # Root project directory
├── fashion_store/              # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Development settings
│   ├── production_settings.py  # Production settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
│
├── shop/                       # Main application
│   ├── models.py              # Database models (481 lines)
│   ├── views.py               # View logic (996 lines)
│   ├── urls.py                # URL routing (65 lines)
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin customization (588 lines)
│   ├── cart.py                # Shopping cart logic (162 lines)
│   ├── currency.py            # Multi-currency support
│   ├── context_processors.py  # Template context
│   ├── signals.py             # Django signals
│   ├── sitemaps.py            # SEO sitemaps
│   ├── utility_views.py       # Utility endpoints
│   ├── management/
│   │   └── commands/          # Custom Django commands
│   │       ├── add_product.py
│   │       ├── create_sample_data.py
│   │       ├── import_products.py
│   │       ├── setup_shipping.py
│   │       ├── setup_zone_shipping.py
│   │       ├── setup_international_shipping.py
│   │       ├── setup_international_pincodes.py
│   │       ├── setup_social_auth.py
│   │       └── update_inventory.py
│   ├── migrations/            # Database migrations
│   └── templatetags/          # Custom template tags
│       └── currency_tags.py
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── 403.html, 404.html, 500.html
│   ├── account/               # Authentication templates
│   ├── shop/                  # Shop templates
│   └── registration/          # Legacy auth templates
│
├── static/                     # Static files
│   ├── images/
│   ├── manifest.json
│   └── robots.txt
│
├── media/                      # User uploaded files
│   ├── products/
│   └── categories/
│
├── Scripts & Configuration
│   ├── manage.py              # Django management
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Docker configuration
│   ├── render.yaml            # Render deployment config
│   ├── build.sh               # Build script
│   ├── start.sh               # Startup script
│   ├── deploy_to_render.sh    # Deployment script
│   └── show_deployment_info.sh
│
└── Documentation
    ├── README.md
    ├── RENDER_DEPLOYMENT.md
    ├── SHIPPING_GUIDE.md
    ├── WEIGHT_BASED_SHIPPING_GUIDE.md
    ├── PINCODE_SHIPPING_GUIDE.md
    ├── PRODUCT_MANAGEMENT_GUIDE.md
    ├── SOCIAL_AUTH_GUIDE.md
    ├── MODERN_AUTH_GUIDE.md
    ├── LUXURY_TRANSFORMATION_GUIDE.md
    ├── ERROR_PAGES_GUIDE.md
    └── PROJECT_DOCUMENTATION.md (this file)
```

### Architecture Patterns

**1. MVT Pattern (Model-View-Template)**
- Models: Data layer (`shop/models.py`)
- Views: Business logic (`shop/views.py`)
- Templates: Presentation layer (`templates/`)

**2. Class-Based Views (CBV)**
All views use Django's CBV pattern:
- ListView: Product listings, orders
- DetailView: Product details, order details
- TemplateView: Static pages
- View: Custom logic (cart, payment)

**3. Session-Based Cart**
- No database storage for cart
- Stored in Django sessions
- Persists across page loads
- Converts to Order on checkout

**4. Multi-Currency Architecture**
- Base currency: INR
- Conversion via currency.py
- Session-based currency selection
- Template tag for display

---

## 💾 Database Models

### Entity Relationship Diagram

```
User (Django Auth)
  |
  ├─── UserProfile (1:1)
  ├─── Order (1:N)
  │      └─── OrderItem (1:N) ──> Product
  ├─── Review (1:N) ──> Product
  └─── Wishlist (1:N) ──> Product

Category (1:N) ──> Product

ShippingZone (1:N) ──> PincodeZone
ShippingRate (standalone)
```

### Model Details

#### 1. **Category**
```python
Fields:
  - name: CharField (max_length=200, unique)
  - slug: SlugField (unique, URL-friendly)
  - description: TextField
  - image: ImageField
  - created_at, updated_at: DateTimeField

Relationships:
  - products: Reverse FK to Product (1:N)

Methods:
  - __str__(): Returns category name
  - get_absolute_url(): URL for category page
```

#### 2. **Product** (Main model)
```python
Fields:
  Basic:
    - name, slug, description
    - price: DecimalField (max_digits=10, decimal_places=2)
    - stock: PositiveIntegerField
    - available: BooleanField
    - weight_kg: DecimalField (for shipping)
  
  Fashion-specific:
    - size: CharField (XS, S, M, L, XL, XXL)
    - color: CharField (12 color choices)
    - material, brand: CharField
  
  Images:
    - image, image_2, image_3: ImageField
  
  SEO:
    - meta_description, meta_keywords
  
  Timestamps:
    - created_at, updated_at

Relationships:
  - category: ForeignKey to Category
  - reviews: Reverse FK (1:N)
  - wishlist: Reverse FK (1:N)
  - orderitems: Reverse FK (1:N)

Methods:
  - save(): Auto-resizes images to 800x800
  - is_in_stock(): Checks availability
  - get_main_image_url(): Returns image URL
  - resize_image(): Helper for image resizing
```

#### 3. **UserProfile**
```python
Fields:
  - user: OneToOneField to User
  - phone, address_line_1, address_line_2
  - city, state, postal_code, country
  - date_of_birth: DateField
  - created_at, updated_at

Methods:
  - get_full_address(): Returns formatted address
```

#### 4. **Order**
```python
Fields:
  - order_number: CharField (unique, auto-generated)
  - user: ForeignKey to User
  
  Billing:
    - first_name, last_name, email, phone
  
  Shipping:
    - address_line_1, address_line_2
    - city, state, postal_code, country
  
  Financial:
    - total_amount, shipping_cost, tax_amount
  
  Status:
    - status: (pending, processing, shipped, delivered, cancelled, refunded)
    - payment_status: (pending, paid, failed, refunded)
    - payment_method: (razorpay, paypal)
    - payment_id: Gateway transaction ID
  
  Timestamps:
    - created_at, updated_at, shipped_at, delivered_at

Relationships:
  - items: Reverse FK to OrderItem (1:N)

Methods:
  - save(): Auto-generates order_number (FS + 8 hex chars)
  - get_total_cost(): Returns total with shipping and tax
  - get_absolute_url(): URL for order detail
```

#### 5. **OrderItem**
```python
Fields:
  - order: ForeignKey to Order
  - product: ForeignKey to Product
  - price: DecimalField (snapshot at purchase time)
  - quantity: PositiveIntegerField

Methods:
  - get_cost(): Returns price * quantity
```

#### 6. **Review**
```python
Fields:
  - product: ForeignKey to Product
  - user: ForeignKey to User
  - rating: IntegerField (1-5)
  - title, comment
  - created_at, updated_at

Constraints:
  - unique_together: ['product', 'user']
    (One review per user per product)
```

#### 7. **Wishlist**
```python
Fields:
  - user: ForeignKey to User
  - product: ForeignKey to Product
  - created_at

Constraints:
  - unique_together: ['user', 'product']
```

#### 8. **ShippingRate** (Country-based weight pricing)
```python
Fields:
  - name, description
  - min_order_value, max_order_value
  - cost: DecimalField (₹/kg)
  - min_shipping_charge
  - free_shipping_threshold
  - country: CharField (India, USA, etc.)
  - is_active, priority

Methods:
  - calculate_shipping_cost(cart_total, country, pincode, total_weight_kg):
    Complex multi-step calculation:
    1. Detect country from pincode if provided
    2. Use zone-based pricing for India with pincode
    3. Use country-based weight pricing
    4. Fallback to default rate
```

#### 9. **ShippingZone** (India zone-based)
```python
Fields:
  - zone: CharField (north, south, east, west, central)
  - description
  - cost_per_kg: DecimalField
  - free_shipping_threshold
  - delivery_days
  - is_active

Methods:
  - get_rate_for_pincode(pincode, cart_total, total_weight_kg):
    Returns shipping cost based on zone
```

#### 10. **PincodeZone** (Pincode mapping)
```python
Fields:
  - pincode: CharField (unique, indexed)
  - zone: ForeignKey to ShippingZone (nullable)
  - city, state, country
  - created_at, updated_at

Methods:
  - get_country_from_pincode(pincode):
    Static method to detect country
```

---

## 🔄 Workflow Documentation

### 1. **User Registration & Authentication Flow**

```
┌─────────────────────────────────────────────────────────┐
│                  User Registration                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  1. User accesses /accounts/signup/                      │
│  2. Fills form (email, password)                         │
│  3. Django Allauth validates                             │
│  4. Creates User object                                  │
│  5. Signal creates UserProfile (via signals.py)          │
│  6. Sends verification email (optional)                  │
│  7. Redirects to home page                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Social Authentication                       │
│  • Google OAuth 2.0                                      │
│  • Facebook OAuth                                        │
│  • Configured via django-allauth                         │
│  • Auto-creates UserProfile                              │
└─────────────────────────────────────────────────────────┘
```

### 2. **Shopping & Checkout Flow**

```
User Journey:
════════════

┌──────────────┐
│ Browse Store │ ──> ProductListView / CategoryDetailView
└──────────────┘
       │
       ▼
┌──────────────┐
│ View Product │ ──> ProductDetailView
└──────────────┘     - Shows images, details, reviews
       │             - Add to cart/wishlist buttons
       ▼
┌──────────────┐
│ Add to Cart  │ ──> CartAddView
└──────────────┘     - Session-based cart (cart.py)
       │             - No database storage
       │             - AJAX update (optional)
       ▼
┌──────────────┐
│  View Cart   │ ──> CartDetailView
└──────────────┘     - Update quantities
       │             - Remove items
       │             - Calculate shipping (AJAX)
       ▼
┌──────────────┐
│   Checkout   │ ──> CheckoutView (LoginRequired)
└──────────────┘     - Pre-fill from UserProfile
       │             - Validate shipping address
       │             - Calculate shipping cost
       ▼
┌──────────────┐
│ Create Order │ ──> OrderCreateView
└──────────────┘     - Creates Order object
       │             - Creates OrderItem objects
       │             - Clears cart
       │             - Status: 'pending'
       ▼
┌──────────────┐
│ Select Pay   │ ──> Razorpay or PayPal
└──────────────┘
       │
       ├──> Razorpay ──> RazorpayPaymentView
       │                 - Creates razorpay order
       │                 - Shows payment modal
       │                 - razorpay_verify() callback
       │                 - Updates payment_status to 'paid'
       │
       └──> PayPal ──> PayPalPaymentView
                        - Creates PayPal payment
                        - Redirects to PayPal
                        - PayPalReturnView callback
                        - Updates payment_status to 'paid'
       │
       ▼
┌──────────────┐
│Payment Success│──> PaymentSuccessView
└──────────────┘     - Shows order confirmation
       │             - Sends email (if configured)
       │             - User can view order details
       ▼
┌──────────────┐
│Order Tracking│──> OrderDetailView / OrderHistoryView
└──────────────┘     - View all orders
                     - Track order status
```

### 3. **Shipping Calculation Flow**

```python
"""
Multi-tiered shipping calculation logic
"""

def calculate_shipping(cart_total, country, pincode, total_weight_kg):
    """
    STEP 1: Country Detection
    ──────────────────────────
    if pincode provided:
        country = PincodeZone.get_country_from_pincode(pincode)
    
    STEP 2: India Zone-Based Pricing (if India + pincode)
    ─────────────────────────────────────────────────────
    if country == 'India' and pincode:
        zone_rate = ShippingZone.get_rate_for_pincode(...)
        if zone_rate:
            return zone_rate
    
    STEP 3: Country-Based Weight Pricing
    ────────────────────────────────────
    rates = ShippingRate.objects.filter(
        country=country,
        is_active=True,
        min_order_value <= cart_total
    )
    
    for rate in rates:
        if cart_total within range:
            shipping = rate.cost_per_kg × total_weight_kg
            if shipping < rate.min_shipping_charge:
                shipping = rate.min_shipping_charge
            return shipping
    
    STEP 4: Fallback Default
    ────────────────────────
    return 50 × total_weight_kg (min: ₹100)
    """
```

### 4. **Admin Workflow**

```
Admin Dashboard: /admin/

┌─────────────────────────────────────────────────────────┐
│                    Product Management                    │
├─────────────────────────────────────────────────────────┤
│ • Add/Edit/Delete products                               │
│ • Bulk import via CSV (import_products.py)               │
│ • Auto image resizing (800×800)                          │
│ • Set stock levels                                       │
│ • Manage categories                                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     Order Management                     │
├─────────────────────────────────────────────────────────┤
│ • View all orders with inline items                      │
│ • Update order status (pending → shipped → delivered)    │
│ • Track payments                                         │
│ • View customer details                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Shipping Configuration                 │
├─────────────────────────────────────────────────────────┤
│ • ShippingRate: Country-based rates                      │
│ • ShippingZone: India zone configuration                 │
│ • PincodeZone: Import via Excel                          │
│   - Custom admin actions                                 │
│   - Bulk import with openpyxl                            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                     User Management                      │
├─────────────────────────────────────────────────────────┤
│ • View users with inline profiles                        │
│ • Manage permissions                                     │
│ • View order history                                     │
└─────────────────────────────────────────────────────────┘
```

---

## 📜 Scripts Reference

### Deployment Scripts

#### 1. **build.sh** - Render Build Script
**Location:** `/home/coder/fashion_store/build.sh`

**Purpose:** Prepares the application for deployment on Render.com

**What it does:**
```bash
1. Installs Python dependencies from requirements.txt
2. Collects static files (Django collectstatic)
3. Runs database migrations
4. Creates superuser (if none exists)
   - Username: admin (or from DJANGO_SUPERUSER_USERNAME env var)
   - Email: admin@fashionstore.com (or from DJANGO_SUPERUSER_EMAIL)
   - Password: admin123 (or from DJANGO_SUPERUSER_PASSWORD)
```

**Usage:**
```bash
./build.sh
```

**Environment Variables:**
- `DJANGO_SUPERUSER_USERNAME` (optional)
- `DJANGO_SUPERUSER_EMAIL` (optional)
- `DJANGO_SUPERUSER_PASSWORD` (optional)

**Settings Used:** `fashion_store.production_settings`

---

#### 2. **start.sh** - Render Start Script
**Location:** `/home/coder/fashion_store/start.sh`

**Purpose:** Starts the Gunicorn server on Render.com

**What it does:**
```bash
Launches Gunicorn with:
  - Bind: 0.0.0.0:$PORT
  - Workers: 2
  - Worker class: gthread
  - Worker connections: 1000
  - Max requests: 1000
  - Request jitter: 100
  - Timeout: 30s
  - Keep-alive: 2s
  - Log level: info
  - Logs to stdout/stderr
```

**Usage:**
```bash
./start.sh
```

**Environment Variables:**
- `PORT` (provided by Render)

---

#### 3. **deploy_to_render.sh** - Quick Deploy Script
**Location:** `/home/coder/fashion_store/deploy_to_render.sh`

**Purpose:** Automates git push to trigger Render deployment

**What it does:**
```bash
1. Checks if git repository exists
2. Commits any uncommitted changes
3. Pushes to GitHub (main branch)
4. Triggers automatic Render deployment
```

**Usage:**
```bash
./deploy_to_render.sh
```

**Prompts for:** Commit message (optional)

**Prerequisites:**
- Git repository initialized
- Remote origin configured
- GitHub repository connected to Render

---

#### 4. **show_deployment_info.sh** - Deployment Info
**Location:** `/home/coder/fashion_store/show_deployment_info.sh`

**Purpose:** Displays deployment information and status

---

### Django Management Commands

#### 5. **create_sample_data.py**
**Location:** `shop/management/commands/create_sample_data.py`

**Purpose:** Populates database with sample products and categories

**Usage:**
```bash
python manage.py create_sample_data
python manage.py create_sample_data --clear  # Clear existing data first
```

**Creates:**
- Categories: Women's Clothing, Men's Clothing, Footwear, Accessories, Jewellery
- ~50 sample products per category
- Random prices (₹500-₹5000)
- Random colors, sizes, materials
- Random stock levels (10-100)

---

#### 6. **add_product.py**
**Location:** `shop/management/commands/add_product.py`

**Purpose:** Adds a single product via command line

**Usage:**
```bash
python manage.py add_product \
  --name "Designer Saree" \
  --category "Women's Clothing" \
  --price 2999 \
  --stock 50 \
  --weight 0.5 \
  --description "Beautiful designer saree"
```

**Arguments:**
- `--name`: Product name (required)
- `--category`: Category name (required)
- `--price`: Price in ₹ (required)
- `--stock`: Stock quantity (default: 10)
- `--weight`: Weight in kg (default: 0.1)
- `--description`: Product description
- `--size`: Size (XS/S/M/L/XL/XXL)
- `--color`: Color name

---

#### 7. **import_products.py**
**Location:** `shop/management/commands/import_products.py`

**Purpose:** Bulk import products from CSV file

**Usage:**
```bash
python manage.py import_products sample_products.csv
```

**CSV Format:**
```csv
name,category,price,stock,description,size,color,material,brand,weight_kg
Designer Saree,Women's Clothing,2999,50,Beautiful saree,M,red,Silk,BrandA,0.5
```

**Features:**
- Auto-creates categories if they don't exist
- Auto-generates slugs
- Validates data
- Reports errors

---

#### 8. **setup_shipping.py**
**Location:** `shop/management/commands/setup_shipping.py`

**Purpose:** Sets up basic shipping rates

**Usage:**
```bash
python manage.py setup_shipping
```

**Creates:**
- Standard shipping rate
- Express shipping rate
- International shipping rates

---

#### 9. **setup_zone_shipping.py**
**Location:** `shop/management/commands/setup_zone_shipping.py`

**Purpose:** Sets up India zone-based shipping

**Usage:**
```bash
python manage.py setup_zone_shipping
```

**Creates:**
- 5 zones: North, South, East, West, Central India
- Different rates per zone
- Sample pincodes for each zone

---

#### 10. **setup_international_shipping.py**
**Location:** `shop/management/commands/setup_international_shipping.py`

**Purpose:** Sets up international country shipping rates

**Usage:**
```bash
python manage.py setup_international_shipping
```

**Creates shipping rates for:**
- USA
- UK
- Canada
- Australia
- UAE
- Singapore
- European countries

---

#### 11. **setup_international_pincodes.py**
**Location:** `shop/management/commands/setup_international_pincodes.py`

**Purpose:** Sets up international postal codes in PincodeZone

**Usage:**
```bash
python manage.py setup_international_pincodes
```

**Creates postal code mappings for:**
- USA ZIP codes
- UK postcodes
- Canadian postal codes
- Australian postcodes

---

#### 12. **setup_social_auth.py**
**Location:** `shop/management/commands/setup_social_auth.py`

**Purpose:** Configures social authentication providers

**Usage:**
```bash
python manage.py setup_social_auth
```

**Sets up:**
- Google OAuth provider
- Facebook OAuth provider
- Creates Site objects

---

#### 13. **update_inventory.py**
**Location:** `shop/management/commands/update_inventory.py`

**Purpose:** Updates product stock levels

**Usage:**
```bash
python manage.py update_inventory <product_id> <new_stock>
```

---

### Configuration Files

#### 14. **Dockerfile**
**Location:** `/home/coder/fashion_store/Dockerfile`

**Purpose:** Docker containerization configuration

**Base Image:** python:3.11-slim

**What it does:**
1. Installs system dependencies (PostgreSQL client, image libraries)
2. Installs Python dependencies
3. Copies project files
4. Collects static files
5. Creates non-root user 'appuser'
6. Exposes port 8000
7. Runs Gunicorn

**Build:**
```bash
docker build -t fashion-store .
```

**Run:**
```bash
docker run -p 8000:8000 fashion-store
```

---

#### 15. **render.yaml**
**Location:** `/home/coder/fashion_store/render.yaml`

**Purpose:** Infrastructure as Code for Render.com

**Defines:**
```yaml
Web Service:
  - Type: web
  - Runtime: python3
  - Build: ./build.sh
  - Start: ./start.sh
  - Plan: free
  - Persistent disk: 1GB for media files

Database:
  - Type: PostgreSQL
  - Name: fashion-store-db
  - Plan: free
```

**Environment Variables:**
- `DJANGO_SETTINGS_MODULE=fashion_store.production_settings`
- `SECRET_KEY` (auto-generated)
- `DEBUG=False`

---

#### 16. **requirements.txt**
**Location:** `/home/coder/fashion_store/requirements.txt`

**Purpose:** Python dependencies specification

**Key Dependencies:**
```
Django==4.2.7               # Web framework
pillow==10.1.0              # Image processing
psycopg2-binary==2.9.9      # PostgreSQL adapter
python-decouple==3.8        # Environment variables
razorpay==1.4.2             # Razorpay payment
paypalrestsdk==1.13.3       # PayPal payment
gunicorn==21.2.0            # WSGI server
whitenoise==6.6.0           # Static files
django-allauth==0.57.0      # Authentication ⚠️ (duplicated)
openpyxl==3.1.2             # Excel import
dj-database-url==2.1.0      # Database URL parsing
```

---

### Task Automation (tasks.json)

#### Task 1: Build
```json
{
  "label": "Build",
  "type": "shell",
  "command": "make run",
  "group": {"kind": "build", "isDefault": true}
}
```

#### Task 2 & 3: Alembic Upgrade
```json
{
  "label": "Alembic Upgrade 1",
  "type": "shell",
  "command": "poetry run alembic upgrade head"
}
```
**Note:** These tasks reference Alembic (SQLAlchemy migrations), but the project uses Django migrations. This appears to be legacy/incorrect configuration.

#### Task 4: Run Both Upgrades
```json
{
  "label": "Run Both Upgrades",
  "dependsOn": ["Alembic Upgrade 1", "Alembic Upgrade 2"],
  "dependsOrder": "parallel"
}
```

**⚠️ Issue:** Alembic is not used in this Django project. These tasks should be replaced with Django migration tasks:

**Recommended tasks.json:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Development Server",
      "type": "shell",
      "command": "python manage.py runserver",
      "group": {"kind": "build", "isDefault": true}
    },
    {
      "label": "Make Migrations",
      "type": "shell",
      "command": "python manage.py makemigrations"
    },
    {
      "label": "Migrate Database",
      "type": "shell",
      "command": "python manage.py migrate"
    },
    {
      "label": "Create Superuser",
      "type": "shell",
      "command": "python manage.py createsuperuser"
    },
    {
      "label": "Load Sample Data",
      "type": "shell",
      "command": "python manage.py create_sample_data"
    }
  ]
}
```

---

## 🌐 API Endpoints

### Public Endpoints (No Authentication Required)

```
GET  /                              # Home page (PremiumHomeView)
GET  /products/                     # Product list (ProductListView)
GET  /products/page/<int>/          # Paginated product list
GET  /product/<slug>/               # Product detail (ProductDetailView)
GET  /category/<slug>/              # Category products (CategoryDetailView)
GET  /search/                       # Product search (ProductSearchView)

# Authentication (django-allauth)
GET  /accounts/signup/              # User registration
GET  /accounts/login/               # User login
POST /accounts/logout/              # User logout
GET  /accounts/password/reset/      # Password reset
GET  /accounts/social/login/google/ # Google OAuth
GET  /accounts/social/login/facebook/ # Facebook OAuth

# SEO
GET  /sitemap.xml                   # XML sitemap
GET  /robots.txt                    # Robots.txt
GET  /favicon.ico                   # Favicon
GET  /manifest.json                 # PWA manifest
```

### Authenticated Endpoints (Login Required)

```
# User Profile
GET  /profile/                      # View profile (ProfileView)
GET  /profile/edit/                 # Edit profile (ProfileEditView)
POST /profile/edit/                 # Save profile

# Shopping Cart (Session-based, no auth required but recommended)
GET  /cart/                         # View cart (CartDetailView)
POST /cart/add/<product_id>/        # Add to cart (CartAddView)
POST /cart/remove/<product_id>/     # Remove from cart (CartRemoveView)
POST /cart/update/<product_id>/     # Update quantity (CartUpdateView)
POST /cart/clear/                   # Clear cart (CartClearView)

# Checkout & Orders
GET  /checkout/                     # Checkout page (CheckoutView)
POST /order/create/                 # Create order (OrderCreateView)
GET  /order/<order_number>/         # Order detail (OrderDetailView)
GET  /orders/                       # Order history (OrderHistoryView)

# Payment Processing
GET  /payment/razorpay/<order_number>/  # Razorpay payment page
POST /payment/razorpay/verify/          # Razorpay webhook/verify
GET  /payment/paypal/<order_number>/    # PayPal payment initiation
GET  /payment/paypal/return/            # PayPal return URL
GET  /payment/paypal/cancel/            # PayPal cancel URL
GET  /payment/success/<order_number>/   # Payment success page
GET  /payment/failed/                   # Payment failed page

# Wishlist
GET  /wishlist/                     # View wishlist (WishlistView)
POST /wishlist/add/<product_id>/    # Add to wishlist (WishlistAddView)
POST /wishlist/remove/<product_id>/ # Remove from wishlist (WishlistRemoveView)

# Reviews
POST /product/<slug>/review/        # Add product review (ProductReviewView)

# Utility
POST /currency/switch/              # Switch currency (CurrencySwitchView)
POST /ajax/calculate-shipping/      # Calculate shipping cost (AJAX)
```

### Admin Endpoints

```
GET  /admin/                        # Django admin dashboard
GET  /admin/shop/product/           # Product management
GET  /admin/shop/category/          # Category management
GET  /admin/shop/order/             # Order management
GET  /admin/shop/shippingrate/      # Shipping rates
GET  /admin/shop/shippingzone/      # Shipping zones
GET  /admin/shop/pincodezone/       # Pincode management
     + Custom action: Import from Excel
GET  /admin/auth/user/              # User management
```

---

## ⚙️ Configuration Files

### 1. **settings.py** (Development)

```python
Key Settings:
  DEBUG = True
  ALLOWED_HOSTS = ['localhost', '127.0.0.1']
  
  DATABASES = SQLite (db.sqlite3)
  
  INSTALLED_APPS:
    - Django core apps
    - django.contrib.sites
    - django.contrib.sitemaps
    - allauth + social providers
    - shop (main app)
  
  MIDDLEWARE:
    - SecurityMiddleware
    - SessionMiddleware
    - AuthenticationMiddleware
    - AccountMiddleware (allauth)
  
  AUTHENTICATION_BACKENDS:
    - ModelBackend (Django)
    - AuthenticationBackend (allauth)
  
  ALLAUTH CONFIG:
    - Email authentication
    - Optional email verification
    - Social account auto-signup
    - Google & Facebook providers
  
  PAYMENT GATEWAYS:
    - RAZORPAY_KEY_ID (from env)
    - RAZORPAY_KEY_SECRET (from env)
    - PAYPAL_CLIENT_ID (from env)
    - PAYPAL_CLIENT_SECRET (from env)
    - PAYPAL_MODE = 'sandbox'
  
  SESSION:
    - SESSION_COOKIE_AGE = 7 days
    - SESSION_SAVE_EVERY_REQUEST = True
  
  EMAIL:
    - EMAIL_BACKEND = console (development)
  
  STATIC/MEDIA:
    - STATIC_URL = '/static/'
    - MEDIA_URL = '/media/'
    - STATIC_ROOT = staticfiles/
    - MEDIA_ROOT = media/
```

### 2. **production_settings.py** (Production)

```python
Inherits from settings.py, overrides:

  DEBUG = False
  
  ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.render.com',
    '.onrender.com'
  ]
  
  DATABASES = PostgreSQL (via DATABASE_URL env var)
    - Parsed by dj-database-url
    - Connection pooling enabled
  
  MIDDLEWARE:
    + WhiteNoiseMiddleware (position 1)
  
  STATICFILES_STORAGE:
    - CompressedManifestStaticFilesStorage
  
  SECURITY:
    - SESSION_COOKIE_SECURE = True
    - CSRF_COOKIE_SECURE = True
    - SECURE_BROWSER_XSS_FILTER = True
    - SECURE_CONTENT_TYPE_NOSNIFF = True
    - X_FRAME_OPTIONS = 'DENY'
```

### 3. **urls.py** (Main URL Configuration)

```python
URL Patterns:
  /admin/                   # Django admin
  /                         # Shop app (includes shop.urls)
  /accounts/                # Allauth URLs
  /sitemap.xml              # SEO sitemap
  /robots.txt               # Robots file
  /favicon.ico              # Favicon
  /manifest.json            # PWA manifest
  /.well-known/security.txt # Security contact
  
Media serving (DEBUG mode only):
  /media/<path>             # User uploads
  /static/<path>            # Static files
```

### 4. **wsgi.py** & **asgi.py**

```python
# wsgi.py - WSGI application
WSGI_APPLICATION = 'fashion_store.wsgi.application'

# asgi.py - ASGI application (async support)
ASGI_APPLICATION = 'fashion_store.asgi.application'
```

---

## 🚀 Deployment Guide

### Local Development

```bash
# 1. Clone repository
git clone <repo-url>
cd fashion_store

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
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

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Load sample data (optional)
python manage.py create_sample_data

# 8. Run server
python manage.py runserver

# Access at: http://localhost:8000
# Admin at: http://localhost:8000/admin
```

### Render.com Deployment

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin <github-repo-url>
git push -u origin main

# 2. Create Render Web Service
- Go to dashboard.render.com
- New > Web Service
- Connect GitHub repository
- Configure:
  * Name: fashion-store
  * Environment: Python 3
  * Build Command: ./build.sh
  * Start Command: ./start.sh
  
# 3. Add Environment Variables
SECRET_KEY=<generate-random-key>
DEBUG=False
RAZORPAY_KEY_ID=<production-key>
RAZORPAY_KEY_SECRET=<production-secret>
PAYPAL_CLIENT_ID=<production-id>
PAYPAL_CLIENT_SECRET=<production-secret>
PAYPAL_MODE=live

# 4. Create PostgreSQL Database
- New > PostgreSQL
- Name: fashion-store-db
- Copy DATABASE_URL
- Add to web service env vars

# 5. Deploy
- Click "Create Web Service"
- Render will build and deploy automatically

# 6. Quick redeploy
./deploy_to_render.sh
```

### Docker Deployment

```bash
# Build image
docker build -t fashion-store .

# Run container
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret \
  -e DEBUG=False \
  -e DATABASE_URL=postgres://... \
  --name fashion-store \
  fashion-store

# Access at: http://localhost:8000
```

---

## ⚠️ Issues & Recommendations

### Critical Issues

#### 1. **Duplicate Dependency**
- **File:** `requirements.txt`
- **Issue:** `django-allauth==0.57.0` appears twice (lines 13 and 21)
- **Fix:** Remove line 21
- **Impact:** Low (pip handles it, but poor practice)

#### 2. **Incorrect Task Configuration**
- **File:** `.vscode/tasks.json` (implied from task data)
- **Issue:** Alembic tasks defined, but project uses Django migrations
- **Fix:** Replace with Django migration tasks
- **Impact:** Medium (tasks won't work)

### Medium Priority Issues

#### 3. **Missing CART_SESSION_ID Setting**
- **File:** `shop/cart.py`
- **Issue:** Falls back to 'cart' if not in settings
- **Fix:** Add `CART_SESSION_ID = 'cart'` to `settings.py`
- **Impact:** Low (works but not explicit)

#### 4. **Free Shipping Disabled**
- **File:** `shop/models.py` lines 372-374
- **Issue:** Free shipping code commented out
- **Fix:** Document or enable feature
- **Impact:** Medium (business decision)

#### 5. **Payment Method Missing COD**
- **File:** `shop/models.py` line 213
- **Issue:** README mentions COD, but not in PAYMENT_METHOD_CHOICES
- **Fix:** Add ('cod', 'Cash on Delivery') or update README
- **Impact:** Medium (feature inconsistency)

#### 6. **Default Superuser Credentials**
- **File:** `build.sh`
- **Issue:** Hardcoded default credentials (admin/admin123)
- **Fix:** Require env vars, no defaults
- **Impact:** High (security in production)

### Low Priority Issues

#### 7. **Email Backend**
- **File:** `settings.py`
- **Issue:** Console backend (dev only)
- **Fix:** Configure SMTP for production
- **Impact:** Low (documented in settings)

#### 8. **No Image Placeholder**
- **File:** `shop/models.py` line 158
- **Issue:** References `/static/images/no-image.jpg` (doesn't exist)
- **Fix:** Add placeholder image or handle missing images
- **Impact:** Low (UI glitch for products without images)

### Recommendations

#### Code Quality
1. **Add type hints** to Python functions
2. **Add docstrings** to all classes and methods
3. **Add unit tests** (currently no tests/)
4. **Add integration tests** for payment flows
5. **Add logging** throughout application
6. **Add error monitoring** (e.g., Sentry)

#### Security
1. **Rate limiting** on login/signup endpoints
2. **CAPTCHA** on forms (prevent spam)
3. **Content Security Policy** (CSP headers)
4. **Regular security updates** (dependabot)
5. **Remove default superuser** creation in build.sh

#### Performance
1. **Add Redis caching** for sessions and queries
2. **Add CDN** for static files
3. **Optimize database queries** (select_related, prefetch_related)
4. **Add database indexes** on frequently queried fields
5. **Lazy load images** on product list pages

#### Features
1. **Add inventory alerts** (low stock notifications)
2. **Add product variants** (size/color combinations)
3. **Add order notes** for customers
4. **Add admin analytics dashboard**
5. **Add email notifications** for orders
6. **Add SMS notifications** via Twilio
7. **Add newsletter subscription**
8. **Add discount codes/coupons**
9. **Add customer loyalty program**
10. **Add multi-language support** (i18n)

#### Documentation
1. **API documentation** (Swagger/OpenAPI)
2. **Database schema diagram** (ERD)
3. **User manual** for customers
4. **Admin manual** for store operators
5. **Developer setup guide** (expanded)

---

## 📊 Project Statistics

```
Total Lines of Code: ~5,000+ (Python)
  - models.py: 481 lines
  - views.py: 996 lines
  - admin.py: 588 lines
  - cart.py: 162 lines
  - forms.py: ~200 lines
  - urls.py: 65 lines
  - management commands: ~1,000+ lines

Database Models: 10
  - Category, Product, UserProfile
  - Order, OrderItem
  - Review, Wishlist
  - ShippingRate, ShippingZone, PincodeZone

Views: 25+
  - Class-based views: 20+
  - Function-based views: 5+

URL Endpoints: 40+

Management Commands: 9

Templates: 20+

Static Files: Minimal (mostly Bootstrap CDN)

External Dependencies: 18
```

---

## 🎓 Learning Resources

### Django Documentation
- [Django 4.2 Docs](https://docs.djangoproject.com/en/4.2/)
- [Class-Based Views](https://docs.djangoproject.com/en/4.2/topics/class-based-views/)
- [Django ORM](https://docs.djangoproject.com/en/4.2/topics/db/)

### Payment Gateways
- [Razorpay Python SDK](https://razorpay.com/docs/payment-gateway/server-integration/python/)
- [PayPal REST API](https://developer.paypal.com/docs/api/overview/)

### Deployment
- [Render Django Deployment](https://render.com/docs/deploy-django)
- [Docker Django Tutorial](https://docs.docker.com/samples/django/)

### Authentication
- [Django Allauth Docs](https://django-allauth.readthedocs.io/)
- [OAuth 2.0 Guide](https://oauth.net/2/)

---

## 📝 Changelog

### Version 1.0 (Current)
- Initial release
- Complete e-commerce functionality
- Payment gateway integration
- Shipping calculation system
- Social authentication
- Multi-currency support
- Admin panel customization

### Planned Features (v1.1)
- [ ] Inventory alerts
- [ ] Email notifications
- [ ] Discount codes
- [ ] Product reviews moderation
- [ ] Advanced analytics
- [ ] Performance optimizations

---

## 👥 Contributors

This project documentation was created through comprehensive code analysis.

---

## 📄 License

This project is proprietary. All rights reserved to Sri Devi Fashion Jewellery.

---

## 📞 Support

For issues and questions:
- Email: support@sridevifashion.com (placeholder)
- Documentation: See individual guide files in project root

---

**End of Documentation**

*Generated: November 8, 2025*
*Project: Sri Devi Fashion Jewellery*
*Framework: Django 4.2.7*
