from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # Requires `Pillow` for image uploads
    seller = models.CharField(max_length=100, default="Nearest Seller")
    shipping_time = models.CharField(max_length=50, default="3-4 days")

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Actual price
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Discount price
    image = models.ImageField(upload_to='products/')
    seller = models.CharField(max_length=255, null=True, blank=True)
    shipping_time = models.CharField(max_length=50, default="3-4 days")
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user} - {self.product.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.product.name}"
    


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional user
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Processing', 'Processing'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} by {self.user.username if self.user else 'Guest'}"




class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"