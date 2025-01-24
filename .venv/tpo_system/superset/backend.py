from django.contrib.auth.backends import ModelBackend
from .models import CustomUser  # Import your CustomUser model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Attempt to get the user by email
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None  # Return None if user does not exist
            
        # Check if the password is valid
        if user.check_password(password):
            return user  # Return the user if password matches
        return None  # Return None if password does not match