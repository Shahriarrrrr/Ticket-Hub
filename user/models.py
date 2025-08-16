from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('OPERATOR', 'Operator'),   # Bus or Event operator
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    # Basic info inherited: username, email, first_name, last_name, password
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Email/Phone verification
    is_premium = models.BooleanField(default=False)   # Premium user feature
    loyalty_points = models.PositiveIntegerField(default=0)
    country = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=20, default='en')

    def __str__(self):
        return self.username
