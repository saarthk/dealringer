from rest_framework import serializers
from .models import Phone, Posting, UserInfo, SavedPhone
from django.contrib.auth.models import User


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ["id"]


class PostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posting
        fields = ["phone", "variant", "posting_url", "price", "seller"]


# SavedPhone model will not be serialized. This is because it is an intermediary model,
# and won't be serialized and rendered to JSON (or other content types).
# Nor will it be parsed and deserialized, since requests will never contain SavedPhone data.


class UserInfoSerializer(serializers.ModelSerializer):
    # The UserInfoSerializer will not be serialized directly.
    # Instead, it will be used as a nested serializer in UserSerializer.
    class Meta:
        model = UserInfo
        # We only serialize the userid_3p field from UserInfo model.
        fields = ["userid_3p"]


class UserSerializer(serializers.ModelSerializer):
    # UserInfo will be nested inside the User model. Hence, we create a nested serializer for UserInfo.
    additional_info = UserInfoSerializer()

    class Meta:
        model = User
        # We exclude the password field from serialization, since APIs will use token-based authentication.
        exclude = ["password"]

    # The create method is overridden to create the UserInfo instance along with the User instance.
    # By default, nested serializers are read-only. We need to override the create method to make them writable.
    # Refer https://www.django-rest-framework.org/api-guide/relations/#writable-nested-serializers

    # The serialized User object (typically a dictionary) will be of the form:
    # {"username": "user1", "password": "password1", "email": "user1@example.com", ..., "additional_info": {"userid_3p": "12345"}}
    def create(self, validated_data):
        # The nested UserInfo data is popped out from the validated_data.
        info_data = validated_data.pop("additional_info")
        user = User.objects.create(**validated_data)
        # Since we are not using the password field for authentication, we set it as unusable (best practice).
        user.set_unusable_password()
        user.save()
        UserInfo.objects.create(auth_user=user, **info_data)

        # Since UserInfo model has a one-to-one relation with User model, the User model
        # will have a reference to the UserInfo model instance, via its additional_info attribute.
        return user
