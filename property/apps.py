from django.apps import AppConfig


class PropertyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'property'

    def ready(self):
        try:
            import property.signals  # noqa F401
        except ImportError:
            pass
