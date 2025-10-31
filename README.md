# Fashion Store - Django E-commerce Website

A complete fashion e-commerce website built with Django, featuring user authentication, product catalog, shopping cart, payment processing (Razorpay UPI + PayPal), order management, and admin panel.

## 🚀 Features

### Core Functionality
- **User Authentication**: Registration, login, logout, password reset, user profiles
- **Product Catalog**: Browse products by category, search, filters, detailed product pages
- **Shopping Cart**: Session-based cart with add/update/remove functionality
- **Checkout & Orders**: Complete order processing with order history and tracking
- **Payment Integration**: 
  - Razorpay (UPI, Cards, Net Banking)
  - PayPal (International payments)
  - Cash on Delivery
- **Admin Panel**: Comprehensive Django admin for managing products, orders, and users

### Technical Features
- **Responsive Design**: Bootstrap 5 for mobile-friendly UI
- **Image Handling**: Automatic image resizing with Pillow
- **Security**: CSRF protection, secure payments, user authentication
- **Database**: SQLite for development, PostgreSQL-ready for production
- **SEO Ready**: Meta tags, clean URLs, structured data

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Local Development Setup

1. **Clone or download the project**
```bash
# If using git
git clone <repository-url>
cd fashion_store

# Or extract the downloaded folder and navigate to it
cd fashion_store
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
Create a `.env` file in the project root:
```env
SECRET_KEY=your-super-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - SQLite is default)
# DB_NAME=fashion_store
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432

# Payment Gateways (Use sandbox/test keys for development)
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_secret_key

PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox
```

5. **Database setup**
```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
```

6. **Load sample data (optional)**
```bash
python manage.py create_sample_data
```

7. **Run the development server**
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to view the website.
Admin panel: `http://localhost:8000/admin`

## 🎯 Usage Guide

### For Customers
1. **Browse Products**: Visit the homepage to see featured products and categories
2. **Search & Filter**: Use the search bar or category filters to find products
3. **Product Details**: Click on any product to view details, images, and reviews
4. **Add to Cart**: Add products to your cart and manage quantities
5. **Checkout**: Complete your purchase with multiple payment options
6. **Account Management**: Create an account to track orders and manage your profile

### For Administrators
1. **Access Admin Panel**: Visit `/admin` and login with superuser credentials
2. **Manage Products**: Add/edit products, categories, and inventory
3. **Process Orders**: View and update order status, track shipments
4. **User Management**: Manage customer accounts and profiles
5. **Analytics**: View sales data and customer insights

## 💳 Payment Configuration

### Razorpay Setup (UPI/Cards)
1. Sign up at [Razorpay](https://razorpay.com/)
2. Get your test API keys from the dashboard
3. Add keys to your `.env` file
4. For production, replace with live keys

### PayPal Setup
1. Create a developer account at [PayPal Developer](https://developer.paypal.com/)
2. Create a sandbox application
3. Get Client ID and Secret
4. Add credentials to `.env` file

## 🚀 Deployment

### Deploy to Heroku

1. **Install Heroku CLI** and login
```bash
heroku login
```

2. **Create Heroku app**
```bash
heroku create your-fashion-store
```

3. **Configure environment variables**
```bash
heroku config:set SECRET_KEY=your-production-secret-key
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
# Add other environment variables...
```

4. **Add PostgreSQL database**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

5. **Deploy**
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

6. **Run migrations**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Deploy to Render

1. **Create account** at [Render](https://render.com/)

2. **Create new Web Service**
   - Connect your repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `gunicorn fashion_store.wsgi:application`

3. **Add environment variables** in Render dashboard

4. **Add PostgreSQL database** and connect to your service

### Docker Deployment

1. **Build Docker image**
```bash
docker build -t fashion-store .
```

2. **Run container**
```bash
docker run -p 8000:8000 fashion-store
```

For production with PostgreSQL:
```bash
docker-compose up -d
```

## 📁 Project Structure

```
fashion_store/
├── fashion_store/          # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI application
├── shop/                  # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # App URLs
│   ├── forms.py           # Django forms
│   ├── admin.py           # Admin configuration
│   ├── cart.py            # Shopping cart logic
│   └── signals.py         # Django signals
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── shop/              # Shop templates
│   └── registration/      # Auth templates
├── static/                # Static files (CSS, JS, images)
├── media/                 # User uploaded files
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── README.md             # This file
```

## 🔧 Configuration

### Database Configuration
By default, the project uses SQLite for development. For production, configure PostgreSQL:

```python
# In settings.py, uncomment and configure:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### Email Configuration
For password reset functionality:
```python
# For production SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-host'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
```

## 🛡️ Security

The application includes several security features:
- CSRF protection on all forms
- User authentication for sensitive operations
- Secure payment processing with signature verification
- SQL injection protection through Django ORM
- XSS protection through template escaping
- HTTPS enforcement in production

## 🎨 Customization

### Adding New Product Fields
1. Update the `Product` model in `shop/models.py`
2. Create and run migrations
3. Update forms, views, and templates accordingly

### Styling Customization
- Modify the CSS in `templates/base.html`
- Add custom styles to the `static/` directory
- Customize Bootstrap variables for theme changes

### Payment Gateway Integration
- Implement new payment providers in `shop/views.py`
- Add corresponding URL patterns
- Create payment-specific templates

## 📱 API Endpoints

The application includes AJAX endpoints for:
- Adding items to cart: `POST /cart/add/<product_id>/`
- Updating cart: `POST /cart/update/<product_id>/`
- Removing from cart: `POST /cart/remove/<product_id>/`
- Wishlist management: `POST /wishlist/add/<product_id>/`

## 🐛 Troubleshooting

### Common Issues

1. **ImportError: No module named 'PIL'**
   ```bash
   pip install Pillow
   ```

2. **Database errors**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Static files not loading**
   ```bash
   python manage.py collectstatic
   ```

4. **Payment gateway errors**
   - Verify API keys in `.env` file
   - Check sandbox/production mode settings
   - Ensure webhook URLs are configured

### Development Tips

- Use `DEBUG=True` only in development
- Regularly backup your database
- Test payment flows with sandbox credentials
- Monitor application logs for errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Django framework for the robust foundation
- Bootstrap for responsive UI components
- Razorpay and PayPal for payment processing
- Pillow for image processing capabilities

## 📞 Support

For questions, issues, or support:
- Create an issue in the repository
- Check the Django documentation
- Review the payment gateway documentation

---

**Happy Coding! 🛍️👗**