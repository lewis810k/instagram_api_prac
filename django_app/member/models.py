from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    def to_dict(self):
        return {
            'pk': self.pk,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
