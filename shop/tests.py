"""
Tests for the Sri Devi Fashion Jewellery application

This module contains tests for:
- Models
- Views
- Forms
- Cart functionality
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from shop.models import Category, Product, Order, OrderItem, UserProfile
from shop.cart import Cart
from shop.forms import CustomUserCreationForm, ProductSearchForm


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test category description'
        )
    
    def test_category_creation(self):
        """Test category creation"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')
        self.assertEqual(str(self.category), 'Test Category')
    
    def test_category_absolute_url(self):
        """Test category absolute URL"""
        expected_url = reverse('shop:category_detail', kwargs={'slug': 'test-category'})
        self.assertEqual(self.category.get_absolute_url(), expected_url)


class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product description',
            price=Decimal('99.99'),
            stock=10,
            size='M',
            color='blue'
        )
    
    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, Decimal('99.99'))
        self.assertEqual(str(self.product), 'Test Product')
    
    def test_product_absolute_url(self):
        """Test product absolute URL"""
        expected_url = reverse('shop:product_detail', kwargs={'slug': 'test-product'})
        self.assertEqual(self.product.get_absolute_url(), expected_url)
    
    def test_product_is_in_stock(self):
        """Test product stock checking"""
        self.assertTrue(self.product.is_in_stock())
        
        # Test out of stock
        self.product.stock = 0
        self.assertFalse(self.product.is_in_stock())
        
        # Test unavailable
        self.product.stock = 10
        self.product.available = False
        self.assertFalse(self.product.is_in_stock())


class UserProfileModelTest(TestCase):
    """Test UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test that user profile is created automatically"""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(str(self.user.userprofile), "testuser's Profile")


class CartTest(TestCase):
    """Test shopping cart functionality"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product description',
            price=Decimal('99.99'),
            stock=10
        )
    
    def test_add_to_cart(self):
        """Test adding product to cart"""
        # Simulate a request
        session = self.client.session
        session['cart'] = {}
        session.save()
        
        # Create cart and add product
        request = type('Request', (), {'session': session})()
        cart = Cart(request)
        cart.add(self.product, quantity=2)
        
        # Check cart contents
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal('199.98'))
    
    def test_cart_view(self):
        """Test cart detail view"""
        response = self.client.get(reverse('shop:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shopping Cart')


class ProductViewTest(TestCase):
    """Test product views"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product description',
            price=Decimal('99.99'),
            stock=10,
            available=True
        )
    
    def test_product_list_view(self):
        """Test product list view"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
    def test_product_detail_view(self):
        """Test product detail view"""
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': 'test-product'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '99.99')
    
    def test_category_detail_view(self):
        """Test category detail view"""
        response = self.client.get(
            reverse('shop:category_detail', kwargs={'slug': 'test-category'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')


class UserAuthenticationTest(TestCase):
    """Test user authentication views"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_register_view(self):
        """Test user registration view"""
        response = self.client.get(reverse('shop:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
    
    def test_login_view(self):
        """Test login view"""
        response = self.client.get(reverse('account_login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
    
    def test_user_login(self):
        """Test user login functionality"""
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser',
            'password': 'testpass123'
        })
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication"""
        response = self.client.get(reverse('shop:profile'))
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
    
    def test_profile_view_authenticated(self):
        """Test profile view when authenticated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('shop:profile'))
        self.assertEqual(response.status_code, 200)


class FormsTest(TestCase):
    """Test forms"""
    
    def test_user_creation_form(self):
        """Test custom user creation form"""
        form_data = {
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'testpass123456',
            'password2': 'testpass123456'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_product_search_form(self):
        """Test product search form"""
        form_data = {
            'query': 'test product',
            'min_price': '10.00',
            'max_price': '100.00',
            'size': 'M',
            'color': 'blue'
        }
        form = ProductSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class OrderModelTest(TestCase):
    """Test Order model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            category=self.category,
            description='Test product',
            price=Decimal('99.99'),
            stock=10
        )
        self.order = Order.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='1234567890',
            address_line_1='123 Test St',
            city='Test City',
            state='Test State',
            postal_code='12345',
            total_amount=Decimal('99.99'),
            payment_method='razorpay'
        )
    
    def test_order_creation(self):
        """Test order creation"""
        self.assertTrue(self.order.order_number)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(str(self.order), f"Order {self.order.order_number}")
    
    def test_order_absolute_url(self):
        """Test order absolute URL"""
        expected_url = reverse('shop:order_detail', kwargs={'order_number': self.order.order_number})
        self.assertEqual(self.order.get_absolute_url(), expected_url)
    
    def test_order_total_cost(self):
        """Test order total cost calculation"""
        self.order.shipping_cost = Decimal('10.00')
        self.order.tax_amount = Decimal('5.00')
        expected_total = Decimal('114.99')  # 99.99 + 10.00 + 5.00
        self.assertEqual(self.order.get_total_cost(), expected_total)


class SearchTest(TestCase):
    """Test search functionality"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics'
        )
        self.product1 = Product.objects.create(
            name='Smartphone',
            slug='smartphone',
            category=self.category,
            description='High-end smartphone',
            price=Decimal('599.99'),
            stock=5,
            available=True
        )
        self.product2 = Product.objects.create(
            name='Laptop',
            slug='laptop',
            category=self.category,
            description='Gaming laptop',
            price=Decimal('1299.99'),
            stock=3,
            available=True
        )
    
    def test_product_search(self):
        """Test product search functionality"""
        response = self.client.get(reverse('shop:product_search'), {'query': 'smartphone'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')
        self.assertNotContains(response, 'Laptop')
    
    def test_price_filter(self):
        """Test price filtering in search"""
        response = self.client.get(reverse('shop:product_search'), {
            'min_price': '1000.00',
            'max_price': '1500.00'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertNotContains(response, 'Smartphone')