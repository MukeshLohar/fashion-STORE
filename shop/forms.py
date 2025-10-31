"""
Forms for the Fashion Store application

This module contains all forms used throughout the application:
- User registration and profile forms
- Order and checkout forms
- Product review forms
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Order, Review


class CustomUserCreationForm(UserCreationForm):
    """Enhanced user registration form with additional fields"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Update placeholders
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile information"""
    
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'address_line_1', 'address_line_2', 
            'city', 'state', 'postal_code', 'country', 'date_of_birth'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address line 2 (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal/ZIP code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CheckoutForm(forms.ModelForm):
    """Form for checkout and order placement"""
    
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address_line_1', 'address_line_2', 'city', 
            'state', 'postal_code', 'country', 'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address line 2 (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal/ZIP code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Pre-populate form with user data if available
        if user and user.is_authenticated:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            
            # Pre-populate with profile data if available
            if hasattr(user, 'userprofile'):
                profile = user.userprofile
                self.fields['phone'].initial = profile.phone
                self.fields['address_line_1'].initial = profile.address_line_1
                self.fields['address_line_2'].initial = profile.address_line_2
                self.fields['city'].initial = profile.city
                self.fields['state'].initial = profile.state
                self.fields['postal_code'].initial = profile.postal_code
                self.fields['country'].initial = profile.country


class CartAddProductForm(forms.Form):
    """Form for adding products to cart"""
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 80px;',
            'min': '1'
        })
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )


class ProductReviewForm(forms.ModelForm):
    """Form for product reviews"""
    
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }


class ProductSearchForm(forms.Form):
    """Form for product search"""
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...',
            'autocomplete': 'off'
        })
    )
    category = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.HiddenInput()
    )
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min price',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max price',
            'step': '0.01'
        })
    )
    size = forms.ChoiceField(
        choices=[('', 'Any Size')] + [choice for choice in [
            ('XS', 'Extra Small'),
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
            ('XXL', 'Double Extra Large'),
        ]],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    color = forms.ChoiceField(
        choices=[('', 'Any Color')] + [choice for choice in [
            ('red', 'Red'),
            ('blue', 'Blue'),
            ('green', 'Green'),
            ('black', 'Black'),
            ('white', 'White'),
            ('gray', 'Gray'),
            ('navy', 'Navy'),
            ('pink', 'Pink'),
            ('yellow', 'Yellow'),
            ('purple', 'Purple'),
            ('brown', 'Brown'),
            ('orange', 'Orange'),
        ]],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )