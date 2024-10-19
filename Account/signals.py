from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils.timezone import now
from .models import LoginHistory

# Capture Login event
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip_address = request.META.get('REMOTE_ADDR')
    # Save Login History
    LoginHistory.objects.create(user=user, login_time=now(), ip_address=ip_address)
    
# Capture Logout event
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    # Update the logout_time of the latest login record
    login_history = LoginHistory.objects.filter(user=user, logout_time__isnull=True).last()
    if login_history:
        login_history.logout_time = now()
        login_history.save()