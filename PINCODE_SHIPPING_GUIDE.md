# Pincode-Based Shipping System Guide

## Overview
The shipping system now calculates shipping charges based on:
1. **Pincode** entered by the customer
2. **Country** detected from the pincode
3. **Total weight** of products in cart
4. **Shipping rate per kg** for that country

## How It Works

### Step 1: Customer Enters Pincode on Checkout
- Customer fills in the checkout form
- When they enter the **postal code/pincode**, the system:
  1. Looks up the pincode in the `PincodeZone` table
  2. Determines the country from the pincode
  3. Calculates shipping cost based on country rate × total weight

### Step 2: Dynamic Shipping Calculation
- **AJAX endpoint**: `/ajax/calculate-shipping/`
- **Triggered when**: Customer enters pincode and leaves the field (blur event)
- **Returns**: 
  - Shipping cost
  - Detected country
  - Total weight
  - Cart total

### Step 3: Order Creation
- When customer submits the order:
  - System uses pincode to lookup country
  - Calculates final shipping cost: `Country Rate (₹/kg) × Total Weight (kg)`
  - Stores shipping cost in the order

## Database Structure

### PincodeZone Model
```python
class PincodeZone:
    pincode = CharField(max_length=10, unique=True)  # e.g., "018956", "10001"
    country = CharField(max_length=100)              # e.g., "Singapore", "USA"
    city = CharField(max_length=100)                 # e.g., "Singapore", "New York"
    state = CharField(max_length=100)                # For India zones
    zone = ForeignKey(ShippingZone, null=True)       # For India zone-based shipping
```

### ShippingRate Model
```python
class ShippingRate:
    name = CharField(max_length=100)                 # e.g., "Singapore Standard"
    country = CharField(max_length=100)              # e.g., "Singapore"
    cost = DecimalField()                            # Cost per kg (e.g., 290.00)
    min_order_value = DecimalField()                 # Minimum order value
    priority = IntegerField()                        # Lower = higher priority
```

## Shipping Calculation Logic

### Formula
```
Shipping Cost = Country Rate (₹/kg) × Total Weight (kg)
```

### Example Calculation
**Cart Contents:**
- Product A: 0.5 kg × 2 qty = 1.0 kg
- Product B: 0.3 kg × 1 qty = 0.3 kg
- **Total Weight**: 1.3 kg

**Customer Location:**
- Pincode: 018956
- Detected Country: Singapore
- Singapore Rate: ₹290/kg

**Shipping Cost:**
```
1.3 kg × ₹290/kg = ₹377.00
```

## Supported Countries & Rates

### Asia Pacific & Middle East
- Malaysia: ₹255/kg
- Singapore: ₹290/kg
- Sri Lanka: ₹799/kg
- Maldives: ₹343/kg
- UAE: ₹230/kg

### Oceania
- Australia: ₹436/kg
- New Zealand: ₹649/kg

### United Kingdom
- United Kingdom: ₹365/kg

### Western Europe
- Germany: ₹535/kg
- France: ₹565/kg
- Monaco: ₹565/kg
- Austria: ₹553/kg
- Belgium: ₹553/kg
- Luxembourg: ₹553/kg
- Netherlands: ₹553/kg

### Central Europe
- Czech Republic: ₹563/kg
- Denmark: ₹563/kg
- Hungary: ₹576/kg
- Italy: ₹576/kg
- Poland: ₹576/kg
- Slovak Republic: ₹576/kg
- Slovenia: ₹576/kg
- Sweden: ₹594/kg

### Northern & Baltic Europe
- Estonia: ₹613/kg
- Finland: ₹613/kg
- Croatia: ₹613/kg
- Lithuania: ₹613/kg
- Latvia: ₹613/kg

### Southern & Eastern Europe
- Bulgaria: ₹647/kg
- Bosnia: ₹647/kg
- Greece: ₹647/kg
- Iceland: ₹647/kg
- Romania: ₹647/kg
- Serbia: ₹647/kg

### Atlantic Europe
- Ireland: ₹584/kg
- Portugal: ₹584/kg

### India (Zone-based)
- North India: ₹50/kg
- South India: ₹60/kg
- East India: ₹55/kg
- West India: ₹55/kg
- Central India: ₹50/kg

## Admin Management

### 1. Add Shipping Rates via Excel
**URL**: `/admin/shop/shippingrate/import-excel/`

**Excel Format:**
| Name | Description | Country | Cost (₹/kg) | Min Order Value | Max Order Value | Free Shipping Threshold | Priority |
|------|-------------|---------|-------------|-----------------|-----------------|------------------------|----------|
| Singapore Standard | Standard shipping | Singapore | 290 | 0 | | | 1 |

### 2. Add Pincodes via Excel
**URL**: `/admin/shop/pincodezone/import-excel/`

**Excel Format:**
| Pincode | City | State | Country | Zone |
|---------|------|-------|---------|------|
| 018956 | Singapore | | Singapore | |
| 10001 | New York | NY | United States | |

### 3. Management Commands

#### Setup International Shipping Rates
```bash
python manage.py setup_international_shipping
```
Creates shipping rates for 36+ countries.

#### Setup International Pincodes
```bash
python manage.py setup_international_pincodes
```
Creates sample pincode mappings for major cities worldwide.

## Customer Experience

### Checkout Flow
1. **Add products to cart**
   - Each product has a weight (in kg)
   - Cart displays total items

2. **Go to checkout**
   - Fill in billing information
   - Enter shipping address
   - **Enter postal code/pincode**

3. **Automatic shipping calculation**
   - When pincode is entered and user leaves the field
   - System detects country from pincode
   - Displays: "Shipping to [Country] • [X.XXX] kg"
   - Shows shipping cost: "₹XXX.XX"

4. **Place order**
   - Final total includes: Subtotal + Shipping + Tax
   - Shipping is calculated based on actual weight

### Sample Pincodes for Testing

#### Singapore
- 018956 (Singapore)
- 238859 (Singapore)
- 629418 (Singapore)

#### Malaysia
- 50088 (Kuala Lumpur)
- 10250 (Penang)
- 80000 (Johor Bahru)

#### UAE
- DXB (Dubai)
- AUH (Abu Dhabi)

#### United Kingdom
- SW1A1AA (London)
- EC1A1BB (London)
- M11AE (Manchester)

#### USA
- 10001 (New York)
- 90001 (Los Angeles)
- 60601 (Chicago)

#### Australia
- 2000 (Sydney)
- 3000 (Melbourne)
- 4000 (Brisbane)

## Important Notes

### No Free Shipping
- All orders require shipping payment
- Free shipping threshold is disabled
- Shipping is always calculated based on weight

### Fallback Behavior
- If pincode not found in database: Defaults to India
- If country rate not found: Uses default ₹50/kg
- System prioritizes zone-based shipping for India

### Weight Requirements
- All products must have a `weight_kg` value
- Default weight if not set: 0.100 kg (100g)
- Weight is used in all shipping calculations

## API Endpoints

### Calculate Shipping (AJAX)
**URL**: `POST /ajax/calculate-shipping/`

**Parameters:**
- `pincode`: Postal code/pincode (required)
- `country`: Country name (optional)

**Response:**
```json
{
    "success": true,
    "shipping_cost": 377.00,
    "country": "Singapore",
    "total_weight_kg": 1.3,
    "cart_total": 2500.00,
    "formatted_shipping": "₹377.00"
}
```

## Files Modified

1. **Models**: `shop/models.py`
   - Added `country` field to `PincodeZone`
   - Updated `ShippingRate.calculate_shipping_cost()` method
   - Added `PincodeZone.get_country_from_pincode()` method

2. **Views**: `shop/views.py`
   - Added `calculate_shipping_ajax()` function

3. **URLs**: `shop/urls.py`
   - Added route for AJAX shipping calculation

4. **Templates**: `templates/shop/checkout.html`
   - Added dynamic shipping cost display
   - Added JavaScript for AJAX shipping calculation

5. **Admin Template**: `templates/admin/import_shippingrate_excel.html`
   - Improved UI with Bootstrap styling
   - Added clear instructions and examples

6. **Management Commands**:
   - `setup_international_shipping.py`: Setup 36+ country rates
   - `setup_international_pincodes.py`: Setup sample pincodes

## Testing the System

### Test Case 1: Singapore Order
1. Add product (0.5 kg) to cart
2. Go to checkout
3. Enter pincode: `018956`
4. System should show:
   - Country: Singapore
   - Shipping: ₹145.00 (0.5 kg × ₹290/kg)

### Test Case 2: UK Order
1. Add product (1.0 kg) to cart
2. Go to checkout
3. Enter pincode: `SW1A1AA`
4. System should show:
   - Country: United Kingdom
   - Shipping: ₹365.00 (1.0 kg × ₹365/kg)

### Test Case 3: India Order
1. Add product (0.8 kg) to cart
2. Go to checkout
3. Enter pincode: `110001` (Delhi)
4. System should show:
   - Country: India
   - Shipping: ₹40.00 (0.8 kg × ₹50/kg for North zone)

## Maintenance

### Adding New Countries
1. Go to Admin → Shipping Rates → Import Excel
2. Download sample template
3. Add new country with rate per kg
4. Upload Excel file

### Adding New Pincodes
1. Go to Admin → Pincode Zones → Import Excel
2. Download sample template
3. Add pincodes with country mappings
4. Upload Excel file

### Updating Rates
- Rates can be updated individually or via Excel import
- Changes take effect immediately
- No need to restart the server

## Troubleshooting

### Shipping not calculating
- Check if pincode exists in database
- Verify country has a shipping rate
- Check browser console for JavaScript errors

### Wrong country detected
- Update pincode mapping in admin
- Or add correct pincode via Excel import

### Rate not applied
- Check shipping rate priority (lower = higher priority)
- Verify min_order_value constraint
- Ensure rate is active (`is_active = True`)
