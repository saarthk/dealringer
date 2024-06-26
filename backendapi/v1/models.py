from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.indexes import GinIndex


# Model to store phone details
class Phone(models.Model):
    class Meta:
        indexes = [
            GinIndex(
                SearchVector("brand_name", "model_name", config="english"),
                name="phone_search_index",
            )
        ]

    device_id = models.CharField(max_length=50, null=True)
    brand_name = models.CharField(max_length=20, null=True)
    model_name = models.CharField(max_length=20, null=True)
    # min_price is the minimum price of the phone across all sellers
    min_price = models.PositiveIntegerField(null=True)
    photo_url = models.URLField(
        default="https://cdn4.iconfinder.com/data/icons/desktop-app-free/32/Desktop_Desktop_App_Smartphone_Phone_Android-09-512.png"
    )


# Model to store posting details. A phone can have multiple postings from different sellers.
class Posting(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE, related_name="postings")
    # variant is the specific model variant (e.g., color, storage) of the phone
    variant = models.CharField(max_length=50, null=True)
    posting_url = models.URLField(null=True)
    price = models.PositiveIntegerField()

    seller_choices = {"AMZ": "Amazon", "FLK": "Flipkart", "CRM": "Croma"}
    seller = models.CharField(max_length=20, choices=seller_choices)
    # last_updated is the time when the posting was last updated
    last_updated = models.DateTimeField(default=timezone.now)


# Model to extend auth.User model
class UserInfo(models.Model):
    # auth_user is the one-to-one field to the corresponding auth.User model
    auth_user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="additional_info"
    )
    # userid_3p is the unique identifier for the user in the third-party user management service
    userid_3p = models.CharField(max_length=50, null=True)
    # saved_phones is the many-to-many field to the Phone model, through the SavedPhoneInfo model.
    # This field stores the phones saved by the user.
    saved_phones = models.ManyToManyField(Phone, through="SavedPhone")


# Intermediary model for many-to-many relationship between UserInfo and Phone
class SavedPhone(models.Model):
    # related_name is set to "+" to avoid backward relation from UserInfo to SavedPhone
    # since UserInfo already has a direct (forward) relation to SavedPhone through saved_phones field.
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="+")
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    # is_alert is True if user has set a price alert for this phone
    is_alert = models.BooleanField(default=False)
