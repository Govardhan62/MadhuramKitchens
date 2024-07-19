from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class PhoneEmailBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, email=None, password=None, **kwargs):
        try:
            # Try to fetch the user by phone number or email
            user = UserModel.objects.get(
                Q(phone_number=phone_number) | Q(email=email)
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
