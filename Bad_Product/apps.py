from django.apps import AppConfig


class BadProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Bad_Product'
    
    def ready(self):
        from Bad_Product import signals
