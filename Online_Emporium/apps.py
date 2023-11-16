from django.apps import AppConfig


class OnlineEmporiumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Online_Emporium'

    def ready(self):
        import Online_Emporium.signals  
