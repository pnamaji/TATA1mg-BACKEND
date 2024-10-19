from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class CustomBackend(ModelBackend):
    """
    Custom authentication backend to allow users to log in with either their email or mobile number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get the user by email or mobile number
            user = User.objects.get(Q(email=username) | Q(mobile_number=username))
        except User.DoesNotExist:
            return None
        
        # Check if the password is correct
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
