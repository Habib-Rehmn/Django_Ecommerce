from http.client import responses
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
import secrets





class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    details_image_1 = models.ImageField(upload_to='products/', default=None)
    details_image_2 = models.ImageField(upload_to='products/', default=None)
    details_image_3 = models.ImageField(upload_to='products/', default=None)
    details_image_4 = models.ImageField(upload_to='products/', default=None)
    details_image_5 = models.ImageField(upload_to='products/', default=None)
    price = models.FloatField(default=None)
    ratings = models.IntegerField()
    free_shipping = models.BooleanField(default=False)
    brand = models.CharField(max_length=100, default=None)
    description = models.TextField(default=None)
    category = models.CharField(max_length=50, default=None)
    product_type = models.CharField(max_length=50, default=None)
    inventory = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute_name = models.CharField(max_length=50)
    attribute_value = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.product.name} - {self.attribute_name}: {self.attribute_value}"





class CustomUser(AbstractUser):

    address = models.CharField(max_length=255, blank=True, null=True, default=None)
    phone_number = models.CharField(max_length=15, blank=True, null=True, default=None)
    city = models.CharField(max_length=30, blank=True, null=True, default=None)
    full_name = models.CharField(max_length=40, blank=True, null=True, default=None)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=True, null=True, default=None)
    email = models.EmailField(blank=True)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.username
    



class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product, through='CartItem')
    

    def get_total_price(self):
        # Calculate the total price of items in the cart
        total_price = sum(item.get_subtotal() for item in self.cart_items.all())
        return total_price
    
    
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def get_subtotal(self):
        # Calculate the subtotal for this item
        return self.product.price * self.quantity




class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # You can adjust the decimal places as needed
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True, null=True, default=None)
    phone_number = models.CharField(max_length=15, blank=True, null=True, default=None)
    city = models.CharField(max_length=30, blank=True, null=True, default=None)
    full_name = models.CharField(max_length=40, blank=True, null=True, default=None)
    zip_code = models.CharField(max_length=10, blank=True, null=True, default=None)
    email = models.EmailField(blank=True)
    order_id = models.CharField(max_length=10, unique=True)
    # Define order status choices
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_process', 'In Process'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('paid','Paid'),
    )

    # Add a status field to the Order model
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    PAYMENT_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('online_payment', 'Online Payment'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash_on_delivery')
    ordered_products = models.ManyToManyField(Product, related_name='orders', blank=True)
    product_quantity = models.JSONField(null=True, blank=True)
    def generate_unique_order_id(self):
        order_id = ''
        while not order_id:
            # Generate a random 4-character alphanumeric order ID
            order_id = secrets.token_hex(2).upper()
            if Order.objects.filter(order_id=order_id).exists():
                order_id = ''  # Clear order_id and try again
        return order_id

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_unique_order_id()
        super(Order, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'Order: {self.order_id}'




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE )
    cart_item = models.OneToOneField(CartItem, on_delete=models.CASCADE, related_name='order_items')






class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True)
    discount_percentage = models.PositiveIntegerField()    