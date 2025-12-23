"""
Template tags for currency conversion
"""
from django import template
from shop.currency import get_currency, convert_price, format_price

register = template.Library()


@register.filter
def currency_convert(price, request):
    """Convert price to current currency"""
    if not price:
        return 0
    
    current_currency = get_currency(request)
    if current_currency == 'USD':
        return convert_price(float(price), 'INR', 'USD')
    return float(price)


@register.filter
def currency_format(price, request):
    """Format price with currency symbol"""
    if not price:
        return format_price(0, get_currency(request))
    
    current_currency = get_currency(request)
    if current_currency == 'USD':
        converted = convert_price(float(price), 'INR', 'USD')
        return format_price(converted, 'USD')
    return format_price(float(price), 'INR')


@register.simple_tag(takes_context=True)
def show_price(context, price):
    """Display price in current currency"""
    request = context['request']
    if not price:
        return format_price(0, get_currency(request))
    
    current_currency = get_currency(request)
    if current_currency == 'USD':
        converted = convert_price(float(price), 'INR', 'USD')
        return format_price(converted, 'USD')
    return format_price(float(price), 'INR')
