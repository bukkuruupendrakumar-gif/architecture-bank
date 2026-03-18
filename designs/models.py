from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Design(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='designs')

    # ❤️ LIKE FEATURE
    likes = models.ManyToManyField(User, related_name='liked_designs', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name


# ⭐ WISHLIST MODEL
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.design.name}"