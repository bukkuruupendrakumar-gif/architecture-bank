from django.db import models
from django.contrib.auth.models import User


# 📂 CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# 🎨 DESIGN
class Design(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='designs/')

    # ❤️ LIKE
    likes = models.ManyToManyField(User, related_name='liked_designs', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.name


# ⭐ WISHLIST
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'design')

    def __str__(self):
        return f"{self.user.username} - {self.design.name}"


# 📅 BOOKING (FINAL UPDATED ✅)
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)

    # 👤 CUSTOMER DETAILS (WITH DEFAULTS ✅)
    name = models.CharField(max_length=100, default="unknown")
    phone = models.CharField(max_length=15, default="0000000000")
    address = models.TextField(default="not provided")

    # 💳 PAYMENT STATUS
    status = models.CharField(max_length=50, default="Pending")

    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'design')

    def __str__(self):
        return f"{self.user.username} booked {self.design.name}"