from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    
class Category(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField()

    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Menu(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    description = models.TextField()

    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu/',null=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    customer = models.ForeignKey( Customer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.first_name

class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    def total_price(self):
        return self.menu.price * self.quantity        
        
class Order(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        default="Cash On Delivery"
    )

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def subtotal(self):
        return self.quantity * self.price        