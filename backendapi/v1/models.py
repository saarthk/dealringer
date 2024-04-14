from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Model to store phone details
class Phone(models.Model):
    device_id = models.CharField(max_length=50, null=True)
    brand_name = models.CharField(max_length=20, null=True)
    model_name = models.CharField(max_length=20, null=True)
    photo_url = models.URLField(
        default="https://cdn4.iconfinder.com/data/icons/desktop-app-free/32/Desktop_Desktop_App_Smartphone_Phone_Android-09-512.png"
    )


# Model to store price details
class Price(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name="prices")
    posting_url = models.URLField(null=True)
    posting_price = models.PositiveIntegerField()
    
    seller_choices = {"AMZ": "Amazon", "FLK": "Flipkart", "CRM": "Croma"}
    seller = models.CharField(max_length=20, choices=seller_choices)
    last_updated = models.DateTimeField(default=timezone.now)


# Intermediary model to store user's saved phones
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_phones = models.ManyToManyField(Phone, through="SavedPhoneInfo")


class SavedPhoneInfo(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    is_alert = models.BooleanField(default=False)
