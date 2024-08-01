from django.apps import AppConfig


class NotebookManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notebook_manager'

    def ready(self):
        import notebook_manager.signals
