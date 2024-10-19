from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = 'Account'  # Replace with your app's name

    def ready(self):
        import Account.signals  # Import the signals module when the app is ready