from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    # items = GenericRelation('ShopItem')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # items = GenericRelation('ShopItem')

    def __str__(self):
        return self.name


class ShopItem(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    short_description = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    picture = models.URLField(max_length=200)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")

    def __str__(self):
        return str(self.user) + ": Cart " + str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.cart.user) + ": " + self.product.name + " - Cart " + str(self.cart.id)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order")
    number = models.IntegerField()
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    archival = models.BooleanField()

    def __str__(self):
        return str(self.user) + ": Order no. " + str(self.number)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.order.user) + ": " + self.product.name + " - Order no. " + str(self.order.number)
