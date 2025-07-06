from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    logo = models.ImageField(upload_to="logo", blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_auth_token(self):
        return "Token " + self.custom_auth_token.create(user_id=self.id).key
    
    def delete_auth_token(self, key):
        self.custom_auth_token.filter(key=key).delete()

