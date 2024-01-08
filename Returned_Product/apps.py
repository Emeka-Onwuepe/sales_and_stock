from django.apps import AppConfig


class ReturnedProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Returned_Product'
    
    def ready(self):
        from Returned_Product import signals
