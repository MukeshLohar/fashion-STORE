# Shipping Charges Management Guide

## Overview
Your Sri Devi Fashion Jewellery store uses a **weight-based shipping system** for India with zone-based pricing. Shipping costs are calculated based on:
- Product weight in kilograms
- Customer's pincode (determines shipping zone)
- Order total (for free shipping eligibility)

## 🆕 Weight-Based Shipping (India)

### Current Zone Rates (Per Kilogram)

| Zone | Coverage | Rate | Free Above | Delivery |
|------|----------|------|------------|----------|
| **North** | Delhi, Punjab, Haryana, etc. | ₹40/kg | ₹500 | 3-5 days |
| **South** | Tamil Nadu, Karnataka, Kerala, etc. | ₹50/kg | ₹500 | 4-6 days |
| **East** | West Bengal, Bihar, Assam, etc. | ₹60/kg | ₹500 | 5-7 days |
| **West** | Maharashtra, Gujarat, Goa, etc. | ₹45/kg | ₹500 | 3-5 days |
| **Central** | MP, Chhattisgarh, UP | ₹45/kg | ₹500 | 4-6 days |

### Example Calculation
**Cart Items:**
- Jewelry Set (0.500 kg) × 2 = 1.000 kg
- Earrings (0.150 kg) × 1 = 0.150 kg
- **Total Weight**: 1.150 kg

**Customer in Mumbai (West Zone):**
- Shipping: 1.150 kg × ₹45/kg = **₹51.75**
- If order > ₹500: **FREE SHIPPING**

## International Shipping (Flat Rates)

### USA
- **Orders under ₹3,000**: ₹200 shipping charge
- **Orders ₹3,000 and above**: FREE SHIPPING 🎉

### Other Countries
- **Orders under ₹5,000**: ₹250 shipping charge
- **Orders ₹5,000 and above**: FREE SHIPPING 🎉

## How It Works

### Automatic Calculation
The system automatically calculates shipping costs when:
1. Customer adds items to cart
2. Customer proceeds to checkout
3. Order is created

### Database Model
The `ShippingRate` model stores all shipping configurations with:
- **Name**: Display name for the shipping option
- **Country**: Applicable country
- **Min Order Value**: Minimum cart value for this rate
- **Max Order Value**: Maximum cart value (optional)
- **Cost**: Shipping charge amount
- **Free Shipping Threshold**: Amount above which shipping is free
- **Priority**: Lower number = higher priority (used when multiple rates match)

## Managing Shipping Rates

### Through Django Admin
1. Go to: `http://your-domain/admin/`
2. Navigate to: **Shop** > **Shipping Rates**
3. You can:
   - Add new shipping rates
   - Edit existing rates
   - Enable/disable rates
   - Change priority order

### Using Management Command

#### Set up default rates:
```bash
python manage.py setup_shipping
```

This creates the default shipping rates for India, USA, and Other countries.

### Import Shipping Rates via Excel (Recommended for Bulk Updates)

For adding multiple shipping rates for different countries at once:

1. **Access Import Feature:**
   - Go to Django Admin
   - Navigate to **Shop** > **Shipping Rates**
   - Click the **"Import from Excel"** button (top right)

2. **Download Sample Template:**
   - Click **"Download Sample Excel"** to get the template
   - The template includes example rates for India, USA, UK, and Australia

3. **Fill in Your Data:**
   
   Excel columns:
   - **Name**: Unique name (e.g., "Standard USA", "Express India")
   - **Description**: Details about the shipping method
   - **Country**: Country name (India, USA, UK, Australia, etc.)
   - **Cost**: Shipping charge in ₹
   - **Min Order Value**: Minimum cart value (usually 0)
   - **Max Order Value**: Maximum cart value (leave empty for no limit)
   - **Free Shipping Threshold**: Amount for free shipping (leave empty for none)
   - **Priority**: Lower number = higher priority (0 = highest)

4. **Example Excel Data:**
   ```
   Name              | Description              | Country   | Cost | Min Order | Max Order | Free Threshold | Priority
   Standard India    | Standard shipping        | India     | 50   | 0         |           | 500            | 1
   Express India     | 1-2 day delivery         | India     | 150  | 0         |           | 1000           | 2
   Standard USA      | International USA        | USA       | 200  | 0         |           | 3000           | 1
   Standard UK       | International UK         | UK        | 250  | 0         |           | 3000           | 1
   Standard Europe   | EU countries             | Germany   | 280  | 0         |           | 3500           | 1
   Standard Asia     | Asian countries          | Singapore | 180  | 0         |           | 2500           | 1
   ```

5. **Upload and Import:**
   - Save your Excel file
   - Upload it using the import form
   - System will create or update shipping rates automatically

### Tips for Excel Import:
- **Bulk Updates**: Update existing rates by using the same Name and Country
- **Multiple Countries**: Add rows for each country
- **Priority System**: Use 0 for express/premium, 1 for standard, 2 for economy
- **Free Shipping**: Leave threshold empty if you don't offer free shipping for that rate
- **Regional Rates**: Create specific rates for regions (e.g., "South India", "North USA")

## Customizing Shipping Rates

### Add a New Shipping Rate
1. Go to Django Admin
2. Click "Add Shipping Rate"
3. Fill in:
   - **Name**: e.g., "Express Shipping (India)"
   - **Description**: Details about delivery time
   - **Country**: Select country
   - **Min Order Value**: e.g., 0.00
   - **Max Order Value**: e.g., 999.99 (or leave empty)
   - **Cost**: e.g., 100.00
   - **Free Shipping Threshold**: e.g., 1000.00 (optional)
   - **Priority**: Lower = higher priority
   - **Is Active**: Check to enable

### Examples

#### Example 1: Express Shipping
```
Name: Express Shipping (1-2 days)
Country: India
Min Order Value: 0.00
Cost: 150.00
Free Shipping Threshold: 1000.00
Priority: 2
```

#### Example 2: Regional Shipping
```
Name: South India Shipping
Country: India
Min Order Value: 0.00
Cost: 30.00
Free Shipping Threshold: 300.00
Priority: 1
```

#### Example 3: Bulk Orders
```
Name: Bulk Order Discount
Country: India
Min Order Value: 5000.00
Cost: 0.00
Priority: 0
```

## Code Integration

### In Templates
The shipping cost is automatically displayed in:
- **Cart page**: Shows shipping cost and free shipping progress
- **Checkout page**: Shows final shipping cost in order summary

### In Views
The `Cart` class automatically calculates shipping:
```python
cart.get_shipping_cost()  # Returns shipping cost as Decimal
```

### In Models
Static method to calculate shipping:
```python
from shop.models import ShippingRate
cost = ShippingRate.calculate_shipping_cost(cart_total=500, country='India')
```

## Tips for Optimization

1. **Priority Matters**: Set lower priority for premium/special rates
2. **Free Shipping Strategy**: Use free shipping thresholds to increase average order value
3. **Regional Rates**: Create specific rates for different regions
4. **Testing**: Always test with different order values before going live

## Customer Experience

### Cart Page Shows:
- Current shipping cost (if any)
- "Add ₹X more for FREE shipping!" message
- Progress indicator (visual feedback)

### Checkout Page Shows:
- Final shipping cost
- Tax calculation (18% GST)
- Total amount including all charges

## Tax Configuration

Current tax rate: **18% GST** (Indian standard)

To modify tax rate, edit `shop/cart.py`:
```python
def get_tax_amount(self):
    return self.get_total_price() * Decimal('0.18')  # Change 0.18 to your rate
```

## Troubleshooting

### Issue: Shipping shows as ₹0 for all orders
**Solution**: Check if a shipping rate with priority 0 and min_order_value 0 exists. Deactivate or adjust it.

### Issue: Wrong shipping cost calculated
**Solution**: 
1. Check shipping rates in admin
2. Verify priority order
3. Check min/max order value ranges don't overlap incorrectly

### Issue: Free shipping not working
**Solution**: Verify `free_shipping_threshold` is set correctly and cart total meets the threshold.

## Future Enhancements

Consider adding:
- Shipping zones (pincode-based rates)
- Weight-based shipping
- Multiple shipping methods per order
- Real-time carrier API integration
- Shipping discounts/coupons
- Estimated delivery dates

## Support

For technical support or custom shipping requirements, contact your development team.

---

**Last Updated**: November 2025
**Version**: 1.0
