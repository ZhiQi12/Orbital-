from django.apps import AppConfig

class ModerateConfig(AppConfig):
    name = 'moderate'

    def ready(self):
        from .scheduler import updater
        updater.start()