# Favicon Files - Instructions

The following favicon files are missing and need to be created:

## Required Files:

1. **favicon.ico** (16x16 and 32x32 multi-resolution ICO file)
2. **favicon-16x16.png** (16x16 PNG)
3. **favicon-32x32.png** (32x32 PNG)
4. **apple-touch-icon.png** (180x180 PNG)

## How to Create These Files:

### Option 1: Using an Online Tool (Easiest)
1. Go to: https://realfavicongenerator.net/
2. Upload your logo (at least 260x260px)
3. Download the generated favicon package
4. Extract and copy all files to `/home/coder/fashion_store/static/images/`

### Option 2: Using Canva
1. Go to: https://www.canva.com/
2. Create a square design (512x512px recommended)
3. Add your logo/brand icon
4. Download as PNG
5. Use an online converter to create ICO file

### Option 3: Manual Creation
If you have an existing logo file:
```bash
# Install ImageMagick (if not already installed)
sudo apt-get install imagemagick

# Convert logo to different sizes
convert logo.png -resize 16x16 favicon-16x16.png
convert logo.png -resize 32x32 favicon-32x32.png
convert logo.png -resize 180x180 apple-touch-icon.png
convert logo.png -resize 32x32 favicon.ico
```

## Temporary Workaround:
The current setup uses an icon.svg which works for modern browsers.
To remove the 404 errors, you can:

1. Comment out or update the favicon references in base.html
2. Or create simple placeholder icons

## Quick Fix - Remove 404 Errors:
Update base.html to use only the SVG icon by removing PNG references.
