from django.db import models
from django.contrib.auth.models import User as AbstractUser
from django.utils.functional import cached_property

# Create your models here.


class User(AbstractUser):
    class Meta:
        proxy = True
