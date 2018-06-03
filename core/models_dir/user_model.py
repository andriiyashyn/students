from django.contrib.auth.models import User
from django.db import models


class Client(User):
    is_admin = models.BooleanField(default=False)