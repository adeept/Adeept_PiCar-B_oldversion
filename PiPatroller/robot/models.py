from django.contrib import admin
from django.db import models


# Create your models here.
class Config(models.Model):
    key = models.CharField(max_length=30, primary_key=True)
    value = models.CharField(max_length=512)

    @staticmethod
    def get(key):
        try:
            o = Config.objects.get(key=key)
            return o.value
        except:
            return None

    @staticmethod
    def get_config():
        config = {}
        for o in Config.objects.all():
            config[o.key] = o.value
        return config

    def __str__(self):
        return self.key


admin.site.register(Config)
