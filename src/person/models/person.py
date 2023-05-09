from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone

from main.models import BaseModel
from main.utils.time import to_timestamp


class Person(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=254)
    last_activity = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self._password = None
            self.save(update_fields=['password'])

        return check_password(raw_password, self.password, setter)

    def as_dict(self):
        return {
            'id': str(self.id),
            'name': self.name
        }

    def as_activity_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'last_activity': to_timestamp(self.last_activity),
            'last_login': to_timestamp(self.last_login),
        }
