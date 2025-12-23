# Weight-Based Shipping System Guide

## Overview
The Sri Devi Fashion Jewellery store uses a weight-based shipping calculation system. Shipping costs are calculated based on:
- **Product Weight**: Each product has a weight in kilograms
- **Shipping Zone**: India is divided into 5 zones with different per-kg rates
- **Pincode**: Customer's pincode determines their shipping zone

## Current Shipping Rates (Per Kilogram)

| Zone | States Covered | Rate (₹/kg) | Free Shipping Above | Delivery Time |
|------|---------------|-------------|---------------------|---------------|
| **North** | Delhi, Punjab, Haryana, HP, J&K, Uttarakhand, Chandigarh | ₹40/kg | ₹500 | 3-5 days |
| **South** | Tamil Nadu, Karnataka, Kerala, AP, Telangana, Puducherry | ₹50/kg | ₹500 | 4-6 days |
| **East** | West Bengal, Odisha, Bihar, Jharkhand, Assam, Sikkim, NE | ₹60/kg | ₹500 | 5-7 days |
| **West** | Maharashtra, Gujarat, Goa, Rajasthan, DNH, Daman & Diu | ₹45/kg | ₹500 | 3-5 days |
| **Central** | Madhya Pradesh, Chhattisgarh, Uttar Pradesh | ₹45/kg | ₹500 | 4-6 days |

## How It Works

### Example Calculation
If a customer orders:
- Product A: 0.500 kg (jewelry set) × 2 qty = 1.000 kg
- Product B: 0.250 kg (earrings) × 1 qty = 0.250 kg
- **Total Weight**: 1.250 kg

Customer is in Mumbai (West Zone, ₹45/kg):
- **Shipping Cost**: 1.250 kg × ₹45/kg = **₹56.25**

If order total is above ₹500, shipping is **FREE**!

## Admin Tasks

### 1. Adding Products with Weight

When adding a new product:
1. Go to **Admin > Products > Add Product**
2. Fill in all regular fields
3. In the **Shipping** section:
   - Enter weight in kilograms (e.g., `0.500` for 500g)
   - Default is 0.100 kg (100g) if not specified
4. Save the product

**Weight Guidelines:**
- Light jewelry (earrings, small pendants): 0.050 - 0.150 kg
- Medium jewelry (necklaces, bracelets): 0.150 - 0.500 kg
- Heavy jewelry (sets, heavy necklaces): 0.500 - 1.500 kg

### 2. Managing Shipping Zones

To update zone rates:
1. Go to **Admin > Shipping Zones**
2. Click on any zone to edit
3. Modify:
   - **Cost per kg**: Base rate per kilogram
   - **Free Shipping Threshold**: Order value for free shipping
   - **Delivery Days**: Estimated delivery time
4. Save changes

### 3. Managing Pincodes

#### Import Pincodes via Excel:
1. Go to **Admin > Pincode Zones**
2. Click **"Import from Excel"** button (top right)
3. Click **"Download Sample Excel"** to get template
4. Fill Excel with pincode data:
   ```
   Pincode | Zone      | City      | State
   110001  | north     | Delhi     | Delhi
   400001  | west      | Mumbai    | Maharashtra
   600001  | south     | Chennai   | Tamil Nadu
   ```
5. Upload the filled Excel file
6. Click **"Import"**

#### Add Individual Pincode:
1. Go to **Admin > Pincode Zones > Add Pincode Zone**
2. Enter pincode, select zone, add city/state
3. Save

### 4. Viewing Shipping Calculations

In the admin, you can:
- View all products with their weights: **Admin > Products**
- See total weight column in product list
- Edit weights directly in the list (quick edit)

## Customer Experience

### Checkout Process:
1. Customer adds items to cart
2. Goes to checkout
3. Enters delivery address with **pincode**
4. System automatically:
   - Looks up pincode's shipping zone
   - Calculates total weight of cart items
   - Calculates shipping: `Total Weight × Zone Rate`
   - Checks if order qualifies for free shipping
5. Shows final cost with shipping

### Cart Display:
- Shows individual product weights
- Shows total cart weight
- Shows estimated shipping cost (before pincode entry)
- After pincode entry, shows exact shipping cost

## Technical Details

### Database Models:

**Product Model:**
```python
weight_kg = DecimalField(
    max_digits=6, 
    decimal_places=3,
    default=0.100,
    help_text="Product weight in kilograms"
)
```

**ShippingZone Model:**
```python
cost_per_kg = DecimalField(
    max_digits=10,
    decimal_places=2,
    default=50.00,
    help_text="Shipping cost per kilogram"
)
```

### Calculation Flow:
1. **Cart.get_total_weight()**: Sums all product weights × quantities
2. **ShippingZone.get_rate_for_pincode()**: Finds zone for pincode
3. **Calculate**: `Total Weight (kg) × Zone Rate (₹/kg)`
4. **Check Free Shipping**: If cart total ≥ threshold, return ₹0

### API Endpoints:
- Shipping calculation happens server-side for security
- Real-time updates when pincode is entered
- Weight validation on product creation

## Best Practices

### For Admins:
✅ **Weigh products accurately** - Use a digital scale
✅ **Use 3 decimal places** - For precision (e.g., 0.125 kg)
✅ **Set realistic thresholds** - Balance free shipping with costs
✅ **Keep pincode database updated** - Add new pincodes regularly
✅ **Review shipping costs periodically** - Adjust zone rates as needed

### For Product Entry:
- **Light Items**: 0.050 - 0.200 kg
- **Medium Items**: 0.200 - 0.800 kg
- **Heavy Items**: 0.800+ kg

### For Zone Management:
- Review rates quarterly
- Monitor shipping costs vs revenue
- Adjust free shipping threshold based on average order value
- Consider seasonal rate adjustments

## Troubleshooting

### Issue: Shipping cost too high
**Solution**: 
- Check product weights are correct (not in grams!)
- Verify zone rates are per kg, not total
- Check if free shipping threshold is set correctly

### Issue: Pincode not found
**Solution**:
- Import pincode via Excel
- Or add manually in Admin > Pincode Zones
- Falls back to default rate if pincode not in database

### Issue: Free shipping not applying
**Solution**:
- Verify cart total ≥ free_shipping_threshold
- Check zone is active (`is_active=True`)
- Ensure calculation happens after cart total update

## Future Enhancements

Possible improvements:
- [ ] Volumetric weight calculation
- [ ] Different rates for express delivery
- [ ] Weight-based discounts on shipping
- [ ] International shipping zones
- [ ] Real-time courier API integration
- [ ] Shipping insurance options

## Support

For issues or questions:
1. Check Django admin error messages
2. Review product weights are in kg (not grams)
3. Verify pincode-zone mappings
4. Check shipping zone configurations
5. Review cart total calculations

---

**Last Updated**: November 8, 2025
**System Version**: 1.0 - Weight-Based Shipping
