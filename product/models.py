from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings


from Category.models import Category, PodCategory
from user_profiles.models import CustomUser

class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    podcategory = models.ForeignKey(PodCategory, related_name="pod_products", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    image1 = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True, null=True)
    image2 = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True, null=True)
    image3 = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True, null=True)
    image4 = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True, null=True)

    description = models.TextField()
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    location = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-created"]),
        ]
        ordering = ["title"]

        indexes = [
            models.Index(fields=["id"]),
            models.Index(fields=["title"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.title


class Recall(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField()
    file = models.FileField(upload_to="recalls/%Y/%m/%d", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Discount(models.Model):
    product = models.OneToOneField(
        Product, related_name="discount", on_delete=models.CASCADE
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def discounted_price(self):
        return self.price * (1 - self.discount_rate)

    def __str__(self):
        return f"Discount for {self.product.name}"