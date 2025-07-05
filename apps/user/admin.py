from django.contrib import admin
from django.apps import apps
from apps.user.models import User

# Register your models here.
my_app = apps.get_app_config("user")

admin.site.register(User)