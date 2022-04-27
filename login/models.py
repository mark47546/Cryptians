import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_cryptography.fields import encrypt

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = encrypt(models.CharField(max_length=100))
