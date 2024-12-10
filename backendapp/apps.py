from django.apps import AppConfig


class BackendappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backendapp'

    def ready(self):
        import backendapp.signals