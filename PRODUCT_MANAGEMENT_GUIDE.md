# 🛍️ Product & Inventory Management Guide

## Overview
This guide shows you how to add products with photos and manage inventory in your Django Fashion Store.

## 🎯 Quick Start

### Option 1: Django Admin Interface (Recommended for Beginners)
1. **Access Admin**: Go to `http://localhost:8000/admin`
2. **Login**: Username: `test`, Password: `test`
3. **Add Products**: Navigate to `Shop` → `Products` → `Add Product`
4. **Upload Photos**: Use the image field to upload product photos
5. **Set Inventory**: Enter stock quantity and mark as available

### Option 2: Command Line (Single Product)
```bash
python manage.py add_product \
  --name "Product Name" \
  --description "Product description" \
  --price 29.99 \
  --category "Category Name" \
  --stock 50 \
  --size "M" \
  --color "blue" \
  --image-url "https://example.com/image.jpg"
```

### Option 3: Bulk Import from CSV
```bash
python manage.py import_products sample_products.csv
```

## 📝 CSV Format for Bulk Import
Create a CSV file with these columns:
```csv
name,description,price,category,stock,size,color,image_url
"Cotton T-Shirt","Soft cotton shirt",25.99,"Clothing",50,"M","blue","https://example.com/image.jpg"
"Running Shoes","Comfortable shoes",89.99,"Footwear",25,"9","white","https://example.com/shoes.jpg"
```

## 📊 Inventory Management

### Check Current Inventory
```bash
python manage.py update_inventory --list-products
```

### Update Stock for Specific Product
```bash
# Set exact stock amount
python manage.py update_inventory --product-id 1 --stock 100

# Add to existing stock
python manage.py update_inventory --product-id 1 --add-stock 25

# Subtract from existing stock
python manage.py update_inventory --product-id 1 --subtract-stock 10

# Find product by name
python manage.py update_inventory --product-name "T-Shirt" --stock 50
```

## 🖼️ Image Management

### Supported Image Sources
1. **Upload Files**: Use Django admin interface
2. **URL Download**: Provide image URL in commands
3. **Local Files**: Use `--image-path` parameter

### Image Requirements
- **Formats**: JPG, PNG, GIF
- **Size**: Recommended 400x400px or larger
- **Storage**: Images saved to `/media/products/`

## 📦 Product Attributes

### Required Fields
- **Name**: Product title
- **Price**: Decimal value (e.g., 29.99)
- **Category**: Product category
- **Stock**: Integer quantity

### Optional Fields
- **Description**: Product details
- **Size**: XS, S, M, L, XL, XXL
- **Color**: red, blue, green, black, white, etc.
- **Image**: Product photo

## 🏷️ Categories

### Default Categories
- Clothing
- Footwear
- Accessories
- Men's Clothing
- Women's Clothing
- Kids' Clothing

### Adding New Categories
Categories are automatically created when adding products, or manually via admin interface.

## 🚀 Production Tips

### Inventory Alerts
- Products with stock ≤ 5 are marked as "LOW"
- Products with stock = 0 are marked as "OUT"
- Use `--low-stock` parameter to customize threshold

### Bulk Operations
- Use CSV import for adding many products at once
- Include image URLs for automatic download
- Validate CSV format before importing

### Performance
- Optimize images before uploading
- Use appropriate image sizes (400-800px)
- Consider using CDN for production

## 🛠️ Troubleshooting

### Common Issues

**Image Download Fails**
- Check internet connection
- Verify image URL is accessible
- Use `--skip-images` flag for CSV import

**Product Not Found**
- Use `--list-products` to see all products
- Check product ID or name spelling
- Products are case-sensitive

**Stock Issues**
- Stock cannot go below 0
- Availability is automatically updated
- Check product status in admin

## 📈 Example Workflows

### Daily Inventory Check
```bash
python manage.py update_inventory --list-products --low-stock 10
```

### Restocking Popular Items
```bash
python manage.py update_inventory --product-name "T-Shirt" --add-stock 50
```

### Seasonal Inventory Update
```bash
python manage.py import_products winter_collection.csv
```

## 🔗 Quick Links
- **Admin Panel**: http://localhost:8000/admin
- **Store Front**: http://localhost:8000
- **Product List**: http://localhost:8000/products/
- **Categories**: http://localhost:8000/category/clothing/

## 📞 Support
For additional help, check the Django admin interface or refer to the application logs.