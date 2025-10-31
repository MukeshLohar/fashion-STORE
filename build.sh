#!/usr/bin/env bash
# Render build script for Fashion Store

echo "🔨 Building Fashion Store for Render..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --settings=fashion_store.production_settings

# Run database migrations
python manage.py migrate --settings=fashion_store.production_settings

# Create superuser if it doesn't exist (optional)
echo "Creating superuser..."
python manage.py shell --settings=fashion_store.production_settings << 'PYEOF'
from django.contrib.auth import get_user_model
User = get_user_model()

# Only create superuser if none exists
if not User.objects.filter(is_superuser=True).exists():
    import os
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@fashionstore.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
    
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully!")
else:
    print("Superuser already exists. Skipping creation.")
PYEOF

echo "✅ Build completed successfully!"