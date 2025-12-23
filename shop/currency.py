"""
Currency conversion utility for Sri Devi Fashion Jewellery
Handles INR to USD conversion
"""

# Current exchange rate (update periodically or use API)
INR_TO_USD = 0.012  # 1 INR = 0.012 USD (approximately)

def get_currency(request):
    """Get current currency from session"""
    return request.session.get('currency', 'INR')

def set_currency(request, currency):
    """Set currency in session"""
    if currency in ['INR', 'USD']:
        request.session['currency'] = currency
        return True
    return False

def convert_price(amount, from_currency='INR', to_currency='USD'):
    """Convert price from one currency to another"""
    if from_currency == to_currency:
        return amount
    
    if from_currency == 'INR' and to_currency == 'USD':
        return round(amount * INR_TO_USD, 2)
    elif from_currency == 'USD' and to_currency == 'INR':
        return round(amount / INR_TO_USD, 2)
    
    return amount

def format_price(amount, currency='INR'):
    """Format price with currency symbol"""
    if currency == 'USD':
        return f'${amount:.2f}'
    else:  # INR
        return f'₹{amount:.2f}'
