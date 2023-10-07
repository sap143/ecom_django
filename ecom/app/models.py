from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    # Add any other relevant fields (e.g., images, ratings, etc.)
    
    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def update_total_price(self):
        self.total_price = sum(item.product.price * item.quantity for item in self.cart_items.all())
        self.save()

    def __str__(self):
        return f'Cart for {self.user.username}'
    


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def update_total_price(self):
        self.cart.update_total_price()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_total_price()
    
    def __str__(self):
        return f'{self.product.title} in {self.cart.user.username}\'s cart'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending')
    # Add any other relevant fields (e.g., shipping address, date, etc.)
    
    def __str__(self):
        return f'Order {self.id} by {self.user.username}'
    



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.product.price * self.quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.quantity} of {self.product.title} in Order {self.order.id}'



